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
## The electron albedo is found for a semi-infinite aluminum slab. Since the
## electron albedo requires a surface current, DagMC will be used and not Root.

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
python -c "import al_albedo; al_albedo.createResultsDirectory()"

# # Run the simulation in hybrid parallel
# echo "Running Facemc Al Albedo test with ${HISTORIES} particles on ${NODES} nodes with ${TASKS} tasks:"
# mpiexec -n ${NODES} python -c "import al_albedo; al_albedo.runSimulation(${TASKS}, ${HISTORIES}, ${TIME})"

# Run the simulation in distributed parallel
echo "Running Facemc Al Albedo test with ${HISTORIES} particles on ${NODES} nodes:"
mpiexec -n ${THREADS} python -c "import al_albedo; al_albedo.runSimulation(1, ${HISTORIES}, ${TIME})"

# # Run the simulation in shared parallel
# echo "Running Facemc Al Albedo test with ${HISTORIES} particles on ${THREADS} threads:"
# python -c "import al_albedo; al_albedo.runSimulation(${THREADS}, ${HISTORIES}, ${TIME})"