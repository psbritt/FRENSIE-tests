#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test result data processor
##---------------------------------------------------------------------------##

EXTRA_ARGS=$@

echo -n "Enter the energy to process in keV (1, 10, 100) > "
read ENERGY
ENERGY="${ENERGY}kev"
echo "You entered: $ENERGY"

# Set cross_section.xml directory path.
TODAY=$(date +%Y-%m-%d)
DIR="results/${TODAY}"
echo "Files will be located in $DIR"
mkdir -p $DIR

H5="h_spheres_${ENERGY}.h5"
FLUX_ENERGY_BINS="results/${TODAY}/${ENERGY}_flux_bins.txt"
CURRENT_ENERGY_BINS="results/${TODAY}/${ENERGY}_current_bins.txt"
FLUX="results/${TODAY}/${ENERGY}_flux"
CURRENT="results/${TODAY}/${ENERGY}_current"

if [ -f $H5 ];
then
    # Extract the energy bins
    ./edump.py -f $H5 -e 1 -i Energy > $FLUX_ENERGY_BINS
    ./edump.py -f $H5 -e 2 -i Energy > $CURRENT_ENERGY_BINS

    for i in 1 3 6 9 12
    do
        tmp=${ENERGY}_${i}_tmp1.txt
        tmp2=${ENERGY}_${i}_tmp2.txt

        file=${FLUX}_${i}.txt
        # Extract the flux data
        ./edump.py -f $H5 -e 1 -i ${i} > $tmp
        sed '1a\0.0 0.0' $tmp > $tmp2
        # Paste the energy bins to the flux data
        paste -d " " $FLUX_ENERGY_BINS $tmp2 > $file

        file=${CURRENT}_${i}.txt
        # Extract the current data
        ./edump.py -f $H5 -e 2 -i ${i} > $tmp
        sed '1a\0.0 0.0' $tmp > $tmp2
        # Paste the energy bins to the flux data
        paste -d " " $CURRENT_ENERGY_BINS $tmp2 > $file

        rm $tmp $tmp2
    done

    rm $FLUX_ENERGY_BINS $CURRENT_ENERGY_BINS

    DATE=$(date +%b%d)
    NEW_NAME="../../../results/facemc/h_spheres_${ENERGY}_${DATE}.h5"

    NEW_RUN_INFO="continue_run_${ENERGY}_${DATE}.xml"
    mv $H5 $NEW_NAME
    mv continue_run.xml $NEW_RUN_INFO

    cd $DIR
    plot="../../plot_${ENERGY}.p"
    gnuplot $plot

else
   echo "File $H5 does not exist."
fi

