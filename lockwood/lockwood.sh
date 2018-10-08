#!/bin/sh
# This file is named run_facemc_mpi.sh
#SBATCH --partition=pre
#SBATCH --time=1-00:00:00
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=16

##---------------------------------------------------------------------------##
## ---------------------------- FACEMC test runner --------------------------##
##---------------------------------------------------------------------------##
## FRENSIE benchmark test: Lockwood dose depth data.
## The dose depth for several ranges and material is calculated by dividing the
## energy deposition by the calorimeter thickness (g/cm^2).
##---------------------------------------------------------------------------##

##---------------------------------------------------------------------------##
## ------------------------------- COMMANDS ---------------------------------##
##---------------------------------------------------------------------------##
EXTRA_ARGS=$@

# Set the number of threads
THREADS=160
NODES=10
TASKS=16
# Set the number of histories
HISTORIES=1000000
# Set the max runtime (in minutes, 1 day = 1440 )
TIME=1400

# Create the results directory
python -c "import lockwood; lockwood.createResultsDirectory()"

# # Run the simulation in hybrid parallel
# echo "Running Facemc Lockwood test with ${HISTORIES} particles on ${NODES} nodes with ${TASKS} tasks:"
# mpiexec -n ${NODES} python -c "import lockwood; lockwood.runSimulation(${TASKS}, ${HISTORIES}, ${TIME})"

# Run the simulation in distributed parallel
echo "Running Facemc Lockwood test with ${HISTORIES} particles on ${NODES} nodes:"
mpiexec -n ${THREADS} python -c "import lockwood; lockwood.runSimulation(1, ${HISTORIES}, ${TIME})"

# # Run the simulation in shared parallel
# echo "Running Facemc Lockwood test with ${HISTORIES} particles on ${THREADS} threads:"
# python -c "import lockwood; lockwood.runSimulation(${THREADS}, ${HISTORIES}, ${TIME})"
