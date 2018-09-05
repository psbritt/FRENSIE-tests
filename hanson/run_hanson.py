#! /usr/bin/env python
import PyFrensie.Geometry as Geometry
import PyFrensie.Geometry.DagMC as DagMC
import PyFrensie.Geometry.ROOT as ROOT
import PyFrensie.Utility as Utility
import PyFrensie.Utility.MPI as MPI
import PyFrensie.Utility.Prng as Prng
import PyFrensie.Utility.Coordinate as Coordinate
import PyFrensie.Utility.Distribution as Distribution
import PyFrensie.MonteCarlo as MonteCarlo
import PyFrensie.MonteCarlo.Collision as Collision
import PyFrensie.MonteCarlo.ActiveRegion as ActiveRegion
import PyFrensie.MonteCarlo.Event as Event
import PyFrensie.MonteCarlo.Manager as Manager
import PyFrensie.Data as Data
import PyFrensie.Data.Native as Native
import numpy
import os
import sys

##---------------------------------------------------------------------------##
## ------------------------------ MPI Session ------------------------------ ##
##---------------------------------------------------------------------------##
session = MPI.GlobalMPISession( len(sys.argv), sys.argv )
session.initializeLogs( 0, True )

##---------------------------------------------------------------------------##
## ------------------------- SIMULATION PROPERTIES ------------------------- ##
##---------------------------------------------------------------------------##
properties = MonteCarlo.SimulationProperties()

## -------------------------- GENERAL PROPERTIES --------------------------- ##

# Set the particle mode
properties.setParticleMode( MonteCarlo.ELECTRON_MODE )

# Set the number of histories
properties.setNumberOfHistories( 10 )

## -------------------------- NEUTRON PROPERTIES --------------------------- ##

## --------------------------- PHOTON PROPERTIES --------------------------- ##

## -------------------------- ELECTRON PROPERTIES -------------------------- ##

# Set the min electron energy in MeV (Default is 100 eV)
properties.setMinElectronEnergy( 1e-4 )

# Set the max electron energy in MeV (Default is 20 MeV)
properties.setMaxElectronEnergy( 20.0 )

# Set the bivariate interpolation (LOGLOGLOG, LINLINLIN, LINLINLOG)
properties.setElectronTwoDInterpPolicy( MonteCarlo.LOGLOGLOG_INTERPOLATION )

# Set the bivariate Grid Policy (UNIT_BASE_CORRELATED, CORRELATED, UNIT_BASE)
grid_policy = MonteCarlo.UNIT_BASE_CORRELATED_SAMPLING
properties.setElectronTwoDSamplingPolicy( grid_policy )

# Set the electron evaluation tolerance (Default is 1e-7)
properties.setElectronEvaluationTolerance( 1e-8 )

## --- Elastic Properties ---

# Turn elastic electron scattering off
# properties.setElasticModeOff()

# Set the elastic distribution mode ( DECOUPLED, COUPLED, HYBRID )
properties.setElasticElectronDistributionMode( MonteCarlo.COUPLED_DISTRIBUTION )

# Set the elastic coupled sampling method
# ( TWO_D_UNION, ONE_D_UNION, MODIFIED_TWO_D_UNION )
properties.setCoupledElasticSamplingMode( MonteCarlo.TWO_D_UNION )

# Set the elastic cutoff angle cosine ( -1.0 < mu < 1.0 )
properties.setElasticCutoffAngleCosine( 1.0 )

## --- Electroionization Properties ---

# Turn the electro-ionization reaction off
# properties.setElectroionizationModeOff()

## --- Bremsstrahlung Properties ---

# Turn electron bremsstrahlung reaction off
# properties.setBremsstrahlungModeOff()

# Set the bremsstrahlung angular distribution function
# ( DIPOLE, TABULAR, ??? )
properties.setBremsstrahlungAngularDistributionFunction( MonteCarlo.DIPOLE_DISTRIBUTION )

## --- Atomic Excitation Properties ---

# Turn electron atomic excitation reaction off
# properties.setAtomicExcitationModeOff()

##---------------------------------------------------------------------------##
## ---------------------------- GEOMETRY SETUP ----------------------------- ##
##---------------------------------------------------------------------------##

# Set geometry path and type
geometry_type = "DagMC" #(ROOT or DAGMC)
geomerty_path = "/home/lkersting/frensie/tests/hanson/geom3.sat"
# geometry_path = "/home/alexr/Research/transport/frensie-tests/hanson/geom3.sat"

# Set element zaid and name
zaid=79000
element="Au"

# Set geometry model properties
if geometry_type == "DagMC":
  model_properties = DagMC.DagMCModelProperties( geometry_path )
  model_properties.setFacetTolerance( 1e-3 )
  model_properties.useFastIdLookup()
  model_properties.setMaterialPropertyName( "mat" )
  model_properties.setDensityPropertyName( "rho" )
  # model_properties.setTerminationCellPropertyName( "graveyard" )
  # model_properties.setEstimatorPropertyName( "tally" )

  # Get model instance
  geom_model = DagMC.DagMCModel.getInstance()

elif geometry_type == "ROOT":
  model_properties = ROOT.RootModelProperties( geometry_path )

  # Get model instance
  geom_model = ROOT.RootModel.getInstance()
else:
  print "ERROR: geometry type ", geometry_type, " not supprted!"

##---------------------------------------------------------------------------##
## ----------------------- SIMULATION MANAGER SETUP ------------------------ ##
##---------------------------------------------------------------------------##

# Set the number of threads
threads = 1

# Set database directory path.
database_path = "/home/lkersting/frensie/build/packages/database.xml"
# database_path = "/home/alexr/Research/transport/build/packages/database.xml"
data_directory = os.path.dirname(database_path)

# Initialized database
database = Data.ScatteringCenterPropertiesDatabase(database_path)
scattering_center_definition_database = Collision.ScatteringCenterDefinitionDatabase()

# Set element properties
element_properties = database.getAtomProperties( Data.Au_ATOM )
print element_properties.photoatomicDataAvailable( Data.PhotoatomicDataProperties.ACE_EPR_FILE )



element_definition = scattering_center_definition_database.createDefinition( element, Data.ZAID(zaid) )


element_definition.setElectroatomicDataProperties(
          element_properties.getSharedElectroatomicDataProperties(
                     Data.ElectroatomicDataProperties.ACE_EPR_FILE, 14 ) )

material_definition_database = Collision.MaterialDefinitionDatabase()
material_definition_database.addDefinition( element, 1, (element,), (1.0,) )

# Initialized model
geom_model.initialize( model_properties )

material_ids = geom_model.getMaterialIds()
print geom_model.hasSurfaceEstimatorData()
print geom_model.hasCellEstimatorData()


# Set particle distribution
particle_distribution = ActiveRegion.StandardParticleDistribution( "source distribution" )

# Set the energy dimension distribution
delta_energy = Distribution.DeltaDistribution( 0.7 )
energy_dimension_dist = ActiveRegion.IndependentEnergyDimensionDistribution( delta_energy )
particle_distribution.setDimensionDistribution( energy_dimension_dist )

# Set the direction dimension distribution
particle_distribution.setDirection( 1.0, 0.0, 0.0 )

# Set the spatial dimension distribution
particle_distribution.setPosition( -0.5, 0.0, 0.0 )

particle_distribution.constructDimensionDistributionDependencyTree()

# Set source components
source_component = [ActiveRegion.StandardElectronSourceComponent( 0, 1.0, geom_model, particle_distribution )]

# Set source
source = ActiveRegion.StandardParticleSource( source_component )

# Set event handler
event_handler = Event.EventHandler( properties )

factory = Manager.ParticleSimulationManagerFactory( model,
                                                    source,
                                                    event_handler,
                                                    properties,
                                                    "test_sim",
                                                    "xml",
                                                    threads )

manager = factory.getManager()

MPI.removeAllLogs()
session.initializeLogs( 0, False )

manager.runSimulation()

# # Set the name reaction and extention
# name_extention=""
# name_reaction=""
# if not elastic_on:
#     name_reaction = name_reaction + "_no_elastic"
# elif [ ${DISTRIBUTION} = "Coupled" ]; then
#     name_extention="${name_extention}_${COUPLED_SAMPLING}"
#     if [ ${COUPLED_SAMPLING} = "2DM" ]; then
#         TITLE="${TITLE} M2D"
#     else
#         TITLE="${TITLE} ${COUPLED_SAMPLING}"
#     fi
# elif [ ${DISTRIBUTION} = "Decoupled" ]; then
#     name_extention="${name_extention}_decoupled"
#     TITLE="${TITLE} DE"
# fi
# if [ "${BREM_ON}" = "false" ]; then
#     name_reaction="${name_reaction}_no_brem"
# fi
# if [ "${IONIZATION_ON}" = "false" ]; then
#     name_reaction="${name_reaction}_no_ionization"
# fi
# if [ "${EXCITATION_ON}" = "false" ]; then
#     name_reaction="${name_reaction}_no_excitation"
# fi

# if not elastic_on:
#   properties.setElasticModeOff()

# # Set database directory path.
# EXTRA_ARGS=$@
# CROSS_SECTION_XML_PATH=/home/lkersting/software/mcnpdata/
# #CROSS_SECTION_XML_PATH=/home/software/mcnp6.2/MCNP_DATA/
# FRENSIE="/home/lkersting/frensie"

# INPUT="1"
# if [ "$#" -eq 1 ]; then
#     # Set the file type (1 = Native (default), 2 = ACE EPR14, 3 = ACE EPR12)
#     INPUT="$1"
# fi

# # Changing variables
# THREADS="112"
# # Number of histories 1e7
# HISTORIES="10000000"
# # Turn certain reactions on (true/false)
# ELASTIC_ON="true"
# BREM_ON="true"
# IONIZATION_ON="true"
# EXCITATION_ON="true"
# # Two D Interp Policy (logloglog, linlinlin, linlinlog)
# INTERP="logloglog"
# # Two D Grid Policy (1 = unit-base correlated, 2 = correlated, 3 = unit-base)
# SAMPLE=1
# # Elastic distribution ( Decoupled, Coupled, Hybrid )
# DISTRIBUTION="Coupled"
# # Elastic coupled sampling method ( 2D, 1D, 2DM )
# COUPLED_SAMPLING="2DM"


# ELEMENT="Au"
# ENERGY="15.7"
# NAME="native"

# zaid=79000

# database = Data.ScatteringCenterPropertiesDatabase(database_path)
# element_properties = database.getAtomProperties( Data.ZAID(zaid) )


# ELASTIC="-d ${DISTRIBUTION} -c ${COUPLED_SAMPLING}"
# REACTIONS=" -t ${ELASTIC_ON} -b ${BREM_ON} -i ${IONIZATION_ON} -a ${EXCITATION_ON}"
# SIM_PARAMETERS="-e ${ENERGY} -n ${HISTORIES} -l ${INTERP} -s ${SAMPLE} ${REACTIONS} ${ELASTIC}"

# if [ ${INPUT} -eq 2 ]; then
#     # Use ACE EPR14 data
#     NAME="epr14"
#     echo "Using ACE EPR14 data!"
# elif [ ${INPUT} -eq 3 ]; then
#     # Use ACE EPR12 data
#     NAME="ace"
#     echo "Using ACE EPR12 data!"
# elif [ ${DISTRIBUTION} = "Hybrid" ]; then
#     # Use Native moment preserving data
#     NAME="moments"
#     echo "Using Native Moment Preserving data!"
# else
#     # Use Native analog data
#     echo "Using Native analog data!"
# fi

# # Set the interp in title
# TITLE=""
# if [ "${INTERP}" = "logloglog" ]; then
#     TITLE="Log-log"
# elif [ "${INTERP}" = "linlinlin" ]; then
#     TITLE="Lin-lin"
# elif [ "${INTERP}" = "linlinlog" ]; then
#     TITLE="Lin-log"
# fi

# # Set the sampling name
# SAMPLE_NAME=""
# if [ ${SAMPLE} = 1 ]; then
#     SAMPLE_NAME="unit_correlated"
#     TITLE="${TITLE} Unit-base Correlated"
# elif [ ${SAMPLE} = 2 ]; then
#     SAMPLE_NAME="correlated"
#     TITLE="${TITLE} Correlated"
# elif [ ${SAMPLE} = 3 ]; then
#     SAMPLE_NAME="unit_base"
#     TITLE="${TITLE} Unit-base"
# fi

# # Set the name raction and extention
# name_extention=""
# name_reaction=""
# if [ "${ELASTIC_ON}" = "false" ]; then
#     name_reaction="${name_reaction}_no_elastic"
# elif [ ${DISTRIBUTION} = "Coupled" ]; then
#     name_extention="${name_extention}_${COUPLED_SAMPLING}"
#     if [ ${COUPLED_SAMPLING} = "2DM" ]; then
#         TITLE="${TITLE} M2D"
#     else
#         TITLE="${TITLE} ${COUPLED_SAMPLING}"
#     fi
# elif [ ${DISTRIBUTION} = "Decoupled" ]; then
#     name_extention="${name_extention}_decoupled"
#     TITLE="${TITLE} DE"
# fi
# if [ "${BREM_ON}" = "false" ]; then
#     name_reaction="${name_reaction}_no_brem"
# fi
# if [ "${IONIZATION_ON}" = "false" ]; then
#     name_reaction="${name_reaction}_no_ionization"
# fi
# if [ "${EXCITATION_ON}" = "false" ]; then
#     name_reaction="${name_reaction}_no_excitation"
# fi

# # .xml file paths.
# SOURCE="source.xml"
# EST="est.xml"
# GEOM="geom.xml"
# RSP="../rsp_fn.xml"
# INFO=$(python ../sim_info.py ${SIM_PARAMETERS} 2>&1)
# MAT=$(python ../mat.py -n ${ELEMENT} -t ${NAME} -i ${INTERP} 2>&1)

# # Make directory for the test results
# TODAY=$(date +%Y-%m-%d)

# if [ ${NAME} = "ace" ] || [ ${NAME} = "epr14" ]; then
#     DIR="results/${NAME}/${TODAY}"
#     NAME="hanson_${NAME}${name_reaction}"
#     TITLE="FRENSIE-ACE"
# else
#     DIR="results/${INTERP}/${TODAY}"

#     NAME="hanson_${NAME}_${INTERP}_${SAMPLE_NAME}${name_extention}${name_reaction}"
# fi

# mkdir -p $DIR

# echo "Running Facemc Hanson test with ${HISTORIES} particles on ${THREADS} threads:"
# RUN="mpiexec -n ${THREADS} ${FRENSIE}/bin/facemc-mpi --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME}"
# echo ${RUN}

# ${RUN} > ${DIR}/${NAME}.txt 2>&1

# echo "Removing old xml files:"
# rm ${INFO} ${MAT} ../ElementTree_pretty.pyc


# echo "Processing the results:"
# # Move file to the test results folder
# H5=${NAME}.h5
# NEW_NAME="${DIR}/${H5}"
# NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"
# mv ${H5} ${NEW_NAME}
# mv continue_run.xml ${NEW_RUN_INFO}

# python ./data_processor.py -f ${NEW_NAME} -t "${TITLE}"
# echo "Results will be in ./${DIR}"
