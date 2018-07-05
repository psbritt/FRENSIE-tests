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
FILE="mcnp.in"
NAME="mcnp"

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)
DIR="./results/mcnp/${TODAY}"
mkdir -p $DIR

echo "Running MCNP6.2 H sphere test with ${THREADS} threads:"
RUN="${MCNP} n="${FILE}" tasks ${THREADS}"
echo ${RUN}
${RUN} > ${DIR}/${NAME}.txt

echo "Processing the results:"
NEW_NAME="${DIR}/${NAME}"

# Move output files to test directory
mv ${FILE}o ${NEW_NAME}.o
mv ${FILE}r ${NEW_NAME}.r
mv ${FILE}m ${NEW_NAME}.m

# Process the files
python ./data_processor_mcnp.py -f ${NEW_NAME}.o
echo "The processed data is located at: ${DIR}"
