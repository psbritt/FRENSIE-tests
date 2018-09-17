#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## This script will run the hanson.sh script for several interpolations:
## Decoupled, 2D Coupled, 1D Coupled , and Modified 2D Coupled
##---------------------------------------------------------------------------##

# interpolations to run for mpi ( LINLINLIN LINLINLOG LOGLOGLOG )
interp=( LOGLOGLOG )
# Sey 2D Grid Policy ( CORRELATED UNIT_BASE UNIT_BASE_CORRELATED )
sample_policy=( UNIT_BASE_CORRELATED )
# file type (Native, ACE)
file_type=ACE
# elastic coupled sampling method ( TWO_D, ONE_D, MODIFIED_TWO_D )
method=( TWO_D, ONE_D, MODIFIED_TWO_D )

# Set the file type
command=s/file_type=Data.ElectroatomicDataProperties.*/file_type=Data.ElectroatomicDataProperties.${file_type}_EPR_FILE/
sed -i $command hanson.py
# Set the interp
command=s/interpolation=MonteCarlo.*/interpolation=MonteCarlo.${interp}_INTERPOLATION/
sed -i $command hanson.py
# Set 2D grid policy
command=s/grid_policy=MonteCarlo.*/grid_policy=MonteCarlo.${sample_policy}_SAMPLING/
sed -i $command hanson.py

# Change the distribution to Decoupled
command=s/mode=MonteCarlo.*/mode=MonteCarlo.DECOUPLED_DISTRIBUTION/
sed -i $command hanson.py
echo -e "\nRunning Native Analog with Elastic Decoupled Sampling!"
sbatch hanson.sh

# Change the distribution to coupled
command=s/mode=MonteCarlo.*/mode=MonteCarlo.COUPLED_DISTRIBUTION/
sed -i $command hanson.py

# loop through coupled sampling methods and run mpi script
for i in "${sample_methods[@]}"
do
    # Set the elastic coupled sampling method
    command=s/method=MonteCarlo.*/method=MonteCarlo.${method}_UNION/
    sed -i $command hanson.py
    echo -e "\nRunning Native Analog with Elastic "$i" Coupled Sampling!"
    sbatch hanson.sh
done
