#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## This script will run the run_hanson_mpi.sh script for several interpolations:
## Log-Log-Log, Lin-Lin-Lin, and Lin-Lin-Log
##---------------------------------------------------------------------------##

# interpolations to run for mpi
interps=( linlinlin linlinlog logloglog )
unit_based=( false true )
# file type (1 = Native, 2 = Moment Preserving, 3 = ACE EPR14, 4 = ACE EPR12)
file_type=1

# loop through interps and run mpi script
for i in "${interps[@]}"
do
    # Change the interp
    command=s/INTERP=.*/INTERP=\"$i\"/
    sed -i $command run_hanson_mpi.sh
    # Set unit based on/off
    for j in "${unit_based[@]}"
    do
        command=s/UNIT_BASED_ON=.*/UNIT_BASED_ON=\"$j\"/
        sed -i $command run_hanson_mpi.sh
        if [ ${i} != linlinlog ] || [ ${j} != false ];
        then
            echo -e "\nRunning Native Analog with "$i" and unit based on = "$j
            sbatch run_hanson_mpi.sh $file_type
        fi
    done
done
