#! /usr/bin/env python
import os
import sys
import numpy
import datetime
import socket
import PyFrensie.Data as Data
import PyFrensie.Data.Native as Native
import PyFrensie.Geometry.DagMC as DagMC
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

# Add the parent directory to the path
sys.path.insert(1,'../')
import simulation_setup as setup

##---------------------------------------------------------------------------##
## ---------------------- GLOBAL SIMULATION VARIABLES ---------------------- ##
##---------------------------------------------------------------------------##

# Set the source energy (0.001, 0.01, 0.1)
energy=0.01

# Set the bivariate interpolation (LOGLOGLOG, LINLINLIN, LINLINLOG)
interpolation=MonteCarlo.LOGLOGLOG_INTERPOLATION

# Set the bivariate Grid Policy (UNIT_BASE_CORRELATED, CORRELATED, UNIT_BASE)
grid_policy=MonteCarlo.UNIT_BASE_CORRELATED_GRID

# Set the elastic distribution mode ( DECOUPLED, COUPLED, HYBRID )
mode=MonteCarlo.DECOUPLED_DISTRIBUTION

# Set the elastic coupled sampling method
# ( TWO_D_UNION, ONE_D_UNION, MODIFIED_TWO_D_UNION )
method=MonteCarlo.ONE_D_UNION

# Set the data file type (ACE_EPR_FILE, Native_EPR_FILE)
file_type=Data.ElectroatomicDataProperties.Native_EPR_FILE

# Set database directory path (for Denali)
if socket.gethostname() == "Denali":
  database_path = "/home/software/mcnpdata/database.xml"
  geometry_path = "/home/lkersting/frensie/tests/electron/example/h_sphere.h5m"
else: # Set database directory path (for Cluster)
  database_path = "/home/lkersting/software/mcnp6.2/MCNP_DATA/database.xml"
  geometry_path = "/home/lkersting/dag_frensie/tests/electron/example/h_sphere.h5m"

# Run the simulation
def runSimulation( threads, histories, time ):

  ##---------------------------------------------------------------------------##
  ## ------------------------------ MPI Session ------------------------------ ##
  ##---------------------------------------------------------------------------##
  session = MPI.GlobalMPISession( len(sys.argv), sys.argv )
  Utility.removeAllLogs()
  session.initializeLogs( 0, True )

  properties = setSimulationProperties( histories, time )

  ##---------------------------------------------------------------------------##
  ## ---------------------------- GEOMETRY SETUP ----------------------------- ##
  ##---------------------------------------------------------------------------##

  # Set the element (H)
  atom=Data.H_ATOM; element="H"; zaid=1000

  # Set geometry path and type
  geometry_type = "DagMC" #(ROOT or DAGMC)

  # Set geometry model properties
  if geometry_type == "DagMC":
    model_properties = DagMC.DagMCModelProperties( geometry_path )
    model_properties.useFastIdLookup()
    model_properties.setMaterialPropertyName( "mat" )
    model_properties.setDensityPropertyName( "rho" )
    # model_properties.setTerminationCellPropertyName( "graveyard" )
    # model_properties.setEstimatorPropertyName( "tally" )
  else:
    print "ERROR: geometry type ", geometry_type, " not supported!"

  # Construct model
  geom_model = DagMC.DagMCModel( model_properties )

  ##---------------------------------------------------------------------------##
  ## -------------------------- EVENT HANDLER SETUP -------------------------- ##
  ##---------------------------------------------------------------------------##

  # Set event handler
  event_handler = Event.EventHandler( properties )

  # Set the energy bins
  if energy == 0.1:
    bins = list(Utility.doubleArrayFromString( "{ 1e-4, 5e-4, 198i, 1e-1}" ))
  elif energy == 0.01:
    bins = list(Utility.doubleArrayFromString( "{ 1e-4, 137i, 7e-3, 29i, 1e-2}" ))
  elif energy == 0.001:
    bins = list(Utility.doubleArrayFromString( "{ 1e-4, 197i, 1e-3}" ))
  else:
    print "ERROR: energy ", energy, " not supported!"

  ## -------------------------- Track Length Flux --------------------------- ##

  # Setup a track length flux estimator
  estimator_id = 1
  cell_ids = [1]
  track_flux_estimator = Event.WeightMultipliedCellTrackLengthFluxEstimator( estimator_id, 1.0, cell_ids, geom_model )

  # Set the particle type
  track_flux_estimator.setParticleTypes( [MonteCarlo.ELECTRON] )

  # Set the energy bins
  track_flux_estimator.setEnergyDiscretization( bins )

  # Add the estimator to the event handler
  event_handler.addEstimator( track_flux_estimator )

  ## ------------------------ Surface Flux Estimator ------------------------ ##

  # Setup a surface flux estimator
  estimator_id = 2
  surface_ids = [1]
  surface_flux_estimator = Event.WeightMultipliedSurfaceFluxEstimator( estimator_id, 1.0, surface_ids, geom_model )

  # Set the particle type
  surface_flux_estimator.setParticleTypes( [MonteCarlo.ELECTRON] )

  # Set the energy bins
  surface_flux_estimator.setEnergyDiscretization( bins )

  # Add the estimator to the event handler
  event_handler.addEstimator( surface_flux_estimator )

  ## ---------------------- Surface Current Estimator ----------------------- ##

  # Setup a surface current estimator
  estimator_id = 3
  surface_ids = [1]
  surface_current_estimator = Event.WeightMultipliedSurfaceCurrentEstimator( estimator_id, 1.0, surface_ids )

  # Set the particle type
  surface_current_estimator.setParticleTypes( [MonteCarlo.ELECTRON] )

  # Set the energy bins
  surface_current_estimator.setEnergyDiscretization( bins )

  # Add the estimator to the event handler
  event_handler.addEstimator( surface_current_estimator )

  ##--------------------------------------------------------------------------##
  ## ----------------------- SIMULATION MANAGER SETUP ----------------------- ##
  ##--------------------------------------------------------------------------##

  # Initialized database
  database = Data.ScatteringCenterPropertiesDatabase(database_path)
  scattering_center_definition_database = Collision.ScatteringCenterDefinitionDatabase()

  # Set element properties
  element_properties = database.getAtomProperties( atom )

  element_definition = scattering_center_definition_database.createDefinition( element, Data.ZAID(zaid) )


  version = 0
  if file_type == Data.ElectroatomicDataProperties.ACE_EPR_FILE:
    version = 14

  element_definition.setElectroatomicDataProperties(
            element_properties.getSharedElectroatomicDataProperties( file_type, version ) )

  material_definition_database = Collision.MaterialDefinitionDatabase()
  material_definition_database.addDefinition( element, 1, (element,), (1.0,) )

  # Get the material ids
  material_ids = geom_model.getMaterialIds()

  # Fill model
  model = Collision.FilledGeometryModel( database_path, scattering_center_definition_database, material_definition_database, properties, geom_model, True )

  # Set particle distribution
  particle_distribution = ActiveRegion.StandardParticleDistribution( "source distribution" )

  # Set the energy dimension distribution
  delta_energy = Distribution.DeltaDistribution( energy )
  energy_dimension_dist = ActiveRegion.IndependentEnergyDimensionDistribution( delta_energy )
  particle_distribution.setDimensionDistribution( energy_dimension_dist )

  # # Set the direction dimension distribution
  # particle_distribution.setDirection( 0.0, 0.0, 1.0 )

  # Set the spatial dimension distribution
  particle_distribution.setPosition( 0.0, 0.0, 0.0 )

  particle_distribution.constructDimensionDistributionDependencyTree()

  # Set source components
  source_component = [ActiveRegion.StandardElectronSourceComponent( 0, 1.0, geom_model, particle_distribution )]

  # Set source
  source = ActiveRegion.StandardParticleSource( source_component )

  # Set the archive type
  archive_type = "xml"

  name, title = setSimulationName( properties, file_type )

  factory = Manager.ParticleSimulationManagerFactory( model,
                                                      source,
                                                      event_handler,
                                                      properties,
                                                      name,
                                                      archive_type,
                                                      threads )

  manager = factory.getManager()

  Utility.removeAllLogs()
  session.initializeLogs( 0, False )

  manager.runSimulation()

  if session.rank() == 0:

    print "Processing the results:"
    processData( event_handler, name, title )

    print "Results will be in ", os.path.dirname(name)

##---------------------------------------------------------------------------##
## ------------------------- SIMULATION PROPERTIES ------------------------- ##
##---------------------------------------------------------------------------##
def setSimulationProperties( histories, time ):

  properties = setup.setSimulationProperties( histories, time, interpolation, grid_policy, mode, method )


  ## -------------------------- ELECTRON PROPERTIES ------------------------- ##

  # Turn certain reactions off
  # properties.setElasticModeOff()
  # properties.setElectroionizationModeOff()
  # properties.setBremsstrahlungModeOff()
  # properties.setAtomicExcitationModeOff()

  return properties

##----------------------------------------------------------------------------##
## ------------------------ Create Results Directory ------------------------ ##
##----------------------------------------------------------------------------##
def createResultsDirectory():

  directory = setup.getResultsDirectory(file_type, interpolation)

  if not os.path.exists(directory):
    os.makedirs(directory)

  return directory

##---------------------------------------------------------------------------##
## -------------------------- setSimulationName -----------------------------##
##---------------------------------------------------------------------------##
# Define a function for naming an electron simulation
def setSimulationName( properties, file_type ):
  extension, title = setup.setSimulationNameExtention( properties, file_type )
  name = "example" + extension
  output = setup.getResultsDirectory(file_type, interpolation) + "/" + name

  return (output, title)

##----------------------------------------------------------------------------##
##------------------------------- processData --------------------------------##
##----------------------------------------------------------------------------##
def processData( event_handler, filename, title ):

  # Process track flux data
  track_flux = event_handler.getEstimator( 2 )
  ids = list( track_flux.getEntityIds() )
  setup.processTrackFluxEnergyBinData( track_flux, ids[0], filename, title )

  # Process track flux data
  surface_flux = event_handler.getEstimator( 1 )
  ids = list( surface_flux.getEntityIds() )
  setup.processSurfaceFluxEnergyBinData( surface_flux, ids[0], filename, title )

  # Process track flux data
  surface_current = event_handler.getEstimator( 3 )
  ids = list( surface_current.getEntityIds() )
  setup.processSurfaceCurrentEnergyBinData( surface_current, ids[0], filename, title )