#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/software/mcnpdata/
#FRENSIE=/home/lkersting/frensie
FRENSIE=/home/lkersting/research/frensie-repos/lkersting

THREADS="12"
if [ "$#" -eq 1 ];
then
    # Set the number of threads used
    THREADS="$1"
fi

echo -n "Enter the energy to process in keV (1, 10, 100) > "
read INPUT
ENERGY="${INPUT}kev"
echo "You entered: $ENERGY"

NAME="h_spheres_"

# .xml directory paths.
GEOM="${NAME}geom_${ENERGY}.xml"
MAT="${NAME}mat.xml"
RSP="${NAME}rsp_fn.xml"
EST="${NAME}est_${ENERGY}.xml"
SOURCE="${NAME}source_${ENERGY}.xml"
NAME="${NAME}${ENERGY}"


echo "Running Facemc with ${THREADS} threads:"
${FRENSIE}/bin/facemc --sim_info=sim_info.xml --geom_def=${GEOM} --mat_def=${MAT} --resp_def=$RSP --est_def=$EST --src_def=$SOURCE --cross_sec_dir=$CROSS_SECTION_XML_PATH --simulation_name=$NAME --threads=${THREADS}

echo "Processing the results:"

TODAY=$(date +%Y-%m-%d)
DIR="results/${TODAY}"
NAME=${NAME}.h5
NEW_NAME="${DIR}/${NAME}"
NEW_RUN_INFO="${DIR}/continue_run_${ENERGY}.xml"
mkdir -p $DIR
mv ${NAME} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

cd ${DIR}

echo $INPUT | ../../data_processor.sh ./
echo "Results will be in ./${DIR}"

