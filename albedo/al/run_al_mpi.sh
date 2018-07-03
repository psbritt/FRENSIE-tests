#!/bin/sh
# This file is named run_al_mpi.sh
#SBATCH --partition=pre
#SBATCH --time=1-00:00:00
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=16
#SBATCH --mem-per-cpu=4000

##---------------------------------------------------------------------------##
## ---------------------------- FACEMC test runner --------------------------##
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## The electron albedo is found for a semi-infinite aluminum slab. Since the
## electron albedo requires a surface current, DagMC will be used and not Root.
## FRENSIE will be run with three variations.
## 1. Using the Native data in analog mode, whcih uses a different interpolation
## scheme than MCNP.
## 2. Using Native data in moment preserving mode, which should give a less
## acurate answer while decreasing run time.
## 3. Using ACE (EPR14) data, which should match MCNP6.2 almost exactly.

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
# Energy in MeV (.005, .0093, .01, .011, .0134, .015, .0173, .02, .0252, .03, .04, .0415, .05, .06, .0621, .0818, .102)
ENERGY=".102"
THREADS="160"
ELEMENT="Al"
# Number of histories 1e6
HISTORIES="5000000"
# Turn certain reactions on (true/false)
ELASTIC_ON="true"
BREM_ON="true"
IONIZATION_ON="true"
EXCITATION_ON="true"
# Two D Interp Policy (logloglog, linlinlin, linlinlog)
INTERP="logloglog"
# Two D Sampling Policy (1 = unit-base correlated, 2 = correlated, 3 = unit-base)
SAMPLE=1
# Elastic distribution ( Decoupled, Coupled, Hybrid )
DISTRIBUTION="Decoupled"
# Elastic coupled sampling method ( Simplified, 1D, 2D )
COUPLED_SAMPLING="2D"
# Minimum problem energy (default 1e-4 MeV = 100 eV)
ENERGY_MIN="1e-4"

NAME="native"
# NO_ERRORS="true"

# if [ "${ELEMENT}" == "Al" ]; then
#     # Source energies for Al (MeV)
#     energies=( .005 .0093 .01 .011 .0134 .015 .0173 .02 .0252 .03 .04 .0415 .05 .06 .0621 .0818 .102 )
# else
#     NO_ERRORS="false"
#     echo "Error: Element ${ELEMENT} is currently not supported!"
# fi

ELASTIC="-d ${DISTRIBUTION} -c ${COUPLED_SAMPLING}"
REACTIONS=" -t ${ELASTIC_ON} -b ${BREM_ON} -i ${IONIZATION_ON} -a ${EXCITATION_ON}"
SIM_PARAMETERS="-e ${ENERGY} -n ${HISTORIES} -l ${INTERP} -s ${SAMPLE} -m ${ENERGY_MIN} ${REACTIONS} ${ELASTIC}"
ENERGY_EV=$(echo $ENERGY*1000000 |bc)
ENERGY_EV=${ENERGY_EV%.*}

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

# Set the name raction and extention
NAME_EXTENTION=""
NAME_REACTION=""
if [ "${ELASTIC_ON}" = "false" ]; then
    NAME_REACTION="${NAME_REACTION}_no_elastic"
elif [ ${DISTRIBUTION} = "Coupled" ]; then
    if [ ${COUPLED_SAMPLING} = "1D" ]; then
        NAME_EXTENTION="${NAME_EXTENTION}_${COUPLED_SAMPLING}"
        TITLE="${TITLE} ${COUPLED_SAMPLING}"
    elif [ ${COUPLED_SAMPLING} = "2D" ]; then
        NAME_EXTENTION="${NAME_EXTENTION}_${COUPLED_SAMPLING}"
        TITLE="${TITLE} M2D"
    elif  [ ${COUPLED_SAMPLING} = "Simplified" ]; then
        NAME_EXTENTION="${NAME_EXTENTION}_2D_simplified"
        TITLE="${TITLE} 2D"
    fi
elif [ ${DISTRIBUTION} = "Decoupled" ]; then
    NAME_EXTENTION="${NAME_EXTENTION}_${DISTRIBUTION}"
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
INFO=$(python ../../sim_info.py ${SIM_PARAMETERS} 2>&1)
MAT=$(python ../../mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP} 2>&1)
EST=$(python ../est.py -e ${ENERGY} 2>&1)
SOURCE=$(python source.py -e ${ENERGY} 2>&1)
GEOM="geom.xml"
RSP="../rsp_fn.xml"

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)

if [ ${NAME} = "ace" -o ${NAME} = "epr14" ]; then
    DIR="results/${NAME}/${TODAY}"
    NAME="al_${NAME}_${ENERGY_EV}${NAME_REACTION}"
    PROCESSOR="../../../../data_processor.sh ${ENERGY} ${NAME}"
else
    if [ ${SAMPLE} = 1 ]; then
        SAMPLE_NAME="unit_correlated"
    elif [ ${SAMPLE} = 2 ]; then
        SAMPLE_NAME="correlated"
    elif [ ${SAMPLE} = 3 ]; then
        SAMPLE_NAME="unit_base"
    fi

    DIR="results/${INTERP}/${SAMPLE_NAME}${NAME_EXTENTION}${NAME_REACTION}/${TODAY}"
    NAME="al_${NAME}_${ENERGY_EV}_${INTERP}_${SAMPLE_NAME}${NAME_EXTENTION}${NAME_REACTION}"
    PROCESSOR="../../../../../data_processor.sh ${ENERGY} ${NAME}"
fi

mkdir -p $DIR

echo "Running Facemc Albedo test with ${HISTORIES} particles on ${THREADS} threads:"
RUN="mpiexec -n ${THREADS} ${FRENSIE}/bin/facemc-mpi --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME}"
echo ${RUN}

${RUN} > ${DIR}/${NAME}.txt 2>&1

echo "Removing old xml files:"
rm ${INFO} ${EST} ${SOURCE} ${MAT} ../../ElementTree_pretty.pyc

# Process the test results
echo "Processing the results:"
H5=${NAME}.h5
NEW_NAME="${DIR}/${H5}"
NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"
mv ${H5} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

cd ${DIR}

bash ${PROCESSOR}
echo "Results will be in ./${DIR}"
