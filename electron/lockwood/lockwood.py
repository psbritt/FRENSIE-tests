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

# Set the element
atom=Data.Al_ATOM; element="Al"; zaid=13000
# Set the source energy
energy=0.314
# Set the test number
test_number=11

# Set the bivariate interpolation (LOGLOGLOG, LINLINLIN, LINLINLOG)
interpolation=MonteCarlo.LOGLOGLOG_INTERPOLATION

# Set the bivariate Grid Policy (UNIT_BASE_CORRELATED, CORRELATED, UNIT_BASE)
grid_policy=MonteCarlo.UNIT_BASE_CORRELATED_GRID

# Set the elastic distribution mode ( DECOUPLED, COUPLED, HYBRID )
mode=MonteCarlo.COUPLED_DISTRIBUTION

# Set the elastic coupled sampling method
# ( TWO_D_UNION, ONE_D_UNION, MODIFIED_TWO_D_UNION )
method=MonteCarlo.MODIFIED_TWO_D_UNION

# Set the data file type (ACE_EPR_FILE, Native_EPR_FILE)
file_type=Data.ElectroatomicDataProperties.Native_EPR_FILE

# Set the calorimeter thickness
calorimeter_thickness=5.050E-03

# Set the ranges
ranges=[ 0.0025, 0.0094, 0.0181, 0.0255, 0.0336, 0.0403, 0.0477, 0.0566, 0.0654, 0.0721, 0.0810, 0.0993 ]

# Set database directory path (for Denali)
if socket.gethostname() == "Denali":
  database_path = "/home/software/mcnpdata/database.xml"
  geometry_path = "/home/lkersting/frensie/tests/electron/lockwood/"
elif socket.gethostname() == "Elbrus": # Set database directory path (for Elbrus)
  database_path = "/home/software/mcnpdata/database.xml"
  geometry_path = "/home/ligross/frensie/tests/lockwood/"
else: # Set database directory path (for Cluster)
  database_path = "/home/lkersting/software/mcnp6.2/MCNP_DATA/database.xml"
  geometry_path = "/home/lkersting/dag_frensie/tests/electron/lockwood/"

geometry_path += element + "/" + element + "_" + str(energy) + "/dagmc/geom_" + str(test_number) + ".h5m"

# Run the simulation
def runSimulation( threads, histories, time ):

  ##--------------------------------------------------------------------------##
  ## ------------------------------ MPI Session ----------------------------- ##
  ##--------------------------------------------------------------------------##
  session = MPI.GlobalMPISession( len(sys.argv), sys.argv )
  Utility.removeAllLogs()
  session.initializeLogs( 0, True )

  properties = setSimulationProperties( threads, histories, time )

  ##--------------------------------------------------------------------------##
  ## ---------------------------- GEOMETRY SETUP ---------------------------- ##
  ##--------------------------------------------------------------------------##


  # Set geometry path and type
  geometry_type = "DagMC" #(ROOT or DAGMC)

  # Set geometry model properties
  if geometry_type == "DagMC":
    model_properties = DagMC.DagMCModelProperties( geometry_path )
    model_properties.useFastIdLookup()
    # model_properties.setMaterialPropertyName( "mat" )
    # model_properties.setDensityPropertyName( "rho" )
    # model_properties.setTerminationCellPropertyName( "graveyard" )
    # model_properties.setEstimatorPropertyName( "tally" )
  else:
    print "ERROR: geometry type ", geometry_type, " not supported!"

  # Construct model
  geom_model = DagMC.DagMCModel( model_properties )

  ##--------------------------------------------------------------------------##
  ## -------------------------- EVENT HANDLER SETUP -------------------------- ##
  ##--------------------------------------------------------------------------##

  # Set event handler
  event_handler = Event.EventHandler( properties )

  ## -------------------- Energy Deposition Calorimeter -------------------- ##

  # Setup a cell pulse height estimator
  estimator_id = 1
  cell_ids = [2]
  energy_deposition_estimator = Event.WeightAndEnergyMultipliedCellPulseHeightEstimator( estimator_id, 1.0, cell_ids )

  # Set the particle type
  energy_deposition_estimator.setParticleTypes( [MonteCarlo.ELECTRON] )

  # Add the estimator to the event handler
  event_handler.addEstimator( energy_deposition_estimator )

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
  particle_distribution.setDirection( 0.0, 0.0, 1.0 )

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
    processData( energy_deposition_estimator, name, title, ranges[test_number], calorimeter_thickness )

    print "Results will be in ", os.path.dirname(name)

##---------------------------------------------------------------------------##
## ------------------------- SIMULATION PROPERTIES ------------------------- ##
##---------------------------------------------------------------------------##
def setSimulationProperties( threads, histories, time ):

  properties = setup.setSimulationProperties( threads, histories, time, interpolation, grid_policy, mode, method )


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

  directory = element + "/" + directory

  if not os.path.exists(directory):
    os.makedirs(directory)

  return directory

##---------------------------------------------------------------------------##
## -------------------------- setSimulationName -----------------------------##
##---------------------------------------------------------------------------##
# Define a function for naming an electron simulation
def setSimulationName( properties, file_type ):
  extension, title = setup.setSimulationNameExtention( properties, file_type )
  name = "lockwood_" + str(test_number) + extension
  output = element + "/" + setup.getResultsDirectory(file_type, interpolation) + "/" + name

  return (output, title)

##----------------------------------------------------------------------------##
##------------------------------- processData --------------------------------##
##----------------------------------------------------------------------------##

# This function pulls pulse height estimator data outputs it to a separate file.
def processData( estimator, filename, title, range, calorimeter_thickness ):

  ids = list(estimator.getEntityIds())

  processed_data = estimator.getEntityBinProcessedData( ids[0] )
  energy_dep_mev = processed_data['mean']
  rel_error = processed_data['re']

  today = datetime.date.today()

  # Read the data file for surface tallies
  name = filename+"_energy_dep.txt"
  out_file = open(name, 'w')

  # Write the header to the file
  header = "# Range (g/cm2)\tEnergy Deposition (MeV cm2/g)\tError\t"+str(today)+"\n"
  out_file.write(header)

  # Write the energy deposition to the file
  data = str(range) + '\t' + str(energy_dep_mev/calorimeter_thickness) + '\t' + str(rel_error/calorimeter_thickness)
  out_file.write(data)
  out_file.close()
