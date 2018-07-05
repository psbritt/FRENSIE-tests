#!/bin/bash
##---------------------------------------------------------------------------##
## MCNP6 test runner
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
MCNP6_1=/home/software/mcnp6.1.1/bin/mcnp611_linux_x86_64_omp
MCNP6_2=/home/software/mcnp6.2/bin/mcnp6
MCNP=$MCNP6_2

THREADS="8"
if [ "$#" -eq 1 ]; then
    # Set the number of threads used
    THREADS="$1"
fi

ENERGY="10kev"

# Set the input file name
NAME="mcnp.in"
OUTPUT="mcnp."

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)
DIR="./results/mcnp/${TODAY}"
mkdir -p ${DIR}

echo "Running MCNP6.2 H sphere test with ${THREADS} threads:"
RUN="${MCNP} i=${NAME} n=${OUTPUT} tasks ${THREADS}"
echo ${RUN}
${RUN}

echo "Processing the results:"
NEW_NAME=${DIR}${OUTPUT}

# Move output files to test directory
mv ${OUTPUT}o ${NEW_NAME}o
mv ${OUTPUT}r ${NEW_NAME}r
mv ${OUTPUT}m ${NEW_NAME}m

# Process the results
echo "Processing the results:"
python mcnp_data_processor.py -f ${NEW_NAME}o
echo "The processed data is located at: ${DIR}"
