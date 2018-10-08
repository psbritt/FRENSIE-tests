#!/bin/bash
##---------------------------------------------------------------------------##
## MCNP6.2 multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and the Lockwood energy deposition data.
## This script will run mcnp several different ranges
##---------------------------------------------------------------------------##


# Set the number of threads
THREADS="8"
if [ "$#" -eq 1 ]; then
    # Set the number of threads used
    THREADS="$1"
fi

# Number of tests for 1.0 MeV
test_number=( 0 1 2 3 4 5 6 7 8 9 )

# loop through test numbers and run mpi script
for i in "${test_number[@]}"
do
    # Change the test number
    line=s/test_number=.*/test_number=\"$i\"/
    sed -i "$line" run_mcnp.sh

     echo -e "\nRunning Lockwood mcnp6.2 ${energy} Test Number $i!"
     bash run_mcnp.sh $file_type ${THREADS}
done
