#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/software/mcnpdata/

echo -n "Enter the energy to process in keV (1, 10, 100) > "
read INPUT
ENERGY="${INPUT}kev"
NAME="h_spheres_"

# Set .xml paths.
if [ $INPUT -eq 1 ];
then
    GEOM="${NAME}geom_${ENERGY}.xml"
else
    GEOM="${NAME}geom.xml"
fi

MAT="${NAME}mat.xml"
RSP="${NAME}rsp_fn.xml"
EST="${NAME}est_${ENERGY}.xml"
SOURCE="${NAME}source_${ENERGY}.xml"
NAME="${NAME}${ENERGY}"


echo "Running Facemc:"
../../../../bin/facemc --sim_info=sim_info.xml --geom_def=$GEOM --mat_def=$MAT --resp_def=$RSP --est_def=$EST --src_def=$SOURCE --cross_sec_dir=$CROSS_SECTION_XML_PATH --simulation_name=$NAME --threads=12

echo "Processing the results:"

TODAY=$(date +%Y-%m-%d)
DIR="results/${TODAY}"

echo $INPUT | ./data_processor.sh ${DIR}

