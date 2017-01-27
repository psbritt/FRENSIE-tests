#!/bin/sh
# This file is named run_facemc_mpi.sh
#SBATCH --partition=univ2
#SBATCH --time=0-20:00:00
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=20
#SBATCH --mem-per-cpu=4000

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
## FRENSIE will be run with three variations.
## 1. Using ACE data, which should match MCNP almost exactly.
## 2. Using the Native data in analog mode, whcih uses a different interpolation
## scheme than MCNP.
## 3. Using Native data in moment preserving mode, which should give a less
## acurate answer while decreasing run time.

##---------------------------------------------------------------------------##
## ------------------------------- COMMANDS ---------------------------------##
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/ecmartin3/software/mcnpdata/
FRENSIE=/home/lkersting/frensie

INPUT="1"
if [ "$#" -eq 1 ];
then
    # Set the file type (1 = ACE, 2 = Native, 3 = Moment Preserving)
    INPUT="$1"
fi

# Changing variables
THREADS="100"
ELEMENT="Au"
# Number of histories 1e6
HISTORIES="1000000"

ENERGY="15.7"
NAME="ace"

if [ ${INPUT} -eq 1 ]
then
    # Use ACE data
    NAME="ace"
    python mat.py -n ${ELEMENT} -t ${NAME}
    python sim_info.py -n ${HISTORIES} -c 1.0
    echo "Using ACE data!"
elif [ ${INPUT} -eq 2 ]
then
    # Use Native analog data
    NAME="native"
    python mat.py -n ${ELEMENT} -t ${NAME}
    python sim_info.py -n ${HISTORIES} -c 1.0
    echo "Using Native analog data!"
elif [ ${INPUT} -eq 3 ]
then
    # Use Native Moment Preserving data
    NAME="moments"
    python mat.py -n ${ELEMENT} -t "native"
    python sim_info.py -n ${HISTORIES} -c 0.9
    echo "Using Native Moment Preserving data!"
else
    # Default to ACE data
    echo "Input not valid, ACE data will be used!"
    python mat.py -n ${ELEMENT} -t ${NAME}
    python sim_info.py -n ${HISTORIES} -c 1.0
fi

# .xml file paths.
python est.py
python source.py
MAT="mat.xml"
INFO="sim_info.xml"
GEOM="geom.xml"
SOURCE="source.xml"
RSP="../rsp_fn.xml"
EST="est.xml"
NAME="hanson_${NAME}"

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)
DIR="results/${TODAY}"
mkdir -p $DIR

echo "Running Facemc Hanson test with ${THREADS} threads:"
RUN="mpiexec -n ${THREADS} ${FRENSIE}/bin/facemc-mpi --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME}"
echo ${RUN}
${RUN} > ${DIR}/${NAME}.txt 2>&1

echo "Moving the results:"

# Move file to the test results folder
H5=${NAME}.h5
NEW_NAME="${DIR}/${H5}"
NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"

mv ${H5} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

echo "Results will be in ./${DIR}"
