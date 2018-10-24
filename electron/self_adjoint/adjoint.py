#! /usr/bin/env python
import os
import sys
import numpy
import datetime
import socket

# Add the parent directory to the path
sys.path.insert(1,'../')
import simulation_setup as setup
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

##---------------------------------------------------------------------------##
## ---------------------- GLOBAL SIMULATION VARIABLES ---------------------- ##
##---------------------------------------------------------------------------##

# Set the element
atom=Data.H_ATOM; element="H"; zaid=1000
# Set the forward source energy ( 0.001, 0.01, 0.1 )
energy=0.01

# Set the min energy (default is 100 eV )
min_energy=1e-4

# Set the elastic distribution mode ( DECOUPLED, COUPLED, HYBRID )
mode=MonteCarlo.COUPLED_DISTRIBUTION

# Set the elastic coupled sampling method
# ( TWO_D_UNION, ONE_D_UNION, MODIFIED_TWO_D_UNION )
method=MonteCarlo.MODIFIED_TWO_D_UNION

# Set database directory path (for Denali)
if socket.gethostname() == "Denali":
  database_path = "/home/software/mcnpdata/database.xml"
  database_path = "/home/lkersting/frensie/build/packages/database.xml"
elif socket.gethostname() == "Elbrus": # Set database directory path (for Elbrus)
  database_path = "/home/software/mcnpdata/database.xml"
else: # Set database directory path (for Cluster)
  database_path = "/home/lkersting/software/mcnp6.2/MCNP_DATA/database.xml"
  database_path = "/home/lkersting/dag_frensie/build/packages/database.xml"

geometry_path = os.path.dirname(os.path.realpath(__file__)) + "/geom.h5m"

# Run the simulation
def runSimulation( threads, histories, time ):

  ##--------------------------------------------------------------------------##
  ## ------------------------------ MPI Session ----------------------------- ##
  ##--------------------------------------------------------------------------##
  session = MPI.GlobalMPISession( len(sys.argv), sys.argv )
  Utility.removeAllLogs()
  session.initializeLogs( 0, True )

  properties = setSimulationProperties( histories, time )

  ##--------------------------------------------------------------------------##
  ## ---------------------------- GEOMETRY SETUP ---------------------------- ##
  ##--------------------------------------------------------------------------##


  # Set geometry path and type
  geometry_type = "DagMC" #(ROOT or DAGMC)

  # Set geometry model properties
  if geometry_type == "DagMC":
    model_properties = DagMC.DagMCModelProperties( geometry_path )
    model_properties.useFastIdLookup()
  else:
    print "ERROR: geometry type ", geometry_type, " not supported!"

  # Construct model
  geom_model = DagMC.DagMCModel( model_properties )

  ##--------------------------------------------------------------------------##
  ## -------------------------- EVENT HANDLER SETUP -------------------------- ##
  ##--------------------------------------------------------------------------##

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
  forward_track_flux_estimator = Event.WeightMultipliedCellTrackLengthFluxEstimator( estimator_id, 1.0, cell_ids, geom_model )

  # Set the particle type
  forward_track_flux_estimator.setParticleTypes( [MonteCarlo.ELECTRON] )

  # Set the energy bins
  forward_track_flux_estimator.setEnergyDiscretization( bins )

  # Add the estimator to the event handler
  event_handler.addEstimator( forward_track_flux_estimator )

  # Setup an adjoint track length flux estimator
  estimator_id = 4
  cell_ids = [1]
  track_flux_estimator = Event.WeightMultipliedCellTrackLengthFluxEstimator( estimator_id, 1.0, cell_ids, geom_model )

  # Set the particle type
  track_flux_estimator.setParticleTypes( [MonteCarlo.ADJOINT_ELECTRON] )

  # Set the energy bins
  track_flux_estimator.setSourceEnergyDiscretization( bins )

  # Add the estimator to the event handler
  event_handler.addEstimator( track_flux_estimator )

  ## ------------------------ Surface Flux Estimator ------------------------ ##

  # Setup a surface flux estimator
  estimator_id = 2
  surface_ids = [1]
  forward_surface_flux_estimator = Event.WeightMultipliedSurfaceFluxEstimator( estimator_id, 1.0, surface_ids, geom_model )

  # Set the particle type
  forward_surface_flux_estimator.setParticleTypes( [MonteCarlo.ELECTRON] )

  # Set the energy bins
  forward_surface_flux_estimator.setEnergyDiscretization( bins )

  # Add the estimator to the event handler
  event_handler.addEstimator( forward_surface_flux_estimator )

  # Setup an adjoint surface flux estimator
  estimator_id = 5
  surface_ids = [1]
  surface_flux_estimator = Event.WeightMultipliedSurfaceFluxEstimator( estimator_id, 1.0, surface_ids, geom_model )

  # Set the particle type
  surface_flux_estimator.setParticleTypes( [MonteCarlo.ADJOINT_ELECTRON] )

  # Set the energy bins
  surface_flux_estimator.setSourceEnergyDiscretization( bins )

  # Create response function
  delta_energy = Distribution.DeltaDistribution( energy )
  particle_response_function = ActiveRegion.EnergyParticleResponseFunction( delta_energy )
  response_function = ActiveRegion.StandardParticleResponse( particle_response_function )

  # Set the response function
  surface_flux_estimator.addResponseFunction( response_function )

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

  # Setup an adjoint surface current estimator
  estimator_id = 6
  surface_ids = [1]
  surface_current_estimator = Event.WeightMultipliedSurfaceCurrentEstimator( estimator_id, 1.0, surface_ids )

  # Set the particle type
  surface_current_estimator.setParticleTypes( [MonteCarlo.ADJOINT_ELECTRON] )

  # Set the energy bins
  surface_current_estimator.setSourceEnergyDiscretization( bins )

  # Add the estimator to the event handler
  event_handler.addEstimator( surface_current_estimator )

  ## -------------------------- Particle Tracker ---------------------------- ##

  particle_tracker = Event.ParticleTracker( 0, 1000 )

  # Add the particle tracker to the event handler
  event_handler.addParticleTracker( particle_tracker )

  ##--------------------------------------------------------------------------##
  ## ----------------------- SIMULATION MANAGER SETUP ------------------------ ##
  ##--------------------------------------------------------------------------##

  # Initialized database
  database = Data.ScatteringCenterPropertiesDatabase(database_path)
  scattering_center_definition_database = Collision.ScatteringCenterDefinitionDatabase()

  # Set element properties
  element_properties = database.getAtomProperties( atom )

  element_definition = scattering_center_definition_database.createDefinition( element, Data.ZAID(zaid) )


  version = 0
  file_type = Data.AdjointElectroatomicDataProperties.Native_EPR_FILE

  element_definition.setAdjointElectroatomicDataProperties(
            element_properties.getSharedAdjointElectroatomicDataProperties( file_type, version ) )

  material_definition_database = Collision.MaterialDefinitionDatabase()
  material_definition_database.addDefinition( element, 1, (element,), (1.0,) )

  # Fill model
  model = Collision.FilledGeometryModel( database_path, scattering_center_definition_database, material_definition_database, properties, geom_model, True )

  # Set particle distribution
  particle_distribution = ActiveRegion.StandardParticleDistribution( "source distribution" )

  # Set the energy dimension distribution
  uniform_energy = Distribution.UniformDistribution( min_energy, energy )
  energy_dimension_dist = ActiveRegion.IndependentEnergyDimensionDistribution( uniform_energy )
  particle_distribution.setDimensionDistribution( energy_dimension_dist )

  # Set the direction dimension distribution
  # particle_distribution.setDirection( 0.0, 0.0, 1.0 )

  # Set the spatial dimension distribution
  particle_distribution.setPosition( 0.0, 0.0, 0.0 )

  particle_distribution.constructDimensionDistributionDependencyTree()

  # Set source components
  source_component = [ActiveRegion.StandardAdjointElectronSourceComponent( 0, 1.0, model, particle_distribution )]

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

  properties = setup.setAdjointSimulationProperties( histories, time, mode, method )

  # Set the min electron energy in MeV (Default is 100 eV)
  properties.setMinElectronEnergy( min_energy )

  # Set the max electron energy in MeV (Default is 20 MeV)
  properties.setMaxElectronEnergy( energy )


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

  date = str(datetime.datetime.today()).split()[0]
  directory = "results/" + date

  if not os.path.exists(directory):
    os.makedirs(directory)

  return directory

##---------------------------------------------------------------------------##
## -------------------------- setSimulationName -----------------------------##
##---------------------------------------------------------------------------##
# Define a function for naming an electron simulation
def setSimulationName( properties, file_type ):
  extension, title = setup.setSimulationNameExtention( properties, file_type )
  name = "adjoint" + extension
  date = str(datetime.datetime.today()).split()[0]

  output = "results/" + date + "/" + name

  return (output, title)

##----------------------------------------------------------------------------##
##------------------------------- processData --------------------------------##
##----------------------------------------------------------------------------##
def processData( event_handler, filename, title ):

  # -- Process the Forward Data -- #

  # Process track flux data
  track_flux = event_handler.getEstimator( 1 )
  ids = list( track_flux.getEntityIds() )
  setup.processTrackFluxEnergyBinData( track_flux, ids[0], filename, title )

  # Process surface flux data
  surface_flux = event_handler.getEstimator( 2 )
  ids = list( surface_flux.getEntityIds() )
  setup.processSurfaceFluxEnergyBinData( surface_flux, ids[0], filename, title )

  # Process surface current data
  surface_current = event_handler.getEstimator( 3 )
  ids = list( surface_current.getEntityIds() )
  setup.processSurfaceCurrentEnergyBinData( surface_current, ids[0], filename, title )

  # -- Process the Adjoint Data -- #

  # Process track flux data
  track_flux = event_handler.getEstimator( 4 )
  ids = list( track_flux.getEntityIds() )
  setup.processTrackFluxSourceEnergyBinData( track_flux, ids[0], filename, title )

  # Process surface flux data
  surface_flux = event_handler.getEstimator( 5 )
  ids = list( surface_flux.getEntityIds() )
  setup.processSurfaceFluxSourceEnergyBinData( surface_flux, ids[0], filename, title )

  # Process surface current data
  surface_current = event_handler.getEstimator( 6 )
  ids = list( surface_current.getEntityIds() )
  setup.processSurfaceCurrentSourceEnergyBinData( surface_current, ids[0], filename, title )
