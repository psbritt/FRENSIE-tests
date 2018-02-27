#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
##---------------------------------------------------------------------------##
## FRENSIE benchmark test: Lockwood dose depth data.
## The dose depth for several ranges and material is calculated by dividing the
## energy deposition by the range (g/cm^2).
## FRENSIE will be run with three variations.
## 1. Using the Native data in analog mode, whcih uses a different interpolation
## scheme than MCNP.
## 2. Using Native data in moment preserving mode, which should give a less
## acurate answer while decreasing run time.
## 3. Using ACE (EPR14) data, which should match MCNP6.2 almost exactly.
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
#CROSS_SECTION_XML_PATH=/home/lkersting/mcnpdata/
CROSS_SECTION_XML_PATH=/home/software/mcnp6.2/MCNP_DATA
FRENSIE=/home/lkersting/frensie

THREADS="12"
if [ "$#" -eq 1 ]; then
    # Set the number of threads used
    THREADS="$1"
fi

ELEMENT="Al"
ENERGY="0.314"
TEST_NUMBER="2"

# Changing variables
# Number of histories
HISTORIES="10"
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
COUPLED_SAMPLING="Simplified"

# ROOT or DagMC (currently no DagMC option)
GEOM_PATH="${FRENSIE}/frensie-tests/lockwood/${ELEMENT}_${ENERGY}/geom_${TEST_NUMBER}.root"
GEOM_TYPE="ROOT"

NAME="native"

ELASTIC="-d ${DISTRIBUTION} -c ${COUPLED_SAMPLING}"
REACTIONS="-t ${ELASTIC_ON} -b ${BREM_ON} -i ${IONIZATION_ON} -a ${EXCITATION_ON}"
SIM_PARAMETERS="-e ${ENERGY} -n ${HISTORIES} -s ${SAMPLE} -l ${INTERP} ${REACTIONS} ${ELASTIC}"

echo -n "Enter the desired data type (1 = Native, 2 = ACE EPR14, 3 = ACE EPR12) > "
read INPUT
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
SOURCE=$(python ./source.py -e ${ENERGY} 2>&1)
EST="est.xml"
GEOM=$(python ./geom.py -t ${GEOM_TYPE} -f ${GEOM_PATH} 2>&1)
RSP="../rsp_fn.xml"

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)

if [ ${NAME} = "ace" -o ${NAME} = "epr14" ]; then
    DIR="results/testrun/${NAME}"
    NAME="lockwood_${ENERGY}_${NAME}${NAME_REACTION}"
else
    DIR="results/testrun/${INTERP}"

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

    NAME="lockwood_${ENERGY}_${INTERP}_${SAMPLE_NAME}${NAME_EXTENTION}${NAME_REACTION}"
fi

mkdir -p $DIR

echo "Running Facemc Hanson test with ${HISTORIES} particles on ${THREADS} threads:"
RUN="${FRENSIE}/bin/facemc --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME} --threads=${THREADS}"
echo ${RUN}

#gdb --args ${RUN}
#valgrind --tool=memcheck --leak-check=yes ${RUN}
${RUN}

echo "Removing old xml files:"
rm ${INFO} ${MAT} ${SOURCE} ${GEOM} ../ElementTree_pretty.pyc

echo "Processing the results:"
H5=${NAME}.h5
NEW_NAME="${DIR}/${H5}"
NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"
mv ${H5} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

# cd ${DIR}

bash ../../../data_processor.sh ${NAME}
echo "Results will be in ./${DIR}"
