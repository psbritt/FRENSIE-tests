#!/bin/sh
# This file is named run_facemc_mpi.sh
#SBATCH --partition=pre
#SBATCH --time=1-00:00:00
#SBATCH --nodes=7
#SBATCH --ntasks-per-node=16
#SBATCH --mem-per-cpu=4000

##---------------------------------------------------------------------------##
## ---------------------------- FACEMC test runner --------------------------##
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## The electron angular distribution for a thin gold foil of .0009658 cm.
## The # of particles per steradian for scattering angle is found by dividing
## the surface current by 2pi * ( \mu_{i} - \mu_{i-1} ) where \mu_{0} is the
## lowest cosine bin (ie: -1). Surface current is needed so DagMC will be used.
## The #/steradians can be changed to #/square degree by multiplying by
## (pi/180)^2.
## FRENSIE will be run with three variations.
## 1. Using ACE data, which should match MCNP almost exactly.
## 2. Using the Native data in analog mode, whcih uses a different interpolation
## scheme than MCNP.
## 3. Using Native data in moment preserving mode, which should give a less
## acurate answer while decreasing run time.

##---------------------------------------------------------------------------##
## ------------------------------- COMMANDS ---------------------------------##
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/lkersting/software/mcnpdata/
#CROSS_SECTION_XML_PATH=/home/software/mcnp6.2/MCNP_DATA/
FRENSIE=/home/lkersting/frensie

INPUT="1"
if [ "$#" -eq 1 ]; then
    # Set the file type (1 = Native (default), 2 = ACE EPR14, 3 = ACE EPR12)
    INPUT="$1"
fi

# Changing variables
THREADS="112"
# Number of histories 1e7
HISTORIES="10000000"
# Turn certain reactions on (true/false)
ELASTIC_ON="true"
BREM_ON="true"
IONIZATION_ON="true"
EXCITATION_ON="true"
# Two D Interp Policy (logloglog, linlinlin, linlinlog)
INTERP="logloglog"
# Two D Grid Policy (1 = unit-base correlated, 2 = correlated, 3 = unit-base)
SAMPLE=1
# Elastic distribution ( Decoupled, Coupled, Hybrid )
DISTRIBUTION="Coupled"
# Elastic coupled sampling method ( Simplified, 1D, 2D )
COUPLED_SAMPLING="2D"


ELEMENT="Au"
ENERGY="15.7"
NAME="native"

ELASTIC="-d ${DISTRIBUTION} -c ${COUPLED_SAMPLING}"
REACTIONS=" -t ${ELASTIC_ON} -b ${BREM_ON} -i ${IONIZATION_ON} -a ${EXCITATION_ON}"
SIM_PARAMETERS="-e ${ENERGY} -n ${HISTORIES} -l ${INTERP} -s ${SAMPLE} ${REACTIONS} ${ELASTIC}"

if [ ${INPUT} -eq 2 ]; then
    # Use ACE EPR14 data
    NAME="epr14"
    echo "Using ACE EPR14 data!"
elif [ ${INPUT} -eq 3 ]; then
    # Use ACE EPR12 data
    NAME="ace"
    echo "Using ACE EPR12 data!"
elif [ ${DISTRIBUTION} = "Hybrid" ]; then
    # Use Native moment preserving data
    NAME="moments"
    echo "Using Native Moment Preserving data!"
else
    # Use Native analog data
    echo "Using Native analog data!"
fi

# Set the interp in title
TITLE=""
if [ "${INTERP}" = "logloglog"]; then
    TITLE="Log-log"
elif [ "${INTERP}" = "linlinlin"]; then
    TITLE="Lin-lin"
elif [ "${INTERP}" = "linlinlog"]; then
    TITLE="Lin-log"
fi

# Set the sampling name
SAMPLE_NAME=""
if [ ${SAMPLE} = 1 ]; then
    SAMPLE_NAME="unit_correlated"
    TITLE="${TITLE} Unit-base Correlated"
elif [ ${SAMPLE} = 2 ]; then
    SAMPLE_NAME="correlated"
    TITLE="${TITLE} Correlated"
elif [ ${SAMPLE} = 3 ]; then
    SAMPLE_NAME="unit_base"
    TITLE="${TITLE} Unit-base"
fi

# Set the name raction and extention
NAME_EXTENTION=""
NAME_REACTION=""
if [ "${ELASTIC_ON}" = "false" ]; then
    NAME_REACTION="${NAME_REACTION}_no_elastic"
elif [ ${DISTRIBUTION} = "Coupled" ]; then
    NAME_EXTENTION="${NAME_EXTENTION}_${COUPLED_SAMPLING}"
    TITLE="${TITLE} ${COUPLED_SAMPLING}"
elif [ ${DISTRIBUTION} = "Decoupled" ]; then
    NAME_EXTENTION="${NAME_EXTENTION}_${DISTRIBUTION}"
    TITLE="${TITLE} ${DISTRIBUTION}"
fi
if [ "${BREM_ON}" = "false" ]; then
    NAME_REACTION="${NAME_REACTION}_no_brem"
fi
if [ "${IONIZATION_ON}" = "false" ]; then
    NAME_REACTION="${NAME_REACTION}_no_ionization"
fi
if [ "${EXCITATION_ON}" = "false" ]; then
    NAME_REACTION="${NAME_REACTION}_no_excitation"
fi

# .xml file paths.
INFO=$(python ../sim_info.py ${SIM_PARAMETERS} 2>&1)
MAT=$(python ../mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP} 2>&1)
SOURCE="source.xml"
EST="est.xml"
GEOM="geom.xml"
RSP="../rsp_fn.xml"

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)

if [ ${NAME} = "ace" ] || [ ${NAME} = "epr14" ]; then
    DIR="results/${NAME}/${TODAY}"
    NAME="hanson_${NAME}${NAME_REACTION}"
    TITLE="FACEMC-ACE"
else
    DIR="results/${INTERP}/${TODAY}"

    if [ ${SAMPLE} = 1 ]; then
        SAMPLE_NAME="unit_correlated"
    elif [ ${SAMPLE} = 2 ]; then
        SAMPLE_NAME="correlated"
    elif [ ${SAMPLE} = 3 ]; then
        SAMPLE_NAME="unit_base"
    fi

    if [ ${NAME} = "moments" ]; then
        NAME="${NAME}_moments"
    fi

    NAME="hanson_${NAME}_${INTERP}_${SAMPLE_NAME}${NAME_EXTENTION}${NAME_REACTION}"
    TITLE="FACEMC-ACE"
fi

mkdir -p $DIR

echo "Running Facemc Hanson test with ${HISTORIES} particles on ${THREADS} threads:"
RUN="mpiexec -n ${THREADS} ${FRENSIE}/bin/facemc-mpi --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME}"
echo ${RUN}

${RUN} > ${DIR}/${NAME}.txt 2>&1

echo "Removing old xml files:"
rm ${INFO} ${MAT} ../ElementTree_pretty.pyc


echo "Processing the results:"
# Move file to the test results folder
H5=${NAME}.h5
NEW_NAME="${DIR}/${H5}"
NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"
mv ${H5} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

bash ./data_processor.py -f ${NAME} -t \"${TITLE}\"
echo "Results will be in ./${DIR}"
