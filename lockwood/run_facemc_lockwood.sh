#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
##---------------------------------------------------------------------------##
## FRENSIE benchmark test: Lockwood dose depth data.
## The dose depth for several ranges and material is calculated by dividing the
## energy deposition by the calorimeter thickness (g/cm^2).
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

# Changing variables

# Al: 0.314 MeV & tests 0-11, 0.512 MeV & test 0-16, 1.033 MeV & tests 0-24
ELEMENT="Al"; ENERGY="0.314"; TEST_NUMBER="0"

# Number of histories
HISTORIES="100000"
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

# ROOT or DagMC
GEOM_TYPE="DagMC"

NAME="native"
NO_ERRORS="true"

if [ "${ELEMENT}" == "Al" ]; then
    calorimeter_thickness=5.050E-03

    if [ ${ENERGY} == 0.314 ]; then
        # ranges for 0.314 MeV source (g/cm2)
        ranges=( 0.0025 0.0094 0.0181 0.0255 0.0336 0.0403 0.0477 0.0566 0.0654 0.0721 0.0810 0.0993 )
    elif [ ${ENERGY} == 0.521 ]; then
        # ranges for 0.521 MeV source (g/cm2)
        ranges=( 0.0025 0.0094 0.0180 0.0255 0.0335 0.0405 0.0475 0.0566 0.0653 0.0721 0.0807 0.0992 0.1111 0.1259 0.1439 0.1596 0.1825 0.2125 )
    elif [ ${ENERGY} == 1.033 ]; then
        # ranges for 1.033 MeV source (g/cm2)
        ranges=( 0.0025 0.0094 0.0180 0.0255 0.0336 0.0402 0.0476 0.0562 0.0654 0.0723 0.0808 0.0990 0.1110 0.1257 0.1440 0.1593 0.1821 0.2122 0.2225 0.2452 0.2521 0.2908 0.3141 0.3533 0.4188 0.4814 )
    else
        NO_ERRORS="false"
        echo "Error: Energy ${ENERGY} is currently not supported!"
    fi
else
    NO_ERRORS="false"
    echo "Error: Element ${ELEMENT} is currently not supported!"
fi

# Path to geometry file
if [ "${GEOM_TYPE}" == "DagMC" ]; then
    GEOM_PATH="${FRENSIE}/frensie-tests/lockwood/${ELEMENT}/${ELEMENT}_${ENERGY}/dagmc/geom_${TEST_NUMBER}.sat"
elif [ "${GEOM_TYPE}" == "ROOT" ]; then
    GEOM_PATH="${FRENSIE}/frensie-tests/lockwood/${ELEMENT}/${ELEMENT}_${ENERGY}/root/geom_${TEST_NUMBER}.root"
else
    NO_ERRORS="false"
    echo "Error: geometry type \"${GEOM_TYPE}\" is not supported!"
fi

if [ "${NO_ERRORS}" = "true" ]; then

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
        DIR="${ELEMENT}/results/testrun/${NAME}"
        NAME="lockwood_${ENERGY}_${TEST_NUMBER}_${NAME}${NAME_REACTION}"
    else
        DIR="${ELEMENT}/results/testrun/${INTERP}"

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

        NAME="lockwood_${ENERGY}_${TEST_NUMBER}_${INTERP}_${SAMPLE_NAME}${NAME_EXTENTION}${NAME_REACTION}"
    fi

    mkdir -p ${DIR}

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

    python data_processor.py -f ${NEW_NAME} -r ${ranges[${TEST_NUMBER}]} -t ${calorimeter_thickness}
    echo "Results will be in ./${DIR}"
else
    echo "Errors have occured. Facemc was not run!"
fi