#!/bin/sh
# This file is named run_facemc_mpi.sh
#SBATCH --partition=univ2
#SBATCH --time=4-00:00:00
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=20
#SBATCH --mem-per-cpu=4000

##---------------------------------------------------------------------------##
## ---------------------------- FACEMC test runner --------------------------##
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## The electron surface and cell flux and current for three concentrtic spheres
## of Hydrogen for a 1, 10, 100 keV mono-energetic isotropic source of electrons.
## FRENSIE will be run with three variations.
## 1. Using ACE data, which should match MCNP almost exactly.
## 2. Using the Native data in analog mode, which uses a different interpolation
## scheme than MCNP.
## 3. Using Native data in moment preserving mode, which should give a less
## acurate answer while decreasing run time.

# ------------------------------- COMMANDS ------------------------------------

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/lkersting/mcnpdata/
#CROSS_SECTION_XML_PATH=/home/software/mcnp6.2/MCNP_DATA/
FRENSIE=/home/lkersting/frensie

INPUT="1"
if [ "$#" -eq 1 ];
then
    # Set the file type (1 = ACE, 2 = Native, 3 = Moment Preserving)
    INPUT="$1"
fi

# Changing variables

# Number of threads
THREADS="100"
# Number of histories 1e8
HISTORIES="100000000"
# Turn certain reactions on (true/false)
ELASTIC_ON="true"
BREM_ON="true"
IONIZATION_ON="true"
EXCITATION_ON="true"
# Turn certain electron properties on (true/false)
LINLINLOG_ON="false"
CORRELATED_ON="true"
UNIT_BASED_ON="false"

# Geometry package (DagMC or ROOT)
GEOMETRY="DagMC"
# Source Energy (.01 MeV)
ENERGY=0.01
ENERGY_KEV=$(echo $ENERGY*1000 |bc)
ENERGY_KEV=${ENERGY_KEV%.*}

REACTIONS=" -t ${ELASTIC_ON} -b ${BREM_ON} -i ${IONIZATION_ON} -a ${EXCITATION_ON}"
SIM_PARAMETERS="-e ${ENERGY} -n ${HISTORIES} -l ${LINLINLOG_ON} -s ${CORRELATED_ON} -u ${UNIT_BASED_ON} ${REACTIONS}"
NAME="ace"

INTERP="linlin"
if [ ${LINLINLOG_ON} = true ]
then
    INTERP="linlog"
fi

ELEMENT="H"

if [ ${INPUT} -eq 1 ]
then
    # Use ACE data
    NAME="ace"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 1.0"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP}
    INFO="sim_info_${ENERGY}_1.0"
    MAT="mat_${ELEMENT}_${NAME}.xml"
    echo "Using ACE data!"
elif [ ${INPUT} -eq 2 ]
then
    # Use Native analog data
    NAME="native"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 1.0"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP}
    INFO="sim_info_${ENERGY}_1.0"
    MAT="mat_${ELEMENT}_${NAME}_${INTERP}.xml"
    echo "Using Native analog data!"
elif [ ${INPUT} -eq 3 ]
then
    # Use Native Moment Preserving data
    NAME="moments"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 0.9"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t "native" -i ${INTERP}
    INFO="sim_info_${ENERGY}_0.9"
    MAT="mat_${ELEMENT}_native_${INTERP}.xml"
    echo "Using Native Moment Preserving data!"
else
    # Default to ACE data
    NAME="ace"
    SIM_PARAMETERS="${SIM_PARAMETERS} -c 1.0"
    python sim_info.py ${SIM_PARAMETERS}
    python mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP}
    INFO="sim_info_${ENERGY}_1.0"
    MAT="mat_${ELEMENT}_${NAME}_${INTERP}.xml"
    echo "Input not valid, ACE data will be used!"
fi

INTERP_NAMES=""
# Set the sim info xml file name
if [ "${LINLINLOG_ON}" = "false" ]
then
    INTERP_NAMES="${INTERP_NAMES}_linlinlin"
fi
if [ "${CORRELATED_ON}" = "false" ]
then
    INTERP_NAMES="${INTERP_NAMES}_stochastic"
fi
if [ "${UNIT_BASED_ON}" = "false" ]
then
    INTERP_NAMES="${INTERP_NAMES}_exact"
fi

REACTION_NAMES=''
if [ "${ELASTIC_ON}" = "false" ]
then
    REACTION_NAMES="${REACTION_NAMES}_no_elastic"
fi
if [ "${BREM_ON}" = "false" ]
then
    REACTION_NAMES="${REACTION_NAMES}_no_brem"
fi
if [ "${IONIZATION_ON}" = "false" ]
then
    REACTION_NAMES="${REACTION_NAMES}_no_ionization"
fi
if [ "${EXCITATION_ON}" = "false" ]
then
    REACTION_NAMES="${REACTION_NAMES}_no_excitation"
fi

python est.py -e ${ENERGY} -t ${GEOMETRY}
python source.py -e ${ENERGY}
python geom.py -t ${GEOMETRY}

# .xml directory paths.
INFO="${INFO}${INTERP_NAMES}${REACTION_NAMES}.xml"
GEOM="geom.xml"
RSP="rsp_fn.xml"
EST="est_${ENERGY}.xml"
SOURCE="source_${ENERGY}.xml"

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)
DIR=''
if [ "${NAME}" = "ace" ]
then
    DIR="results/ace/${TODAY}"
    NAME="${NAME}${REACTION_NAMES}"
else
    DIR="results/${INTERP}/${TODAY}"
    NAME="${NAME}${INTERP_NAMES}${REACTION_NAMES}"
fi

mkdir -p ${DIR}

# Modify paths for root geometry
if [ "${GEOMETRY}" = "ROOT" ]
then
    NAME="${NAME}_root"
    GEOM="geom_root.xml"
    EST="est_${ENERGY}_root.xml"
fi

echo "Running Facemc H spheres test with ${HISTORIES} particles on ${THREADS} threads:"
RUN="mpiexec -n ${THREADS} ${FRENSIE}/bin/facemc-mpi --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME}"
echo ${RUN}
${RUN} > ${DIR}/${NAME}.txt 2>&1

echo "Removing old xml files:"
rm ${INFO} ${EST} ${SOURCE} ${MAT} ${GEOM} ../ElementTree_pretty.pyc

# Move file to the test results folder
echo "Moving the results:"
H5=${NAME}.h5
NEW_NAME="${DIR}/${H5}"
NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"

mv ${H5} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

echo "Results will be in ./${DIR}"
