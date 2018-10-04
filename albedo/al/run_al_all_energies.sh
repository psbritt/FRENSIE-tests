#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC multiple mpi tests runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## This script will run the run_al_mpi.sh script at several different energies:
## .005 .0093 .01 .011 .0134 .015 .0173 .02 .0252 .03 .04 .0415 .05 .06 .0621
## .0818 and .102 MeV
##---------------------------------------------------------------------------##

# Set 2D interpolation ( LINLINLIN LINLINLOG LOGLOGLOG )
interp=LOGLOGLOG
# Set 2D Grid Policy ( CORRELATED UNIT_BASE UNIT_BASE_CORRELATED )
grid_policy=UNIT_BASE_CORRELATED
# file type (Native, ACE)
file_type=Native
# elastic distribution mode ( DECOUPLED, COUPLED, HYBRID )
mode=COUPLED
# elastic coupled sampling method ( TWO_D, ONE_D, MODIFIED_TWO_D )
method=TWO_D

# Set the file type
command=s/file_type=Data.ElectroatomicDataProperties.*/file_type=Data.ElectroatomicDataProperties.${file_type}_EPR_FILE/
sed -i $command al_albedo.py
# Set the elastic distribution mode
command=s/mode=MonteCarlo.*/mode=MonteCarlo.${mode}_DISTRIBUTION/
sed -i $command al_albedo.py
# Set the elastic coupled sampling method
command=s/method=MonteCarlo.*/method=MonteCarlo.${method}_UNION/
sed -i $command al_albedo.py

# Material element
element="Al"

if [ "${element}" == "Al" ]; then
    # Source energies for Al (MeV)
    energies=(0.0002 0.0003 0.0004 0.0005 0.0006 0.0008 0.001 0.0015 0.002 0.0025 0.003 0.0035 0.004 0.0045 0.005 0.006 0.0093 0.01 0.011 0.0134 0.015 0.0173 0.02 0.0252 0.03 0.04 0.0415 0.05 0.06 0.0621 0.07 0.08 0.0818 0.1 0.102 0.121 0.146 0.172 0.196 0.2 0.238 0.256)
else
    echo "Error: Element \"${element}\" is currently not supported!"
fi

# loop through energies and run mpi script
for i in "${energies[@]}"
do
    command=s/energy=.*/energy=${i}/
    print $command
    sed -i "$command" al_albedo.py
    echo -e "\nRunning Al Albedo Test at an Energy of "$i" MeV!"
    sbatch run_al_albedo.sh
done
