#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test result data processor
##---------------------------------------------------------------------------##

EXTRA_ARGS=$@
TESTING_DIR="/home/lkersting/frensie/tests"

if [ "$#" -ne 1 ];
then
    echo "The input file is required. $# arguments provided!"
    echo "run:  ./data_processor.sh <file_name minus .h5>"
else
    # Set file name
    FILE=$1
    H5="${FILE}.h5"

    # Make a directory for the output files
    FLUX="flux"
    CURRENT="current"
    TRACK_FLUX="track_flux"

    if [ -f $H5 ];
    then
        file=${FLUX}.txt
        # Extract the flux data
        ${TESTING_DIR}/edump.py -f $H5 -e 1 -i 1 -b Energy > $file

        file=${CURRENT}.txt
        # Extract the current data
        ${TESTING_DIR}/edump.py -f $H5 -e 2 -i 1 -b Energy > $file

        file=${TRACK_FLUX}.txt
        # Extract the track length flux data
        ${TESTING_DIR}/edump.py -f $H5 -e 3 -i 1 -b Energy > $file

        plot="${TESTING_DIR}/example/plot.p"
        gnuplot ${plot}
    else
       echo "File $H5 does not exist."
    fi
fi
