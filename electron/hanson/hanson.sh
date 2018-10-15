#!/bin/sh
# This file is named hanson.sh
#SBATCH --partition=pre
#SBATCH --time=1-00:00:00
#SBATCH --ntasks=40
#SBATCH --cpus-per-task=4

##---------------------------------------------------------------------------##
## ---------------------------- FACEMC test runner --------------------------##
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## The electron angular distribution for a thin gold foil of .0009658 cm.
## The # of particles per steradian for scattering angle is found by dividing
## the surface current by 2pi * ( \mu_{i} - \mu_{i-1} ) where \mu_{0} is the
## lowest cosine bin (ie: -1). Surface current is needed so DagMC will be used.
## The #/steradians can be changed to #/square degree by multiplying by
## (pi/180)^2.
##---------------------------------------------------------------------------##
EXTRA_ARGS=$@

# Set the number of histories
HISTORIES=1000000
# Set the max runtime (in minutes, 1 day = 1440 )
TIME=1400

##---------------------------------------------------------------------------##
## ------------------------------- COMMANDS ---------------------------------##
##---------------------------------------------------------------------------##

# Run from the rendezvous
if [ "$#" -eq 1 ]; then
  # Set the rendezvous
  RENDEZVOUS="$1"

  # Restart the simulation
  echo "Restarting Facemc Hanson test for ${HISTORIES} particles with ${SLURM_NTASKS} MPI processes with ${SLURM_CPUS_PER_TASK} OpenMP threads each!"
  mpiexec -n ${SLURM_NTASKS} python -c "import hanson; hanson.restartSimulation(${SLURM_CPUS_PER_TASK}, ${HISTORIES}, ${TIME}, \"${RENDEZVOUS}\" )"

# Run new simulation
else

  # Set the data file type (ACE Native)
  FILE_TYPE=Native

  # Set the bivariate interpolation ( LOGLOGLOG LINLINLIN LINLINLOG )
  INTERP=LOGLOGLOG

  # Set the bivariate Grid Policy ( UNIT_BASE_CORRELATED CORRELATED UNIT_BASE )
  GRID_POLICY=UNIT_BASE_CORRELATED

  # Set the elastic distribution mode ( DECOUPLED COUPLED HYBRID )
  MODE=COUPLED

  # Set the elastic coupled sampling method ( ONE_D TWO_D MODIFIED_TWO_D )
  METHOD=MODIFIED_TWO_D

  # Create a unique python script and change the parameters
  python_script="hanson_${SLURM_JOB_ID}"
  cp hanson.py ${python_script}.py

  # Set the file type
  command=s/file_type=Data.ElectroatomicDataProperties.*/file_type=Data.ElectroatomicDataProperties.${FILE_TYPE}_EPR_FILE/
  sed -i $command ${python_script}.py
  # Set the elastic distribution mode
  command=s/mode=MonteCarlo.*/mode=MonteCarlo.${MODE}_DISTRIBUTION/
  sed -i $command ${python_script}.py
  # Set the elastic coupled sampling method
  command=s/method=MonteCarlo.*/method=MonteCarlo.${METHOD}_UNION/
  sed -i $command ${python_script}.py
  # Change the interp
  command=s/interpolation=MonteCarlo.*/interpolation=MonteCarlo.${INTERP}_INTERPOLATION/
  sed -i $command ${python_script}.py
  # Set 2D grid policy
  command=s/grid_policy=MonteCarlo.*/grid_policy=MonteCarlo.${GRID_POLICY}_GRID/
  sed -i $command ${python_script}.py

  # Create the results directory
  directory=$(python -c "import ${python_script}; ${python_script}.createResultsDirectory()" 2>&1)

  # Run the simulation
  echo "Running Facemc Hanson test with ${HISTORIES} particles with ${SLURM_NTASKS} MPI processes with ${SLURM_CPUS_PER_TASK} OpenMP threads each!"
  mpiexec -n ${SLURM_NTASKS} python -c "import ${python_script}; ${python_script}.runSimulation(${SLURM_CPUS_PER_TASK}, ${HISTORIES}, ${TIME})"

  # Remove the temperary python script
  rm ${python_script}.py*
fi

  # Move the slurm file to the results directory
  mv slurm-${SLURM_JOB_ID}.out ./${directory}