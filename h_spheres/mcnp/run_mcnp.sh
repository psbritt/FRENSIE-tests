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

# Set cross_section.xml directory path.
NAME="h_spheres_${ENERGY}.inp"

echo "Running MCNP6:"
/home/software/mcnp6.1.1/bin/mcnp611_linux_x86_64_omp n="$NAME" tasks ${THREADS}

echo "Processing the results:"
echo $INPUT | ./data_processor.py -d ${OUTPUT_DIR}
echo "The processed data is located at: ${directory}"
