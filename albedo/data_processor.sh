#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test result data processor
##---------------------------------------------------------------------------##

EXTRA_ARGS=$@
TESTING_DIR="/home/lkersting/frensie/frensie-tests"

if [ "$#" -ne 2 ]; then
    echo "The energy and input file are required. $# arguments provided!"
    echo "run:  ./data_processor.sh <energy> <file>"
else
    # Set Energy
    Energy_MeV=$1
    # Set file name
    FILE=$2


    H5="${FILE}.h5"
    TL_FLUX="${FILE}_cell_flux"

    if [ -f $H5 ]; then
        output=${FILE}_albedo.txt
        # Extract the surface current data
        ${TESTING_DIR}/edump.py -f $H5 -e 1 -i 4 -b Cosine > $output
        # Remove extra data and add energy
        sed -i '1s/.*/# Energy (keV)\tAlbedo\tError/' $output
        sed -i '2,4d' $output
        REPLACE="2s/1.0/$Energy_MeV/"
        sed -i $REPLACE $output

        output=${TL_FLUX}.txt
        # Extract the surface current data
        ${TESTING_DIR}/edump.py -f $H5 -e 3 -i total -b Energy > $output
    else
       echo "File $H5 does not exist."
    fi
fi
