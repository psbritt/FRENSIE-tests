#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## This script will run the run_al_mpi.sh script at several different energies:
## .0093, .011, .0134, .0173, .0252, .0415, .0621, .0818 and .102 MeV
##---------------------------------------------------------------------------##

# energies to run for mpi
energies=( .0093 .011 .0134 .0173 .0252 .0415 .0621 .0818 .102 )

# file type (1 = Native, 2 = EPR14, 3 = ACE)
file_type=1

# loop through energies and run mpi script
for i in "${energies[@]}"
do
    command=s/ENERGY=.*/ENERGY=\"$i\"/
    sed -i $command run_al_mpi.sh
    sbatch run_al_mpi.sh $file_type
done
