#!/bin/bash
##---------------------------------------------------------------------------##
## MCNP6 test runner
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/software/mcnpdata/

THREADS="8"
if [ "$#" -eq 1 ];
then
    # Set the number of threads used
    THREADS="$1"
fi

echo -n "Enter the energy to process in keV (1, 10, 100) > "
read INPUT
ENERGY="${INPUT}kev"
echo "You entered: $ENERGY"

# Set the input file name
NAME="h_spheres_${ENERGY}.inp"

echo "Running MCNP6 with ${THREADS} threads:"
/home/software/mcnp6.1.1/bin/mcnp611_linux_x86_64_omp n="$NAME" tasks ${THREADS}

echo "Processing the results:"

TODAY=$(date +%Y-%m-%d)
DIR="./results/${TODAY}/"

NEW_NAME=${DIR}${NAME}

# Move output files to test directory
mkdir -p $DIR
mv ${NAME}o ${NEW_NAME}o
mv ${NAME}r ${NEW_NAME}r
mv ${NAME}m ${NEW_NAME}m

# Move to output directory
cd ${DIR}

echo $INPUT | ../../data_processor.py -d ./
echo "The processed data is located at: ${DIR}"
