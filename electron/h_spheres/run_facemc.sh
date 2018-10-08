#!/bin/bash
##---------------------------------------------------------------------------##
## ---------------------------- FACEMC test runner --------------------------##
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## The electron surface and cell flux and current for three concentrtic spheres
## of Hydrogen for a 1, 10, 100 keV mono-energetic isotropic source of electrons
## FRENSIE will be run with three variations.
## 1. Using the Native data in analog mode, which uses a different interpolation
## scheme than MCNP.
## 2. Using Native data in moment preserving mode, which should give a less
## acurate answer while decreasing run time.
## 3. Using ACE (EPR14) data, which should match MCNP6.2 almost exactly.
## 4. Using ACE (EPR12) data, which should match MCNP6.1 almost exactly.
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/software/mcnp6.2/MCNP_DATA
#CROSS_SECTION_XML_PATH=/home/lkersting/mcnpdata/
FRENSIE=/home/lkersting/frensie

THREADS="8"
if [ "$#" -eq 1 ]; then
    # Set the number of threads used
    THREADS="$1"
fi

# Changing variables

# Source energy (.001, .01, .1 MeV)
ENERGY=.01
ENERGY_KEV=$(echo $ENERGY*1000 |bc)
ENERGY_KEV=${ENERGY_KEV%.*}

# Number of histories 1e7
HISTORIES="10"
# Geometry package (DagMC or ROOT)
GEOMETRY="DagMC"
# Turn certain reactions on (true/false)
ELASTIC_ON="true"
BREM_ON="true"
IONIZATION_ON="true"
EXCITATION_ON="true"
# Two D Interp Policy (logloglog, linlinlin, linlinlog)
INTERP="logloglog"
# Two D Sampling Policy (1 = unit-base correlated, 2 = correlated, 3 = unit-base)
SAMPLE=1
# Elastic distribution ( Decoupled, Coupled, Hybrid )
DISTRIBUTION="Coupled"
# Elastic coupled sampling method ( 2D, 1D, 2DM )
COUPLED_SAMPLING="2DM"

ELEMENT="H"
NAME="native"

ELASTIC="-d ${DISTRIBUTION} -c ${COUPLED_SAMPLING}"
REACTIONS=" -t ${ELASTIC_ON} -b ${BREM_ON} -i ${IONIZATION_ON} -a ${EXCITATION_ON}"
SIM_PARAMETERS="-e ${ENERGY} -n ${HISTORIES} -l ${INTERP} -s ${SAMPLE} ${REACTIONS} ${ELASTIC}"

echo -n "Enter the desired data type (1 = Native, 2 = ACE EPR14, 3 = ACE EPR12) > "
read INPUT
if [ ${INPUT} -eq 2 ]; then
    # Use ACE EPR14 data
    NAME="epr14"
    echo "Using ACE EPR14 data!"
elif [ ${INPUT} -eq 3 ]; then
    # Use ACE EPR12 data
    NAME="ace"
    echo "Using ACE EPR12 data!"
elif [ ${DISTRIBUTION} = "Hybrid" ]; then
    # Use Native moment preserving data
    NAME="moments"
    echo "Using Native Moment Preserving data!"
else
    # Use Native analog data
    echo "Using Native analog data!"
fi

NAME_EXTENTION=""
NAME_REACTION=""
# Set the sim info xml file name
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

# .xml file paths.
INFO=$(python ../sim_info.py ${SIM_PARAMETERS} 2>&1)
MAT=$(python ../mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP} 2>&1)
EST=$(python est.py -e ${ENERGY} -t ${GEOMETRY} 2>&1)
SOURCE=$(python source.py -e ${ENERGY} 2>&1)
GEOM=$(python geom.py -e ${ENERGY} -t ${GEOMETRY} 2>&1)
RSP="../rsp_fn.xml"

if [ ${NAME} = "ace" -o ${NAME} = "epr14" ]; then
    DIR="results/${NAME}/${TODAY}"
    NAME="h_${ENERGY_KEV}kev_${NAME}${NAME_REACTION}"
else
    DIR="results/${INTERP}/${TODAY}"

    if [ ${SAMPLE} = 1 ]; then
        SAMPLE_NAME="unit_correlated"
    elif [ ${SAMPLE} = 2 ]; then
        SAMPLE_NAME="correlated"
    elif [ ${SAMPLE} = 3 ]; then
        SAMPLE_NAME="unit_base"
    fi

    NAME="h_${ENERGY_KEV}kev_${NAME}_${INTERP}_${SAMPLE_NAME}${NAME_EXTENTION}${NAME_REACTION}"
fi

if [ "${GEOMETRY}" = "ROOT" ]; then
    NAME="${NAME}_root"
fi

# Make directory for the test results
DIR="results/testrun/${INTERP}/"

mkdir -p ${DIR}

echo "Running Facemc H spheres test with ${HISTORIES} particles on ${THREADS} threads:"
RUN="${FRENSIE}/bin/facemc --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME} --threads=${THREADS}"
echo ${RUN}
${RUN}

echo "Removing old xml files:"
rm ${INFO} ${EST} ${SOURCE} ${MAT} ${GEOM} ../ElementTree_pretty.pyc

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
