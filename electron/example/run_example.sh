#!/bin/sh
# This file is named run_al_mpi.sh
#SBATCH --partition=pre
#SBATCH --time=1-00:00:00
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=16

##---------------------------------------------------------------------------##
## ---------------------------- FACEMC test runner --------------------------##
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## The electron surface and cell flux and current for three concentrtic spheres
## of Hydrogen for a 1, 10, 100 keV mono-energetic isotropic source of electrons.
##---------------------------------------------------------------------------##

##---------------------------------------------------------------------------##
## ------------------------------- COMMANDS ---------------------------------##
##---------------------------------------------------------------------------##
EXTRA_ARGS=$@

# Set the number of threads
THREADS=112
NODES=7
TASKS=16
# Set the number of histories
HISTORIES=1000000
# Set the max runtime (in minutes, 1 day = 1440 )
TIME=1400

# Create the results directory
python -c "import example;example.createResultsDirectory()"

# # Run the simulation in hybrid parallel
# echo "Running Facemc Example test with ${HISTORIES} particles on ${NODES} nodes with ${TASKS} tasks:"
# mpiexec -n ${NODES} python -c "import example; example.runSimulation(${TASKS}, ${HISTORIES}, ${TIME})"

# Run the simulation in distributed parallel
echo "Running Facemc Example test with ${HISTORIES} particles on ${THREADS} nodes:"
mpiexec -n ${THREADS} python -c "import example; example.runSimulation(1, ${HISTORIES}, ${TIME})"

# # Run the simulation in shared parallel
# echo "Running Facemc Example test with ${HISTORIES} particles on ${THREADS} threads:"
# python -c "import example; example.runSimulation(${THREADS}, ${HISTORIES}, ${TIME})"