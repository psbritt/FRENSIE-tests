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
sample_policy=( correlated exact )
# file type (1 = Native, 2 = ACE EPR14, 3 = ACE EPR12)
file_type=1

# loop through interps and run mpi script
for i in "${interps[@]}"
do
    # Change the interp
    command=s/INTERP=.*/INTERP=\"$i\"/
    sed -i $command run_hanson_mpi.sh
    # Set 2D sampling policy
    for j in "${sample_policy[@]}"
    do
        command=s/SAMPLE=.*/SAMPLE=\"$j\"/
        sed -i $command run_hanson_mpi.sh
        if [ ${i} != linlinlog ] || [ ${j} != exact ];
        then
            echo -e "\nRunning Native Analog with "$i" "$j" Sampling!"
            sbatch run_hanson_mpi.sh $file_type
        fi
    done
done
