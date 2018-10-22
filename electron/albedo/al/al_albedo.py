#! /usr/bin/env python
import os
import sys
import numpy
import datetime
import socket

# Add the parent directory to the path
sys.path.insert(1,'../../')
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

# Set the source energy
energy=0.256

# Set the cutoff energy
cutoff_energy = 1e-4

# Set the bivariate interpolation (LOGLOGLOG, LINLINLIN, LINLINLOG)
interpolation=MonteCarlo.LOGLOGLOG_INTERPOLATION

# Set the bivariate Grid Policy (UNIT_BASE_CORRELATED, CORRELATED, UNIT_BASE)
grid_policy=MonteCarlo.UNIT_BASE_CORRELATED_GRID

# Set the elastic distribution mode ( DECOUPLED, COUPLED, HYBRID )
mode=MonteCarlo.COUPLED_DISTRIBUTION

# Set the elastic coupled sampling method
# ( TWO_D_UNION, ONE_D_UNION, MODIFIED_TWO_D_UNION )
method=MonteCarlo.TWO_D_UNION

# Set the data file type (ACE_EPR_FILE, Native_EPR_FILE)
file_type=Data.ElectroatomicDataProperties.Native_EPR_FILE

# Set database directory path (for Denali)
if socket.gethostname() == "Denali":
  database_path = "/home/software/mcnpdata/database.xml"
else: # Set database directory path (for Cluster)
  database_path = "/home/lkersting/software/mcnp6.2/MCNP_DATA/database.xml"

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

  # Set the possible test energies
  energies = [0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0008, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0035, 0.004, 0.0045, 0.005, 0.006, 0.0093, 0.01, 0.011, 0.0134, 0.015, 0.0173, 0.02, 0.0252, 0.03, 0.04, 0.0415, 0.05, 0.06, 0.0621, 0.07, 0.08, 0.0818, 0.1, 0.102, 0.121, 0.146, 0.172, 0.196, 0.2, 0.238, 0.256 ]

  # Set the element (Al)
  atom=Data.Al_ATOM; element="Al"; zaid=13000

  if not energy in energies:
    message="Energy "+ energy + " is currently not supported!"
    raise ValueError(message)

  ##--------------------------------------------------------------------------##
  ## ---------------------------- GEOMETRY SETUP ---------------------------- ##
  ##--------------------------------------------------------------------------##

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
    raise ValueError(message)

  # Set model
  geom_model = DagMC.DagMCModel( model_properties )

  ##--------------------------------------------------------------------------##
  ##--------------------------- EVENT HANDLER SETUP --------------------------##
  ##--------------------------------------------------------------------------##

  # Set event handler
  event_handler = Event.EventHandler( properties )

  ##----------------------- Surface Current Estimators -----------------------##

  # Setup a surface current estimator for the transmission current
  estimator_id = 1
  surface_ids = [4]
  current_estimator = Event.WeightMultipliedSurfaceCurrentEstimator( estimator_id, 1.0, surface_ids )

  # Set the particle type
  current_estimator.setParticleTypes( [MonteCarlo.ELECTRON] )

  # Set the cosine bins
  cosine_bins = [ -1.0, -0.99, 0.0, 1.0 ]

  current_estimator.setCosineDiscretization( cosine_bins )

  # Add the estimator to the event handler
  event_handler.addEstimator( current_estimator )

  ## ---------------------- Track Length Flux Estimator --------------------- ##

  # Setup a track length flux estimator
  estimator_id = 2
  cell_ids = [1]
  track_flux_estimator = Event.WeightMultipliedCellTrackLengthFluxEstimator( estimator_id, 1.0, cell_ids, geom_model )

  # Set the particle type
  track_flux_estimator.setParticleTypes( [MonteCarlo.ELECTRON] )

  # Set the energy bins
  energy_bins = numpy.logspace(numpy.log10(cutoff_energy), numpy.log10(energy), num=101) #[ cutoff_energy, 99l, energy ]
  track_flux_estimator.setEnergyDiscretization( energy_bins )

  # Add the estimator to the event handler
  event_handler.addEstimator( track_flux_estimator )

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

  # Set the direction dimension distribution
  particle_distribution.setDirection( 1.0, 0.0, 0.0 )

  # Set the spatial dimension distribution
  particle_distribution.setPosition( -20.0, 0.0, 0.0 )

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
    processCosineBinData( current_estimator, energy, name, title )

    print "Results will be in ", os.path.dirname(name)


##----------------------------------------------------------------------------##
## ------------------------- SIMULATION PROPERTIES -------------------------- ##
##----------------------------------------------------------------------------##
def setSimulationProperties( histories, time ):

  properties = setup.setSimulationProperties( histories, time, interpolation, grid_policy, mode, method )


  ## -------------------------- ELECTRON PROPERTIES ------------------------- ##

  # Set the min electron energy
  properties.setMinElectronEnergy( cutoff_energy )

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
  name = "al_albedo_" + str(energy) + extension
  if not cutoff_energy == 1e-4:
     name += "_" + str(cutoff_energy) + "_cutoff"

  output = setup.getResultsDirectory(file_type, interpolation) + "/" + name

  return (output, title)

##----------------------------------------------------------------------------##
##------------------------------- processData --------------------------------##
##----------------------------------------------------------------------------##

# This function pulls data from the .xml results file
def processData( results_file, raw_file_type ):

  Collision.FilledGeometryModel.setDefaultDatabasePath( os.path.dirname(database_path) )

  # Load data from file
  manager = Manager.ParticleSimulationManagerFactory( results_file ).getManager()
  event_handler = manager.getEventHandler()

  # Get the estimator data
  estimator_1 = event_handler.getEstimator( 1 )
  cosine_bins = estimator_1.getCosineDiscretization()

  # Get the simulation name and title
  properties = manager.getSimulationProperties()

  if raw_file_type == "ace":
    file_type = Data.ElectroatomicDataProperties.ACE_EPR_FILE
  elif raw_file_type == "native":
    file_type = Data.ElectroatomicDataProperties.Native_EPR_FILE
  else:
    ValueError
  filename, title = setSimulationName( properties, file_type )

  print "Processing the results:"
  processCosineBinData( estimator_1, cosine_bins, filename, title )

  print "Results will be in ", os.path.dirname(filename)

  filename = filename + "_reflection"
  # Get the estimator data
  estimator_2 = event_handler.getEstimator( 2 )
  cosine_bins = estimator_2.getCosineDiscretization()
  print cosine_bins

  processCosineBinData( estimator_2, cosine_bins, filename, title )

##----------------------------------------------------------------------------##
##--------------------------- processCosineBinData ---------------------------##
##----------------------------------------------------------------------------##

# This function pulls cosine estimator data outputs it to a separate file.
def processCosineBinData( estimator, energy, filename, title ):

  ids = list(estimator.getEntityIds() )
  if not 4 in ids:
    print "ERROR: estimator does not contain entity 4!"
    raise ValueError(message)

  today = datetime.date.today()

  # Read the data file for surface tallies
  name = filename+"_albedo.txt"
  out_file = open(name, 'w')

  # Get the current and relative error
  processed_data = estimator.getEntityBinProcessedData( 4 )
  current = processed_data['mean']
  current_rel_error = processed_data['re']
  cosine_bins = estimator.getCosineDiscretization()

  print cosine_bins
  print current
  print estimator.getEntityBinDataFirstMoments( 4 )

  # Write title to file
  out_file.write( "# " + title +"\n")
  # Write data header to file
  header = "# Energy (MeV)\tAlbedo\tError\t"+str(today)+"\n"
  out_file.write(header)

  # Write data to file
  output = '%.6e' % energy + "\t" + \
           '%.16e' % current[-1] + "\t" + \
           '%.16e' % current_rel_error[-1] + "\n"
  out_file.write( output )
  out_file.close()