#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## This script will run the run_al_mpi.sh script at several different energies:
## .005 .0093 .01 .011 .0134 .05 .0173 .02 .0252 .03 .04 .0415 .05 .06 .0621
## .0818 and .102 MeV
##---------------------------------------------------------------------------##

# energies to run for mpi
energies=(.005 .0093 .01 .011 .0134 .05 .0173 .02 .0252 .03 .04 .0415 .05 .06 .0621 .0818 .102)

# file type (1 = Native, 2 = EPR14, 3 = ACE)
file_type=1

# loop through energies and run mpi script
for i in "${energies[@]}"
do
    command=s/ENERGY=.*/ENERGY=\"$i\"/
    sed -i $command run_al_mpi.sh
    echo "\nRunning Al Albedo Test at Energy "$i"!"
    sbatch run_al_mpi.sh $file_type
done
