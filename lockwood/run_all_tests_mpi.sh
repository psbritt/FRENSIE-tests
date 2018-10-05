#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs using the Lockwood energy deposition data
## This script will run the run_lockwood.sh script for all test numbers.
##---------------------------------------------------------------------------##

# interpolations to run for mpi ( LINLINLIN LINLINLOG LOGLOGLOG )
interp=( LOGLOGLOG )
# Sey 2D Grid Policy ( CORRELATED UNIT_BASE UNIT_BASE_CORRELATED )
sample_policy=( UNIT_BASE_CORRELATED )
# file type (Native, ACE)
file_type=Native
# elastic distribution mode ( DECOUPLED, COUPLED, HYBRID )
mode=COUPLED
# elastic coupled sampling method ( TWO_D, ONE_D, MODIFIED_TWO_D )
method=MODIFIED_TWO_D
# Material element
element="C"
# Energy (0.314, 0.521, 1.033) MeV
energy="1"

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
elif [ "${element}" == "C" ]; then
  if [ ${energy} == 1 ]; then
      # Number of tests for 1 MeV
      test_number=( 0 1 2 3 4 5 6 7 8 9 )
else
      echo "Error: Energy (MeV) \"${energy}\" is currently not supported!"
  fi
else
    echo "Error: Element \"${element}\" is currently not supported!"
fi


# Set the file type
command=s/file_type=Data.ElectroatomicDataProperties.*/file_type=Data.ElectroatomicDataProperties.${file_type}_EPR_FILE/
sed -i $command lockwood.py
# Set the interp
command=s/interpolation=MonteCarlo.*/interpolation=MonteCarlo.${interp}_INTERPOLATION/
sed -i $command lockwood.py
# Set 2D grid policy
command=s/grid_policy=MonteCarlo.*/grid_policy=MonteCarlo.${sample_policy}_SAMPLING/
sed -i $command lockwood.py
# Set the elastic distribution mode
command=s/mode=MonteCarlo.*/mode=MonteCarlo.${mode}_DISTRIBUTION/
sed -i $command lockwood.py

if [ "${mode}" == "COUPLED" ]; then
  # Set the elastic coupled sampling method
  command=s/method=MonteCarlo.*/method=MonteCarlo.${method}_UNION/
  sed -i $command lockwood.py
fi

# loop through test numbers and run mpi script
for i in "${test_number[@]}"
do
    # Change the energy
    line=s/energy=.*/energy=${energy}/
    sed -i "$line" lockwood.py

    # Change the test number
    line=s/test_number=.*/test_number=${i}/
    sed -i "$line" lockwood.py

     echo -e "\nRunning Lockwood ${element} ${energy} ${interp} ${sample_policy} ${method}Test Number ${i}!"
     sbatch run_lockwood.sh
done
