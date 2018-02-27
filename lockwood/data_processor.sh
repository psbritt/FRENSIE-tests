#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test result data processor
##---------------------------------------------------------------------------##

EXTRA_ARGS=$@
TESTING_DIR="/home/lkersting/frensie/frensie-tests"

if [ "$#" -ne 1 ]; then
    echo "The input file is required. $# arguments provided!"
    echo "run:  ./data_processor.sh <file_name minus .h5>"
else
    # Set file name
    FILE=$1

    H5="${FILE}.h5"

    if [ -f $H5 ]; then
        output="${FILE}_energy_dep.txt"
        # Extract the energy deposition
        ${TESTING_DIR}/edump.py -f $H5 -e 1 -i total > ${output}
    else
       echo "File $H5 does not exist."
    fi
fi


