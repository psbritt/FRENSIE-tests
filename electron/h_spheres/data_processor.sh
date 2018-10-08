#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test result data processor
##---------------------------------------------------------------------------##

EXTRA_ARGS=$@
TESTING_DIR="/home/lkersting/frensie/tests"

if [ "$#" -ne 1 ]; then
    echo "The input file is required. $# arguments provided!"
    echo "run:  ./data_processor.sh <file_name minus .h5>"
else
    # Set file name
    FILE=$1
    H5="${FILE}.h5"

    # Make a directory for the output files
    mkdir -p ${FILE}
    FLUX="${FILE}/flux"
    CURRENT="${FILE}/current"
    TRACK_FLUX="${FILE}/track_flux"

    if [ -f $H5 ]; then
        for i in 1 3 6 9 12
        do
            file=${FLUX}_${i}.txt
            # Extract the flux data
            ${TESTING_DIR}/edump.py -f $H5 -e 1 -i ${i} -b Energy > $file

            file=${CURRENT}_${i}.txt
            # Extract the current data
            ${TESTING_DIR}/edump.py -f $H5 -e 2 -i ${i} -b Energy > $file
        done

        for i in 3 6 9 12 13
        do
            file=${TRACK_FLUX}_${i}.txt
            # Extract the track length flux data
            ${TESTING_DIR}/edump.py -f $H5 -e 3 -i ${i} -b Energy > $file
        done

        cd ${FILE}
        plot="${TESTING_DIR}/h_spheres/plot.p"
        gnuplot ${plot}
    else
       echo "File $H5 does not exist."
    fi
fi
