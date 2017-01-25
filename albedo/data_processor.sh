#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test result data processor
##---------------------------------------------------------------------------##

EXTRA_ARGS=$@
TESTING_DIR="/home/lkersting/frensie/frensie-tests"

if [ "$#" -ne 1 ];
then
    echo "The input file is required. $# arguments provided!"
    echo "run:  ./data_processor.sh <file>"
else
    # Set file name
    FILE=$1

    H5="${FILE}.h5"
    TL_FLUX="${FILE}_cell_flux"

    if [ -f $H5 ];
    then
        output=${FILE}_albedo.txt
        # Extract the surface current data
        ${TESTING_DIR}/edump.py -f $H5 -e 1 -i 4 -b Cosine > $output

        output=${TL_FLUX}.txt
        # Extract the surface current data
        ${TESTING_DIR}/edump.py -f $H5 -e 3 -i total -b Energy > $output
    else
       echo "File $H5 does not exist."
    fi
fi
