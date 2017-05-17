#!/bin/bash
##---------------------------------------------------------------------------##
## ---------------------------- FACEMC test runner --------------------------##
##---------------------------------------------------------------------------##
## Validation runs comparing FRENSIE and MCNP.
## The electron surface and cell flux and current for three concentrtic spheres
## of Hydrogen for a 1, 10, 100 keV mono-energetic isotropic source of electrons
## FRENSIE will be run with three variations.
## 1. Using ACE data, which should match MCNP almost exactly.
## 2. Using the Native data in analog mode, which uses a different interpolation
## scheme than MCNP.
## 3. Using Native data in moment preserving mode, which should give a less
## acurate answer while decreasing run time.
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/software/mcnpdata/
#CROSS_SECTION_XML_PATH=/home/ecmartin3/software/mcnpdata/
#FRENSIE=/home/lkersting/research/frensie-repos/lkersting
FRENSIE=/home/lkersting/frensie

THREADS="8"
if [ "$#" -eq 1 ];
then
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
GEOMETRY="ROOT"
# Turn certain reactions on (true/false)
ELASTIC_ON="true"
BREM_ON="true"
IONIZATION_ON="true"
EXCITATION_ON="true"
# Turn certain electron properties on (true/false)
LINLINLOG_ON="true"
CORRELATED_ON="true"
UNIT_BASED_ON="true"

REACTIONS=" -t ${ELASTIC_ON} -b ${BREM_ON} -i ${IONIZATION_ON} -a ${EXCITATION_ON}"
SIM_PARAMETERS="-e ${ENERGY} -n ${HISTORIES} -l ${LINLINLOG_ON} -s ${CORRELATED_ON} -u ${UNIT_BASED_ON} ${REACTIONS}"
NAME="ace"

INTERP="linlin"
if [ ${LINLINLOG_ON} = true ]
then
    INTERP="linlog"
fi

ELEMENT="H"

echo -n "Enter the desired data type (1 = ACE, 2 = Native, 3 = Moment Preserving) > "
read INPUT
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

NAME_EXTENTION=""
# Set the sim info xml file name
if [ "${LINLINLOG_ON}" = "false" ]
then
    NAME_EXTENTION="${NAME_EXTENTION}_linlinlin"
fi
if [ "${CORRELATED_ON}" = "false" ]
then
    NAME_EXTENTION="${NAME_EXTENTION}_stochastic"
fi
if [ "${UNIT_BASED_ON}" = "false" ]
then
    NAME_EXTENTION="${NAME_EXTENTION}_exact"
fi
if [ "${ELASTIC_ON}" = "false" ]
then
    NAME_EXTENTION="${NAME_EXTENTION}_no_elastic"
fi
if [ "${BREM_ON}" = "false" ]
then
    NAME_EXTENTION="${NAME_EXTENTION}_no_brem"
fi
if [ "${IONIZATION_ON}" = "false" ]
then
    NAME_EXTENTION="${NAME_EXTENTION}_no_ionization"
fi
if [ "${EXCITATION_ON}" = "false" ]
then
    NAME_EXTENTION="${NAME_EXTENTION}_no_excitation"
fi

python est.py -e ${ENERGY} -t ${GEOMETRY}
python source.py -e ${ENERGY}
python geom.py -e ${ENERGY} -t ${GEOMETRY}

# .xml directory paths.
INFO="${INFO}${NAME_EXTENTION}.xml"
GEOM="geom_${ENERGY}.xml"
RSP="rsp_fn.xml"
EST="est_${ENERGY}.xml"
SOURCE="source_${ENERGY}.xml"
NAME="h_${ENERGY_KEV}kev_${NAME}${NAME_EXTENTION}"
if [ "${GEOMETRY}" = "ROOT" ]
then
    NAME="${NAME}_root"
    GEOM="geom_${ENERGY}_root.xml"
    EST="est_${ENERGY}_root.xml"
fi

# Make directory for the test results
DIR="results/testrun/${INTERP}/"

mkdir -p ${DIR}

echo "Running Facemc H spheres test with ${HISTORIES} particles on ${THREADS} threads:"
RUN="${FRENSIE}/bin/facemc --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME} --threads=${THREADS}"
echo ${RUN}
${RUN} > ${DIR}/${NAME}.txt 2>&1

echo "Removing old xml files:"
rm ${INFO} ${EST} ${SOURCE} ${MAT} ${GEOM} ElementTree_pretty.pyc

echo "Processing the results:"
H5=${NAME}.h5
NEW_NAME="${DIR}/${H5}"
NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"
mv ${H5} ${NEW_NAME}
mv continue_run.xml ${NEW_RUN_INFO}

cd ${DIR}

if [ "${GEOMETRY}" = "ROOT" ]
then
    bash ../../../data_processor_root.sh ${NAME}
else
    bash ../../../data_processor.sh ${NAME}
fi
echo "Results will be in ./${DIR}"
