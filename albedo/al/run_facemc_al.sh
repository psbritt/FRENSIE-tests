#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
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
## 3. Using ACE (EPR12) data, which should match MCNP6.1 almost exactly.
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/software/mcnpdata/
#CROSS_SECTION_XML_PATH=/home/ecmartin3/software/mcnpdata/
#FRENSIE=/home/lkersting/research/frensie-repos/lkersting
FRENSIE=/home/lkersting/frensie

THREADS="12"
if [ "$#" -eq 1 ];
then
    # Set the number of threads used
    THREADS="$1"
fi

# Changing variables
ENERGY=".015"
ELEMENT="Al"
# Number of histories
HISTORIES="10"
# Turn certain reactions on (true/false)
ELASTIC_ON="true"
BREM_ON="true"
IONIZATION_ON="true"
EXCITATION_ON="true"
# Turn certain electron properties on (true/false)
INTERP="logloglog"
CORRELATED_ON="true"
UNIT_BASED_ON="true"

REACTIONS=" -t ${ELASTIC_ON} -b ${BREM_ON} -i ${IONIZATION_ON} -a ${EXCITATION_ON}"
SIM_PARAMETERS="-e ${ENERGY} -n ${HISTORIES} -l ${INTERP} -s ${CORRELATED_ON} -u ${UNIT_BASED_ON} ${REACTIONS}"
ENERGY_EV=$(echo $ENERGY*1000000 |bc)
ENERGY_EV=${ENERGY_EV%.*}
NAME="native"

echo -n "Enter the desired data type (1 = Native, 2 = Moment Preserving, 3 = ACE EPR14, 4 = ACE EPR12) > "
read INPUT
if [ ${INPUT} -eq 1 ]
then
    # Use Native analog data
    NAME="native"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 1.0"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP}
    INFO="sim_info_${ENERGY}_1.0"
    MAT="mat_${ELEMENT}_${NAME}_${INTERP}.xml"
    echo "Using Native analog data!"
elif [ ${INPUT} -eq 2 ]
then
    # Use Native Moment Preserving data
    NAME="moments"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 0.9"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t "native" -i ${INTERP}
    INFO="sim_info_${ENERGY}_0.9"
    MAT="mat_${ELEMENT}_native_${INTERP}.xml"
    echo "Using Native Moment Preserving data!"
elif [ ${INPUT} -eq 3 ]
then
    # Use ACE EPR14 data
    CROSS_SECTION_XML_PATH=/home/software/mcnp6.2/MCNP_DATA
    NAME="epr14"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 1.0"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP}
    INFO="sim_info_${ENERGY}_1.0"
    MAT="mat_${ELEMENT}_${NAME}_${INTERP}.xml"
    echo "Using ACE data!"
elif [ ${INPUT} -eq 4 ]
then
    # Use ACE EPR12 data
    NAME="ace"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 1.0"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP}
    INFO="sim_info_${ENERGY}_1.0"
    MAT="mat_${ELEMENT}_${NAME}_${INTERP}.xml"
    echo "Using ACE data!"
else
    # Default to Native data
    NAME="native"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 1.0"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP}
    INFO="sim_info_${ENERGY}_1.0"
    MAT="mat_${ELEMENT}_${NAME}_${INTERP}.xml"
    echo "Input not valid, Native data will be used!"
fi

NAME_EXTENTION=""
# Set the sim info xml file name
if [ "${CORRELATED_ON}" = "false" ]
then
    NAME_EXTENTION="${NAME_EXTENTION}_stochastic"
fi
if [ "${UNIT_BASED_ON}" = "false" ]
then
    NAME_EXTENTION="${NAME_EXTENTION}_exact"
fi

NAME_REACTION=""
if [ "${ELASTIC_ON}" = "false" ]
then
    NAME_REACTION="${NAME_REACTION}_no_elastic"
fi
if [ "${BREM_ON}" = "false" ]
then
    NAME_REACTION="${NAME_REACTION}_no_brem"
fi
if [ "${IONIZATION_ON}" = "false" ]
then
    NAME_REACTION="${NAME_REACTION}_no_ionization"
fi
if [ "${EXCITATION_ON}" = "false" ]
then
    NAME_REACTION="${NAME_REACTION}_no_excitation"
fi
INFO="${INFO}_${INTERP}${NAME_EXTENTION}${NAME_REACTION}.xml"

# .xml file paths.
python ../est.py -e ${ENERGY}
python source.py -e ${ENERGY}
EST="../est_${ENERGY}.xml"
SOURCE="source_${ENERGY}.xml"
GEOM="geom.xml"
RSP="../rsp_fn.xml"

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)

if [ ${NAME} = "ace" -o ${NAME} = "epr14" ]
then
    DIR="results/testrun/${NAME}"
    NAME="al_${NAME}_${ENERGY_EV}${NAME_REACTION}"
else
    DIR="results/testrun/${INTERP}"
    NAME="al_${NAME}_${ENERGY_EV}_${INTERP}${NAME_EXTENTION}${NAME_REACTION}"
fi

mkdir -p $DIR

echo "Running Facemc Albedo test with ${HISTORIES} particles on ${THREADS} threads:"
RUN="${FRENSIE}/bin/facemc --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=$RSP --est_def=$EST --src_def=$SOURCE --cross_sec_dir=$CROSS_SECTION_XML_PATH --simulation_name=$NAME --threads=${THREADS}"
echo ${RUN}
${RUN} > ${DIR}/${NAME}.txt #2>&1

echo "Removing old xml files:"
rm ${INFO} ${EST} ${SOURCE} ${MAT} ElementTree_pretty.pyc

echo "Processing the results:"
H5=${NAME}.h5
NEW_NAME="${DIR}/${H5}"
NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"
mv ${H5} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

cd ${DIR}

bash ../../../data_processor.sh ${NAME}
echo "Results will be in ./${DIR}"

