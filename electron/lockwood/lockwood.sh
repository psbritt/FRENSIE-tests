#!/bin/sh
# This file is named lockwood.sh
#SBATCH --partition=pre
#SBATCH --time=1-00:00:00
#SBATCH --ntasks=40
#SBATCH --cpus-per-task=4
#SBATCH --output=Al/results/loglog/2018-10-15/al_lockwood_%j

##---------------------------------------------------------------------------##
## ---------------------------- FACEMC test runner --------------------------##
##---------------------------------------------------------------------------##
## FRENSIE benchmark test: Lockwood dose depth data.
## The dose depth for several ranges and material is calculated by dividing the
## energy deposition by the calorimeter thickness (g/cm^2).
##---------------------------------------------------------------------------##

env | grep SLURM | sort

##---------------------------------------------------------------------------##
## ---------------------------- TEST VARIABLES ------------------------------##
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

# Set the test energy (0.314, 0.521, 1.033)
ENERGY=0.314

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

# Set the material element and zaid
ELEMENT="Al"; ZAID=13000

# Set the test number
TEST_NUMBER=11

# Set the calorimeter thickness (g/cm2)
CALORIMETER_THICKNESS=5.050E-03

# Set the range (g/cm2)
RANGE=0.0993

##---------------------------------------------------------------------------##
## ------------------------------- COMMANDS ---------------------------------##
##---------------------------------------------------------------------------##

# Change the lockwood.py parameters

# Set the element
command=s/atom=.*/atom=Data.${ELEMENT}_ATOM\;\ element=\"${ELEMENT}\"\;\ zaid=${ZAID}/
sed -i "${command}" lockwood.py

# Set the calorimeter thickness
command=s/calorimeter_thickness=.*/calorimeter_thickness=${CALORIMETER_THICKNESS}/
sed -i "${command}" lockwood.py

# Set the ranges
command=s/test_range=.*/test_range=${RANGE}/
sed -i "${command}" lockwood.py

# Set the energy
command=s/energy=.*/energy=${ENERGY}/
sed -i "${command}" lockwood.py

# Set the file type
command=s/file_type=Data.ElectroatomicDataProperties.*/file_type=Data.ElectroatomicDataProperties.${FILE_TYPE}_EPR_FILE/
sed -i "${command}" lockwood.py

# Set the interp
command=s/interpolation=MonteCarlo.*/interpolation=MonteCarlo.${INTERP}_INTERPOLATION/
sed -i "${command}" lockwood.py

# Set 2D grid policy
command=s/grid_policy=MonteCarlo.*/grid_policy=MonteCarlo.${GRID_POLICY}_GRID/
sed -i "${command}" lockwood.py

# Set the elastic distribution mode
command=s/mode=MonteCarlo.*/mode=MonteCarlo.${MODE}_DISTRIBUTION/
sed -i "${command}" lockwood.py

# Set the elastic coupled sampling method
command=s/method=MonteCarlo.*/method=MonteCarlo.${METHOD}_UNION/
sed -i "${command}" lockwood.py

# Set the test number
command=s/test_number=.*/test_number=${TEST_NUMBER}/
sed -i "${command}" lockwood.py

# Create the results directory
python -c "import lockwood; lockwood.createResultsDirectory()"

# Run the simulation
echo "Running Facemc Lockwood test with ${HISTORIES} particles with ${SLURM_NTASKS} MPI processes with ${SLURM_CPUS_PER_TASK} OpenMP threads each!"
mpiexec -n ${SLURM_NTASKS} python -c "import lockwood; lockwood.runSimulation(${SLURM_CPUS_PER_TASK}, ${HISTORIES}, ${TIME})"
