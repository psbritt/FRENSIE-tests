#!/bin/bash
##---------------------------------------------------------------------------##
## MCNP6 test runner
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
MCNP6_1=/home/software/mcnp6.1.1/bin/mcnp611_linux_x86_64_omp
MCNP6_2=/home/software/mcnp6.2/MCNP_CODE/bin/mcnp6
MCNP=$MCNP6_2

THREADS="8"
if [ "$#" -eq 1 ]; then
    # Set the number of threads used
    THREADS="$1"
fi

# Turn on Condensed History mode (true/false)
CONDENSED_HISTORY_ON="false"

# Set the input file name
NAME="mcnp.in"
OUTPUT="mcnp."
if [ "${CONDENSED_HISTORY_ON}" = "true" ]; then
    NAME="mcnp_ch.in"
    OUTPUT="mcnp_ch."
fi

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)
DIR="./results/mcnp/${TODAY}"
mkdir -p ${DIR}

echo "Running MCNP6.2 with ${THREADS} threads:"
echo "${MCNP} i=${NAME} n=${OUTPUT} tasks ${THREADS}"
${MCNP} i=${NAME} n=${OUTPUT} tasks ${THREADS}

NEW_NAME="${DIR}/${OUTPUT}"

# Move output files to test directory
mv ${OUTPUT}o ${NEW_NAME}o
mv ${OUTPUT}r ${NEW_NAME}r
mv ${OUTPUT}m ${NEW_NAME}m

echo "Processing the results:"
python mcnp_data_processor.py -f ${NEW_NAME}o
echo "The processed data is located at: ${DIR}"
