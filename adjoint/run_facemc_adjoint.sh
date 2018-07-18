#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE Forward with Adjoint.
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
#CROSS_SECTION_XML_PATH=/home/lkersting/mcnpdata/
CROSS_SECTION_XML_PATH=/home/software/mcnp6.2/MCNP_DATA/
FRENSIE=/home/lkersting/frensie/

THREADS="12"
if [ "$#" -eq 1 ]; then
    # Set the number of threads used
    THREADS="$1"
fi

# Changing variables
# Number of histories
HISTORIES="100"
# Delta source energy in MeV ( 0.001, 0.01, 0.1)
ENERGY="0.01"
# The Geometry package (ROOT or DagMC)
GEOMETRY="ROOT"
# Turn certain reactions on (true/false)
ELASTIC_ON="true"
BREM_ON="true"
IONIZATION_ON="true"
EXCITATION_ON="true"
# Two D Interp Policy (logloglog, linlinlin, linlinlog)
INTERP="logloglog"
# Elastic distribution ( Decoupled, Coupled, Hybrid )
DISTRIBUTION="Coupled"
# Elastic coupled sampling method (( 2D, 1D, 2DM ))
COUPLED_SAMPLING="2DM"
# Option to turn on particle tracker (true/false)
PARTICLE_TRACKER="false"


ELEMENT="H"

ELASTIC="-d ${DISTRIBUTION} -c ${COUPLED_SAMPLING}"
REACTIONS="-t ${ELASTIC_ON} -b ${BREM_ON} -i ${IONIZATION_ON} -a ${EXCITATION_ON}"
SIM_PARAMETERS="-e ${ENERGY} -n ${HISTORIES} ${REACTIONS} ${ELASTIC}"

NAME="native"
if [ ${DISTRIBUTION} = "Hybrid" ]; then
    # Use Native moment preserving data
    NAME="moments"
    echo "Using Native Moment Preserving data!"
else
    # Use Native analog data
    echo "Using Native analog data!"
fi

NAME_EXTENTION=""
NAME_REACTION=""
# Set the file name extentions
if [ "${ELASTIC_ON}" = "false" ]; then
    NAME_REACTION="${NAME_REACTION}_no_elastic"
elif [ ${DISTRIBUTION} = "Coupled" ]; then
    NAME_EXTENTION="${NAME_EXTENTION}_${COUPLED_SAMPLING}"
fi
if [ "${BREM_ON}" = "false" ]; then
    NAME_REACTION="${NAME_REACTION}_no_brem"
fi
if [ "${IONIZATION_ON}" = "false" ]; then
    NAME_REACTION="${NAME_REACTION}_no_ionization"
fi
if [ "${EXCITATION_ON}" = "false" ]; then
    NAME_REACTION="${NAME_REACTION}_no_excitation"
fi
if [ "${GEOMETRY}" = "ROOT" ]; then
    NAME_EXTENTION="${NAME_EXTENTION}_root"
fi

# .xml file paths.
INFO=$(python ../adjoint_sim_info.py ${SIM_PARAMETERS} 2>&1)
MAT=$(python ../mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP} 2>&1)
SOURCE=$(python ./adjoint_source.py -d ${CROSS_SECTION_XML_PATH} -e ${ENERGY} 2>&1)
EST=$(python ./adjoint_est.py -e ${ENERGY} -t ${GEOMETRY} -p ${PARTICLE_TRACKER} 2>&1)
GEOM=$(python ./geom.py -t ${GEOMETRY} 2>&1)
RSP="../rsp_fn.xml"

# Make directory for the test results
TODAY=$(date +%Y-%m-%d)

DIR="results/testrun/${INTERP}"
NAME="adjoint_${NAME}_${INTERP}${NAME_EXTENTION}${NAME_REACTION}"

mkdir -p $DIR

echo "Running Facemc Adjoint H-Sphere test with ${HISTORIES} particles on ${THREADS} threads:"
RUN="${FRENSIE}/bin/facemc --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME} --threads=${THREADS}"
echo ${RUN}
#gdb --args ${RUN}
${RUN}

echo "Removing old xml files:"
rm ${INFO} ${MAT} ${EST} ${GEOM} ${SOURCE} ../ElementTree_pretty.pyc

echo "Processing the results:"
H5=${NAME}.h5
NEW_NAME="${DIR}/${H5}"
NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"
mv ${H5} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

cd ${DIR}

if [ "${GEOMETRY}" = "ROOT" ]; then
    bash ../../../data_processor_root.sh ${NAME}
else
    bash ../../../data_processor.sh ${NAME}
fi
echo "Results will be in ./${DIR}"