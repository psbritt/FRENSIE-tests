#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs using the Lockwood energy deposition data
## This script will run the run_lockwood_mpi.sh script for all test numbers:
## 0 - 11
##---------------------------------------------------------------------------##

# interpolations to run for mpi
test_number=( 0 1 2 3 4 5 6 7 8 9 10 11 )
# file type (1 = Native, 2 = ACE EPR14, 3 = ACE EPR12)
file_type=1

# loop through test numbers and run mpi script
for i in "${test_number[@]}"
do
    # Change the interp
    command=s/TEST_NUMBER=.*/TEST_NUMBER=\"$i\"/
    sed -i $command run_lockwood_mpi.sh

     echo -e "\nRunning Lockwood Test Number $i!"
     sbatch run_lockwood_mpi.sh $file_type
done
