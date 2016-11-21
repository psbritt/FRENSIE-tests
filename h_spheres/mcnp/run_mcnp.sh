#!/bin/bash
##---------------------------------------------------------------------------##
## MCNP6 test runner
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/software/mcnpdata/
TODAY=$(date +%Y-%m-%d)
OUTPUT_DIR="./results/${TODAY}/"

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

echo "Running MCNP6:"
/home/software/mcnp6.1.1/bin/mcnp611_linux_x86_64_omp n="$NAME" tasks ${THREADS}

NEW_NAME=${OUTPUT_DIR}${NAME}

# Move output files to test directory
mv ${NAME}o ${NEW_NAME}o
mv ${NAME}r ${NEW_NAME}r
mv ${NAME}m ${NEW_NAME}m

# Move to output directory
cd ${OUTPUT_DIR}

echo "Processing the results:"
echo $INPUT | ./data_processor.py -d ./
echo "The processed data is located at: ${OUTPUT_DIR}"
