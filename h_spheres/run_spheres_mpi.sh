#!/bin/sh
# This file is named run_facemc_mpi.sh
#SBATCH --partition=univ2
#SBATCH --time=4-00:00:00
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=20
#SBATCH --mem-per-cpu=4000

##---------------------------------------------------------------------------##
## ---------------------------- FACEMC test runner --------------------------##
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## The electron surface and cell flux and current for three concentrtic spheres
## of Hydrogen for a 1, 10, 100 keV mono-energetic isotropic source of electrons.
## FRENSIE will be run with three variations.
## 1. Using ACE data, which should match MCNP almost exactly.
## 2. Using the Native data in analog mode, which uses a different interpolation
## scheme than MCNP.
## 3. Using Native data in moment preserving mode, which should give a less
## acurate answer while decreasing run time.

# ------------------------------- COMMANDS ------------------------------------

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/lkersting/mcnpdata/
#CROSS_SECTION_XML_PATH=/home/software/mcnp6.2/MCNP_DATA
FRENSIE=/home/lkersting/frensie

INPUT="1"
if [ "$#" -eq 1 ]; then
    # Set the file type (1 = Native (default), 2 = ACE EPR14, 3 = ACE EPR12)
    INPUT="$1"
fi

# Changing variables

# Source Energy (.001, .01, .1 MeV)
ENERGY=0.001
ENERGY_KEV=$(echo $ENERGY*1000 |bc)
ENERGY_KEV=${ENERGY_KEV%.*}
# Number of threads
THREADS="80"
# Number of histories 1e8
HISTORIES="100000000"
# Geometry package (DagMC or ROOT)
GEOMETRY="DagMC"
# Particle tracker ( true = on, false = off)
PARTICLE="false"
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
DISTRIBUTION="Coupled"
# Elastic coupled sampling method ( Simplified, 1D, 2D )
COUPLED_SAMPLING="2D"


ELEMENT="H"
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

NAME_EXTENTION=""
NAME_REACTION=""
# Set the file name extentions
if [ "${ELASTIC_ON}" = "false" ]; then
    NAME_REACTION="${NAME_REACTION}_no_elastic"
elif [ ${DISTRIBUTION} = "Coupled" ]; then
    NAME_EXTENTION="${NAME_EXTENTION}_${COUPLED_SAMPLING}"
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
EST=$(python est.py -e ${ENERGY} -t ${GEOMETRY} -p ${PARTICLE} 2>&1)
SOURCE=$(python ../point_source.py -e ${ENERGY} 2>&1)
GEOM=$(python geom.py -e ${ENERGY} -t ${GEOMETRY} 2>&1)
RSP="../rsp_fn.xml"

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)

if [ ${NAME} = "ace" ] || [ ${NAME} = "epr14" ]; then
    DIR="results/${NAME}/${TODAY}"
    NAME="h_${ENERGY_KEV}kev_${NAME}${NAME_REACTION}"
else
    DIR="results/${INTERP}/${TODAY}"

    if [ ${SAMPLE} = 1 ]; then
        SAMPLE_NAME="unit_correlated"
    elif [ ${SAMPLE} = 2 ]; then
        SAMPLE_NAME="correlated"
    elif [ ${SAMPLE} = 3 ]; then
        SAMPLE_NAME="unit_base"
    fi

    NAME="h_${ENERGY_KEV}kev_${NAME}_${INTERP}_${SAMPLE_NAME}${NAME_EXTENTION}${NAME_REACTION}"
fi

mkdir -p ${DIR}

if [ "${GEOMETRY}" = "ROOT" ]; then
    NAME="${NAME}_root"
fi

echo "Running Facemc H spheres test with ${HISTORIES} particles on ${THREADS} threads:"
RUN="mpiexec -n ${THREADS} ${FRENSIE}/bin/facemc-mpi --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME}"
echo ${RUN}
${RUN} > ${DIR}/${NAME}.txt 2>&1

echo "Removing old xml files:"
rm ${INFO} ${EST} ${SOURCE} ${MAT} ${GEOM} ../ElementTree_pretty.pyc

echo "Processing the results:"
H5=${NAME}.h5
NEW_NAME="${DIR}/${H5}"
NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"
mv ${H5} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

cd ${DIR}

if [ "${GEOMETRY}" = "ROOT" ]; then
    bash ../../../data_processor_root.sh ${NAME}
else
    bash ../../../data_processor.sh ${NAME}
fi
echo "Results will be in ./${DIR}"