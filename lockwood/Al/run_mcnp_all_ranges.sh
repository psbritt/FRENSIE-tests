#!/bin/bash
##---------------------------------------------------------------------------##
## MCNP6.2 multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and the Lockwood energy deposition data.
## This script will run mcnp several different ranges depending on the energy:
## .0093, .011, .0134, .0173, .0252, .0415, .0621, .0818 and .102 MeV
##---------------------------------------------------------------------------##


# Set the number of threads
THREADS="8"
if [ "$#" -eq 1 ]; then
    # Set the number of threads used
    THREADS="$1"
fi

# Energy (0.314, 0.521, 1.033) MeV
energy="0.314"

if [ ${energy} == 0.314 ]; then
    # Number of tests for 0.314 MeV
    test_number=( 0 1 2 3 4 5 6 7 8 9 10 11 )
elif [ ${energy} == 0.521 ]; then
    # Number of tests for 0.521 MeV
    test_number=( 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 )
elif [ ${energy} == 1.033 ]; then
    # Number of tests for 1.033 MeV
    test_number=( 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 )
else
    echo "Error: Energy (MeV) \"${energy}\" is currently not supported!"
fi

# loop through test numbers and run mpi script
for i in "${test_number[@]}"
do
    # Change the interp
    line=s/test_number=.*/test_number=\"$i\"/
    sed -i "$line" run_mcnp.sh

     echo -e "\nRunning Lockwood mcnp6.2 ${energy} Test Number $i!"
     bash run_mcnp.sh $file_type ${THREADS}
done
