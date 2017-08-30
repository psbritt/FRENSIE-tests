#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## This script will run the run_hanson_mpi.sh script for several interpolations:
## Log-Log-Log, Lin-Lin-Lin, and Lin-Lin-Log
##---------------------------------------------------------------------------##

# interpolations to run for mpi
interps=( logloglog linlinlin linlinlog )

# file type (1 = ACE, 2 = Native, 3 = Moment Preserving)
file_type=2

# loop through interps and run mpi script
for i in "${interps[@]}"
do
    command=s/INTERP=.*/INTERP=\"$i\"/
    sed -i $command run_hanson_mpi.sh
    sbatch run_hanson_mpi.sh $file_type
done
