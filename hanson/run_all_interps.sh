#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## This script will run the hanson.sh script for several interpolations:
## Log-Log-Log, Lin-Lin-Lin, and Lin-Lin-Log
##---------------------------------------------------------------------------##

# interpolations to run for mpi
interps=( LINLINLIN LINLINLOG LOGLOGLOG )
# Set 2D Grid Policy ( CORRELATED UNIT_BASE UNIT_BASE_CORRELATED )
grid_policy=( CORRELATED UNIT_BASE UNIT_BASE_CORRELATED )
# file type (Native, ACE)
file_type=ACE
# elastic distribution mode ( DECOUPLED, COUPLED, HYBRID )
mode=COUPLED
# elastic coupled sampling method ( TWO_D, ONE_D, MODIFIED_TWO_D )
method=TWO_D

# Set the file type
command=s/file_type=Data.ElectroatomicDataProperties.*/file_type=Data.ElectroatomicDataProperties.${file_type}_EPR_FILE/
sed -i $command hanson.py
# Set the elastic distribution mode
command=s/mode=MonteCarlo.*/mode=MonteCarlo.${mode}_DISTRIBUTION/
sed -i $command hanson.py
# Set the elastic coupled sampling method
command=s/method=MonteCarlo.*/method=MonteCarlo.${method}_UNION/
sed -i $command hanson.py

# loop through interps and run mpi script
for i in "${interps[@]}"
do
    # Change the interp
    command=s/interpolation=MonteCarlo.*/interpolation=MonteCarlo.${i}_INTERPOLATION/
    sed -i $command hanson.py
    # Set 2D grid policy
    for j in "${grid_policy[@]}"
    do
        command=s/grid_policy=MonteCarlo.*/grid_policy=MonteCarlo.${j}_GRID/
        sed -i $command hanson.py
        if [ ${i} != LINLINLOG ] || [ ${j} != ACE_EPR_FILE ]; then
            echo -e "\nRunning Native Analog with "$i" "$j" Sampling!"
            # sbatch hanson.sh
        fi
    done
done
