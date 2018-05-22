#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs using the Lockwood energy deposition data
## This script will run the run_lockwood_mpi.sh script for all test numbers.
##---------------------------------------------------------------------------##

# file type (1 = Native, 2 = ACE EPR14, 3 = ACE EPR12)
file_type=1
# Material element
element="Al"
# Energy (0.314, 0.521, 1.033) MeV
energy="0.314"

if [ "${element}" == "Al" ]; then
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
else
    echo "Error: Element \"${element}\" is currently not supported!"
fi

# loop through test numbers and run mpi script
for i in "${test_number[@]}"
do
    # Change the interp
    line=s/ELEMENT=.*/ELEMENT=\"${element}\"\;\ ENERGY=\"${energy}\"\;\ TEST_NUMBER=\"$i\"/
    sed -i "$line" run_lockwood_mpi.sh

     echo -e "\nRunning Lockwood ${element} ${energy} Test Number $i!"
     sbatch run_lockwood_mpi.sh $file_type
done
