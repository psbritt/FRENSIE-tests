#!/bin/sh
# This file is named run_facemc_mpi.sh
#SBATCH --partition=univ2                # Use the newer infrastructure
#SBATCH --time=0-12:00:00
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=20
#SBATCH --mem-per-cpu=4000

# ------------------------------- COMMANDS ------------------------------------

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/ecmartin3/software/mcnpdata/
FRENSIE=/home/lkersting/frensie

THREADS="100"
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

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)
DIR="results/${TODAY}"
mkdir -p $DIR

echo "Running Facemc with ${THREADS} threads:"
mpiexec -n ${THREADS} ${FRENSIE}/bin/facemc --sim_info=sim_info.xml --geom_def=${GEOM} --mat_def=${MAT} --resp_def=$RSP --est_def=$EST --src_def=$SOURCE --cross_sec_dir=$CROSS_SECTION_XML_PATH --simulation_name=$NAME > ${DIR}/${NAME}.txt 2>&1

#echo "Processing the results:"

# Move file to the test results folder
#NAME=${NAME}.h5
#NEW_NAME="${DIR}/${NAME}"
#NEW_RUN_INFO="${DIR}/continue_run_${ENERGY}.xml"

#mv ${NAME} ${NEW_NAME}
#mv continue_run.xml ${NEW_RUN_INFO}

#cd ${DIR}

#echo $INPUT | ../../data_processor.sh ./
