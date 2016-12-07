#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test result data processor
##---------------------------------------------------------------------------##

EXTRA_ARGS=$@
TESTING_DIR="/home/lkersting/frensie/frensie-tests"

if [ "$#" -lt 1 ];
then
    echo "The output directory is required. $# arguments provided!"
    echo "run:  ./data_processor.sh <directory>"
else
    echo -n "Enter the energy to process in keV (1, 10, 100) > "
    read ENERGY
    ENERGY="${ENERGY}kev"
    echo "You entered: $ENERGY"

    # Set cross_section.xml directory path.
    DIR=$1
    mkdir -p $DIR

    NAME_EXTENSION=$2
    H5="h_spheres_${ENERGY}${NAME_EXTENSION}.h5"
    FLUX="${DIR}/${ENERGY}_flux"
    CURRENT="${DIR}/${ENERGY}_current"
    TRACK_FLUX="${DIR}/${ENERGY}_track_flux"

    if [ -f $H5 ];
    then
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

        cd $DIR
        plot="${TESTING_DIR}/h_spheres/dagmc/plot_${ENERGY}.p"
        gnuplot ${plot}

    else
       echo "File $H5 does not exist."
    fi
fi
