#!/bin/sh
# This file is named hanson.sh
#SBATCH --partition=pre
#SBATCH --time=1-00:00:00
#SBATCH --nodes=7
#SBATCH --ntasks-per-node=16

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
## ------------------------------- COMMANDS ---------------------------------##
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
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
python -c "import hanson; hanson.createResultsDirectory()"

# Run the simulation in hybrid parallel
echo "Running Facemc Hanson test with ${HISTORIES} particles on ${NODES} nodes with ${TASKS} tasks:"
mpiexec -n ${NODES} python -c "import hanson; hanson.runSimulation(${TASKS}, ${HISTORIES}, ${TIME})"

# Run the simulation in distributed parallel
# echo "Running Facemc Hanson test with ${HISTORIES} particles on ${NODES} nodes:"
# mpiexec -n ${THREADS} python -c "import hanson; hanson.runSimulation(1, ${HISTORIES})"

# Run the simulation in shared parallel
# echo "Running Facemc Hanson test with ${HISTORIES} particles on ${THREADS} threads:"
# python -c "import hanson; hanson.runSimulation(${THREADS}, ${HISTORIES})"