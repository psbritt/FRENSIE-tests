#!/bin/sh
# This file is named run_facemc_mpi.sh
#SBATCH --partition=pre
#SBATCH --time=1-00:00:00
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=16
#SBATCH --mem-per-cpu=4000

##---------------------------------------------------------------------------##
## ---------------------------- FACEMC test runner --------------------------##
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## The electron albedo is found for a semi-infinite aluminum slab. Since the
## electron albedo requires a surface current, DagMC will be used and not Root.
## FRENSIE will be run with three variations. 1. Using ACE data, which should
## match MCNP almost exactly. 2. Using the Native data in analog mode, whcih 
## uses a different interpolation scheme than MCNP. 3. Using Native data in 
## moment preserving mode, which should give a less acurate answer while
## decreasing run time.

##---------------------------------------------------------------------------##
## ------------------------------- COMMANDS ---------------------------------##
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/ecmartin3/software/mcnpdata/
FRENSIE=/home/lkersting/frensie_linlin

INPUT="1"
if [ "$#" -eq 1 ];
then
    # Set the file type (1 = ACE, 2 = Native, 3 = Moment Preserving)
    INPUT="$1"
fi

# Changing variables
ENERGY=".06"
THREADS="80"
ELEMENT="Al"
# Number of histories 1e7
HISTORIES="10"
# Turn certain reactions on (true/false)
ELASTIC_ON="true"
BREM_ON="true"
IONIZATION_ON="true"
EXCITATION_ON="true"


REACTIONS=" -l ${ELASTIC_ON} -b ${BREM_ON} -i ${IONIZATION_ON} -a ${EXCITATION_ON}"
SIM_PARAMETERS="-e ${ENERGY} -n ${HISTORIES} ${REACTIONS}"
ENERGY_EV=$(echo $ENERGY*1000000 |bc)
ENERGY_EV=${ENERGY_EV%.*}
NAME="ace"

if [ ${INPUT} -eq 1 ]
then
    # Use ACE data
    NAME="ace"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 1.0"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t ${NAME}
    INFO="sim_info_${ENERGY}_1.0"
    MAT="mat_${ELEMENT}_${NAME}.xml"
    echo "Using ACE data!"
elif [ ${INPUT} -eq 2 ]
then
    # Use Native analog data
    NAME="native"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 1.0"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t "linlin"
    INFO="sim_info_${ENERGY}_1.0"
    MAT="mat_${ELEMENT}_linlin.xml"
    echo "Using Native analog data!"
elif [ ${INPUT} -eq 3 ]
then
    # Use Native Moment Preserving data
    NAME="moments"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 0.9"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t "linlin"
    INFO="sim_info_${ENERGY}_0.9"
    MAT="mat_${ELEMENT}_linlin.xml"
    echo "Using Native Moment Preserving data!"
else
    # Default to ACE data
    NAME="ace"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 1.0"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t ${NAME}
    INFO="sim_info_${ENERGY}_1.0"
    MAT="mat_${ELEMENT}_${NAME}.xml"
    echo "Input not valid, ACE data will be used!"
fi

# Set the sim info xml file name
if [ "${ELASTIC_ON}" = "false" ]
then
    INFO="${INFO}_no_elastic"
fi
if [ "${BREM_ON}" = "false" ]
then
    INFO="${INFO}_no_brem"
fi
if [ "${IONIZATION_ON}" = "false" ]
then
    INFO="${INFO}_no_ionization"
fi
if [ "${EXCITATION_ON}" = "false" ]
then
    INFO="${INFO}_no_excitation"
fi
INFO="${INFO}.xml"

# .xml file paths.
python ../est.py -e ${ENERGY}
python source.py -e ${ENERGY}
EST="../est_${ENERGY}.xml"
SOURCE="source_${ENERGY}.xml"
GEOM="geom.xml"
RSP="../rsp_fn.xml"
NAME="al_lin_${NAME}_${ENERGY_EV}"

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)
DIR="results/linlin/${TODAY}"
mkdir -p $DIR

echo "Running Facemc Albedo (lin) test with ${HISTORIES} particles on ${THREADS} threads:"
RUN="mpiexec -n ${THREADS} ${FRENSIE}/bin/facemc-mpi --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME}"
echo ${RUN}
${RUN} > ${DIR}/${NAME}.txt 2>&1

echo "Removing old xml files:"
rm ${INFO} ${EST} ${SOURCE} ${MAT} ElementTree_pretty.pyc

# Move file to the test results folder
H5=${NAME}.h5
NEW_NAME="${DIR}/${H5}"
NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"

mv ${H5} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

echo "Results will be in ./${DIR}"
