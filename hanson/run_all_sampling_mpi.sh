#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## This script will run the run_hanson_mpi.sh script for several interpolations:
## Decoupled, 2D Coupled, 1D Coupled , and Simplified Coupled
##---------------------------------------------------------------------------##

# interpolations to run for mpi
sample_methods=( 2D 1D Simplified )
interp=( correlated exact )
# file type (1 = Native, 2 = ACE EPR14, 3 = ACE EPR12)
file_type=1

# Change the distribution to Decoupled
command=s/DISTRIBUTION=.*/DISTRIBUTION=\"Decoupled\"/
sed -i $command run_hanson_mpi.sh
echo -e "\nRunning Native Analog with Elastic Decoupled Sampling!"
sbatch run_hanson_mpi.sh $file_type

# loop through interps and run mpi script
for i in "${sample_methods[@]}"
do
    # Change the distribution to Coupled
    command=s/DISTRIBUTION=.*/DISTRIBUTION=\"Coupled\"/
    sed -i $command run_hanson_mpi.sh
    # Set the coupled sampling method
    command=s/COUPLED_SAMPLING=.*/COUPLED_SAMPLING=\"$i\"/
    sed -i $command run_hanson_mpi.sh
    echo -e "\nRunning Native Analog with Elastic "$i" Coupled Sampling!"
    sbatch run_hanson_mpi.sh $file_type
done
