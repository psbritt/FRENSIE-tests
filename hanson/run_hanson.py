#! /usr/bin/env python
import os
import sys
import numpy
import PyFrensie.Data as Data
import PyFrensie.Data.Native as Native
import PyFrensie.Geometry.DagMC as DagMC
import PyFrensie.Geometry.ROOT as ROOT
import PyFrensie.Geometry as Geometry
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

##---------------------------------------------------------------------------##
## ------------------------------ MPI Session ------------------------------ ##
##---------------------------------------------------------------------------##
session = MPI.GlobalMPISession( len(sys.argv), sys.argv )
Utility.removeAllLogs()
session.initializeLogs( 0, True )

##---------------------------------------------------------------------------##
## ------------------------- SIMULATION VARIABLES -------------------------- ##
##---------------------------------------------------------------------------##

# Set the bivariate interpolation (LOGLOGLOG, LINLINLIN, LINLINLOG)
interp = MonteCarlo.LOGLOGLOG_INTERPOLATION

# Set the bivariate Grid Policy (UNIT_BASE_CORRELATED, CORRELATED, UNIT_BASE)
grid_policy = MonteCarlo.UNIT_BASE_CORRELATED_SAMPLING

# Set the elastic distribution mode ( DECOUPLED, COUPLED, HYBRID )
mode = MonteCarlo.COUPLED_DISTRIBUTION

# Set the elastic coupled sampling method
# ( TWO_D_UNION, ONE_D_UNION, MODIFIED_TWO_D_UNION )
method = MonteCarlo.TWO_D_UNION

# Set the data file type (ACE_EPR_FILE, Native_EPR_FILE)
file_type = Data.ElectroatomicDataProperties.ACE_EPR_FILE

# Set the number of histories
histories = 10

# Set the number of threads
threads = 1

# Set database directory path.
database_path = "/home/lkersting/frensie/build/packages/database.xml"

##---------------------------------------------------------------------------##
## ------------------------- SIMULATION PROPERTIES ------------------------- ##
##---------------------------------------------------------------------------##
properties = MonteCarlo.SimulationProperties()

## -------------------------- GENERAL PROPERTIES --------------------------- ##

# Set the particle mode
properties.setParticleMode( MonteCarlo.ELECTRON_MODE )

# Set the number of histories
properties.setNumberOfHistories( histories )

## -------------------------- NEUTRON PROPERTIES --------------------------- ##

## --------------------------- PHOTON PROPERTIES --------------------------- ##

## -------------------------- ELECTRON PROPERTIES -------------------------- ##

# Set the min electron energy in MeV (Default is 100 eV)
properties.setMinElectronEnergy( 1e-4 )

# Set the max electron energy in MeV (Default is 20 MeV)
properties.setMaxElectronEnergy( 20.0 )

# Set the bivariate interpolation (LOGLOGLOG, LINLINLIN, LINLINLOG)
properties.setElectronTwoDInterpPolicy( interp )

# Set the bivariate Grid Policy (UNIT_BASE_CORRELATED, CORRELATED, UNIT_BASE)
properties.setElectronTwoDSamplingPolicy( grid_policy )

# Set the electron evaluation tolerance (Default is 1e-7)
properties.setElectronEvaluationTolerance( 1e-8 )

## --- Elastic Properties ---

# Turn elastic electron scattering off
# properties.setElasticModeOff()

# Set the elastic distribution mode ( DECOUPLED, COUPLED, HYBRID )
properties.setElasticElectronDistributionMode( mode )

# Set the elastic coupled sampling method
# ( TWO_D_UNION, ONE_D_UNION, MODIFIED_TWO_D_UNION )
properties.setCoupledElasticSamplingMode( method )

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
geometry_path = "/home/lkersting/frensie/tests/hanson/geom3.sat"

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
  print "ERROR: geometry type ", geometry_type, " not supported!"

# Initialized model
geom_model.initialize( model_properties )

##---------------------------------------------------------------------------##
## -------------------------- EVENT HANDLER SETUP -------------------------- ##
##---------------------------------------------------------------------------##

# Set event handler
event_handler = Event.EventHandler( properties )

## -------------------- Transmission Current Estimator --------------------- ##

# Setup a surface current estimator for the transmission current
estimator_id = 1
surface_ids = [48]
transmission_current_estimator = Event.WeightMultipliedSurfaceCurrentEstimator( estimator_id, 1.0, surface_ids )

# Set the particle type
transmission_current_estimator.setParticleTypes( [MonteCarlo.ELECTRON] )

# Set the cosine bins
cosine_bins = [ -1.0, 0.0, 0.848048096156426, 0.882126866017668, 0.913332365617192, 0.938191335922484, 0.951433341895538, 0.960585317886711, 0.968669911264357, 0.974526872786577, 0.978652704312051, 0.982024659632372, 0.985229115235059, 0.988520271746353, 0.991146155097021, 0.992986158373646, 0.995072889372028, 0.996419457128586, 0.997012445565730, 0.997743253476273, 0.998187693254492, 0.998555486558339, 0.998823128276774, 0.999166134342540, 0.999378583910478, 0.999701489781183, 0.999853726281158, 0.999958816007535, 1.0 ]

transmission_current_estimator.setCosineDiscretization( cosine_bins )

# Add the estimator to the event handler
event_handler.addEstimator( transmission_current_estimator )

## --------------------- Reflection Current Estimator ---------------------- ##

# Setup a surface current estimator for the reflection current
estimator_id = 2
surface_ids = [46]
reflection_current_estimator = Event.WeightMultipliedSurfaceCurrentEstimator( estimator_id, 1.0, surface_ids )

# Set the particle type
reflection_current_estimator.setParticleTypes( [MonteCarlo.ELECTRON] )

# Set the cosine bins
cosine_bins = [ -1.0, -0.999999, 1.0 ]
reflection_current_estimator.setCosineDiscretization( cosine_bins )

# Add the estimator to the event handler
event_handler.addEstimator( reflection_current_estimator )

## ---------------------- Track Length Flux Estimator ---------------------- ##

# Setup a track length flux estimator
estimator_id = 3
cell_ids = [7]
track_flux_estimator = Event.WeightMultipliedCellTrackLengthFluxEstimator( estimator_id, 1.0, cell_ids, geom_model )

# Set the particle type
track_flux_estimator.setParticleTypes( [MonteCarlo.ELECTRON] )

# Set the energy bins
energy_bins = numpy.logspace(numpy.log10(1.5e-5), numpy.log10(15.7), num=101) #[ 1.5e-5, 99l, 15.7 ]
track_flux_estimator.setEnergyDiscretization( energy_bins )

# Add the estimator to the event handler
event_handler.addEstimator( track_flux_estimator )

##---------------------------------------------------------------------------##
## ----------------------- SIMULATION MANAGER SETUP ------------------------ ##
##---------------------------------------------------------------------------##

data_directory = os.path.dirname(database_path)

# Initialized database
database = Data.ScatteringCenterPropertiesDatabase(database_path)
scattering_center_definition_database = Collision.ScatteringCenterDefinitionDatabase()

# Set element properties
element_properties = database.getAtomProperties( Data.Au_ATOM )

element_definition = scattering_center_definition_database.createDefinition( element, Data.ZAID(zaid) )


version = 1
if file_type == Data.ElectroatomicDataProperties.ACE_EPR_FILE:
  version = 14

element_definition.setElectroatomicDataProperties(
          element_properties.getSharedElectroatomicDataProperties( file_type, version ) )

material_definition_database = Collision.MaterialDefinitionDatabase()
material_definition_database.addDefinition( element, 1, (element,), (1.0,) )

# Get the material ids
material_ids = geom_model.getMaterialIds()

# Fill model
model = Collision.FilledGeometryModel( data_directory, scattering_center_definition_database, material_definition_database, properties, geom_model, True )

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

# Set the archive type
archive_type = "xml"

factory = Manager.ParticleSimulationManagerFactory( model,
                                                    source,
                                                    event_handler,
                                                    properties,
                                                    "test_sim",
                                                    archive_type,
                                                    threads )

manager = factory.getManager()

Utility.removeAllLogs()
session.initializeLogs( 0, False )

manager.runSimulation()

# # Get the surface current estimator for the transmission current
# transmission_current_estimator = event_handler.getEstimator(1)

# # Get the surface current estimator for the reflection current
# reflection_current_estimator = event_handler.getEstimator(2)

# # Setup a track length flux estimator
# track_flux_estimator = event_handler.getEstimator(3)

surface_ids = transmission_current_estimator.getEntityIds()
print surface_ids

surface_0_first_moments = transmission_current_estimator.getEntityBinDataFirstMoments( 48 )

print surface_0_first_moments


# Define a function for naming an electron simulation
def electronSimulationName( properties ):


  # if [ ${INPUT} -eq 2 ]; then
  #     # Use ACE EPR14 data
  #     NAME="epr14"
  #     print "Using ACE EPR14 data!"
  # elif [ ${INPUT} -eq 3 ]; then
  #     # Use ACE EPR12 data
  #     NAME="ace"
  #     print "Using ACE EPR12 data!"
  # elif [ ${DISTRIBUTION} = "Hybrid" ]; then
  #     # Use Native moment preserving data
  #     NAME="moments"
  #     print "Using Native Moment Preserving data!"
  # else
  #     # Use Native analog data
  #     print "Using Native analog data!"
  # fi

  if file_type == Data.ElectroatomicDataProperties.ACE_EPR_FILE:
    # Use ACE EPR14 data
    NAME="epr14"
    print "Using ACE EPR14 data!"
  else:
    # Use Native analog data
    print "Using Native analog data!"


  # Set the interp in title
  TITLE = ""
  if properties.getElectronTwoDInterpPolicy() == MonteCarlo.LOGLOGLOG_INTERPOLATION:
      TITLE = "Log-log"
  elif properties.getElectronTwoDInterpPolicy() == MonteCarlo.LINLINLIN_INTERPOLATION:
      TITLE = "Lin-lin"
  else:
      TITLE = "Lin-log"

  # Set the sampling name
  SAMPLE_NAME=""
  if properties.getElectronTwoDSamplingPolicy() == MonteCarlo.UNIT_BASE_CORRELATED_SAMPLING:
      SAMPLE_NAME = "unit_correlated"
      TITLE += " Unit-base Correlated"
  elif properties.getElectronTwoDSamplingPolicy() == MonteCarlo.CORRELATED_SAMPLING:
      SAMPLE_NAME = "correlated"
      TITLE += " Correlated"
  else:
      SAMPLE_NAME = "unit_base"
      TITLE += " Unit-base"

  # Set the name reaction and extention
  name_extention = ""
  name_reaction = ""
  if properties.isElasticModeOn():
    if properties.getElasticElectronDistributionMode() == MonteCarlo.COUPLED_DISTRIBUTION:
      name_extention += "_coupled"
      if properties.getCoupledElasticSamplingMode() == MonteCarlo.MODIFIED_TWO_D_UNION:
        TITLE += " M2D"
      elif properties.getCoupledElasticSamplingMode() == MonteCarlo.TWO_D_UNION:
          TITLE += " 2D"
      else:
          TITLE += " 1D"
    elif properties.getElasticElectronDistributionMode() == MonteCarlo.DECOUPLED_DISTRIBUTION:
      name_extention += "_decoupled"
      TITLE += " DE"
    elif properties.getElasticElectronDistributionMode() == MonteCarlo.HYBRID_DISTRIBUTION:
      name_extention += "_hybrid"
      TITLE += " HE"
  else:
    name_reaction = name_reaction + "_no_elastic"

  if not properties.isBremsstrahlungModeOn():
    name_reaction += "_no_brem"
  if not properties.isElectroionizationModeOn():
      name_reaction += "_no_ionization"
  if not properties.isAtomicExcitationModeOn():
      name_reaction += "_no_excitation"


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
#     print "Using ACE EPR14 data!"
# elif [ ${INPUT} -eq 3 ]; then
#     # Use ACE EPR12 data
#     NAME="ace"
#     print "Using ACE EPR12 data!"
# elif [ ${DISTRIBUTION} = "Hybrid" ]; then
#     # Use Native moment preserving data
#     NAME="moments"
#     print "Using Native Moment Preserving data!"
# else
#     # Use Native analog data
#     print "Using Native analog data!"
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

# print "Running Facemc Hanson test with ${HISTORIES} particles on ${THREADS} threads:"
# RUN="mpiexec -n ${THREADS} ${FRENSIE}/bin/facemc-mpi --sim_info=${INFO} --geom_def=${GEOM} --mat_def=${MAT} --resp_def=${RSP} --est_def=${EST} --src_def=${SOURCE} --cross_sec_dir=${CROSS_SECTION_XML_PATH} --simulation_name=${NAME}"
# print ${RUN}

# ${RUN} > ${DIR}/${NAME}.txt 2>&1

# print "Removing old xml files:"
# rm ${INFO} ${MAT} ../ElementTree_pretty.pyc


# print "Processing the results:"
# # Move file to the test results folder
# H5=${NAME}.h5
# NEW_NAME="${DIR}/${H5}"
# NEW_RUN_INFO="${DIR}/continue_run_${NAME}.xml"
# mv ${H5} ${NEW_NAME}
# mv continue_run.xml ${NEW_RUN_INFO}

# python ./data_processor.py -f ${NEW_NAME} -t "${TITLE}"
# print "Results will be in ./${DIR}"
