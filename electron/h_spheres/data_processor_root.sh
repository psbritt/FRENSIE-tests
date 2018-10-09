#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test result data processor
##---------------------------------------------------------------------------##

EXTRA_ARGS=$@
TESTING_DIR="/home/lkersting/frensie/tests/electron"

if [ "$#" -ne 1 ]; then
    echo "The input file is required. $# arguments provided!"
    echo "run:  ./data_processor_root.sh <file_name minus .h5>"
else
    # Set file name
    FILE=$1

    H5="${FILE}.h5"
    TRACK_FLUX="${FILE}_track_flux"

    if [ -f $H5 ]; then
        for i in 1 2 3 4 5
        do
            file=${TRACK_FLUX}_${i}.txt
            # Extract the flux data
            ${TESTING_DIR}/edump.py -f $H5 -e 1 -i ${i} -b Energy > $file
        done

        plot="${TESTING_DIR}/h_spheres/plot_root.p"
        gnuplot -e "filename='${FILE}'" $plot

    else
       echo "File $H5 does not exist."
    fi
fi
