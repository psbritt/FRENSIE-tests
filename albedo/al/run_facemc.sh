#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## The electron albedo is found for a semi-infinite aluminum slab. Since the
## electron albedo requires a surface current, DagMC will be used and not Root.
## FRENSIE will be run with three variations. 1. Using ACE data, which should
## match MCNP almost exactly. 2. Using the Native data in analog mode, whcih 
## uses a different interpolation scheme than MCNP. 3. Using Native data in 
## moment preserving mode, which should give a less acurate answer while
## decreasing run time.
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/software/mcnpdata/
FRENSIE=/home/lkersting/research/frensie-repos/lkersting
#FRENSIE=/home/lkersting/frensie

THREADS="12"
if [ "$#" -eq 1 ];
then
    # Set the number of threads used
    THREADS="$1"
fi

NAME="ace"
ELEMENT="Al"
ENERGY="0.005"
ENERGY_EV=$(echo $ENERGY*1000000 |bc)
ENERGY_EV=${ENERGY_EV%.*}

echo -n "Enter the desired data type (1 = ACE, 2 = Native, 3 = Moment Preserving) > "
read INPUT
if [ ${INPUT} -eq 1 ]
then
    # Use ACE data
    NAME="ace"
    python mat.py -n ${ELEMENT} -t ${NAME}
    MAT="mat_ace.xml"

    python sim_info.py -e ${ENERGY} -c 1.0
    INFO="sim_info.xml"
    echo "Using ACE data!"
elif [ ${INPUT} -eq 2 ]
then
    # Use Native analog data
    NAME="native"
    python mat.py -n ${ELEMENT} -t ${NAME}
    MAT="mat.xml"

    python sim_info.py -e ${ENERGY} -c 1.0
    INFO="sim_info.xml"
    echo "Using Native analog data!"
elif [ ${INPUT} -eq 3 ]
then
    # Use Native Moment Preserving data
    NAME="moments"
    python mat.py -n ${ELEMENT} -t "native"
    MAT="mat.xml"

    python sim_info.py -e ${ENERGY} -c 0.9
    INFO="sim_info.xml"
    echo "Using Native Moment Preserving data!"
else
    # Default to ACE data
    echo "Input not valid, ACE data will be used!"
    python mat.py -n ${ELEMENT} -t ${NAME}
    MAT="mat_ace.xml"

    python sim_info.py -e ${ENERGY} -c 1.0
    INFO="sim_info.xml"
fi

# .xml file paths.
python ../est.py -e ${ENERGY}
EST="../est.xml"
python source.py -e ${ENERGY}
SOURCE="source.xml"
GEOM="geom.xml"
RSP="../rsp_fn.xml"
NAME="al_${NAME}_${ENERGY_EV}"

TODAY=$(date +%Y-%m-%d)
DIR="results/${TODAY}"
mkdir -p $DIR

echo "Running Facemc with ${THREADS} threads:"
${FRENSIE}/bin/facemc --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=$RSP --est_def=$EST --src_def=$SOURCE --cross_sec_dir=$CROSS_SECTION_XML_PATH --simulation_name=$NAME --threads=${THREADS} > ${DIR}/${NAME}.txt 2>&1

echo "Processing the results:"

H5=${NAME}.h5
NEW_NAME="${DIR}/${H5}"
NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"
mv ${H5} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

cd ${DIR}

bash ../../../data_processor.sh ${NAME}
echo "Results will be in ./${DIR}"

