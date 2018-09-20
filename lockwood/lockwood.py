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

##---------------------------------------------------------------------------##
## ---------------------- GLOBAL SIMULATION VARIABLES ---------------------- ##
##---------------------------------------------------------------------------##

# Al: 0.314 MeV & tests 0-11, 0.512 MeV & test 0-17, 1.033 MeV & tests 0-25

# Set the element (Al)
atom=Data.Al_ATOM; element="Al"; zaid=13000
# Set the source energy (0.314, 0.512, 1.033)
energy=0.314
# Set the test number (0.314: 0-11, 0.512: 0-17, 1.033: 0-25)
test_number=0

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
  database_path = "/home/lkersting/frensie/build/packages/database.xml"
  geometry_path = "/home/lkersting/frensie/tests/lockwood/"
else: # Set database directory path (for Cluster)
  database_path = "/home/lkersting/dag_frensie/FRENSIE/packages/database.xml"
  geometry_path = "/home/lkersting/dag_frensie/tests/lockwood/"

geometry_path += element + "/" + element + "_" + str(energy) + "/dagmc/geom_" + str(test_number) + ".h5m"

##---------------------------------------------------------------------------##
## ------------------------- SIMULATION PROPERTIES ------------------------- ##
##---------------------------------------------------------------------------##
def setSimulationProperties( threads, histories, time ):
  properties = MonteCarlo.SimulationProperties()

  ## -------------------------- GENERAL PROPERTIES --------------------------- ##

  # Set the particle mode
  properties.setParticleMode( MonteCarlo.ELECTRON_MODE )

  # Set the number of histories
  properties.setNumberOfHistories( histories )

  # Change time from minutes to seconds
  time_sec = time*60

  # Set the wall time
  properties.setSimulationWallTime( time_sec )

  ## -------------------------- NEUTRON PROPERTIES --------------------------- ##

  ## --------------------------- PHOTON PROPERTIES --------------------------- ##

  ## -------------------------- ELECTRON PROPERTIES -------------------------- ##

  # Set the min electron energy in MeV (Default is 100 eV)
  properties.setMinElectronEnergy( 1e-4 )

  # Set the max electron energy in MeV (Default is 20 MeV)
  properties.setMaxElectronEnergy( 20.0 )

  # Set the bivariate interpolation (LOGLOGLOG, LINLINLIN, LINLINLOG)
  properties.setElectronTwoDInterpPolicy( interpolation )

  # Set the bivariate Grid Policy (UNIT_BASE_CORRELATED, CORRELATED, UNIT_BASE)
  properties.setElectronTwoDGridPolicy( grid_policy )

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

  return properties

##---------------------------------------------------------------------------##
## ------------------------- SIMULATION PROPERTIES ------------------------- ##
##---------------------------------------------------------------------------##
def createResultsDirectory():

  if file_type == Data.ElectroatomicDataProperties.ACE_EPR_FILE:
    # Use ACE EPR14 data
    name = "epr14"
  else:
    # Use Native analog data
    name = ""

  # Set the interp in results directory
  title = ""
  if interpolation == MonteCarlo.LOGLOGLOG_INTERPOLATION:
      interp = "loglog"
  elif interpolation == MonteCarlo.LINLINLIN_INTERPOLATION:
      interp = "linlin"
  else:
      interp = "linlog"

  date = str(datetime.datetime.today()).split()[0]
  if name == "epr14":
    directory = "results/" + name + "/" + date
  else:
    directory = "results/" + interp + "/" + date

  if not os.path.exists(directory):
    os.makedirs(directory)

  return directory

# Run the simulation
def runSimulation( threads, histories, time ):

  ##---------------------------------------------------------------------------##
  ## ------------------------------ MPI Session ------------------------------ ##
  ##---------------------------------------------------------------------------##
  session = MPI.GlobalMPISession( len(sys.argv), sys.argv )
  Utility.removeAllLogs()
  session.initializeLogs( 0, True )

  properties = setSimulationProperties( threads, histories, time )

  ##---------------------------------------------------------------------------##
  ## ---------------------------- GEOMETRY SETUP ----------------------------- ##
  ##---------------------------------------------------------------------------##

  if element == "Al":
    calorimeter_thickness = 5.050E-03

    if energy == 0.314:
        # ranges for 0.314 MeV source (g/cm2)
        ranges = [ 0.0025, 0.0094, 0.0181, 0.0255, 0.0336, 0.0403, 0.0477, 0.0566, 0.0654, 0.0721, 0.0810, 0.0993 ]
    elif energy == 0.521:
        # ranges for 0.521 MeV source (g/cm2)
        ranges = [ 0.0025, 0.0094, 0.0180, 0.0255, 0.0335, 0.0405, 0.0475, 0.0566, 0.0653, 0.0721, 0.0807, 0.0992, 0.1111, 0.1259, 0.1439, 0.1596, 0.1825, 0.2125 ]
    elif energy == 1.033:
        # ranges for 1.033 MeV source (g/cm2)
        ranges = [ 0.0025, 0.0094, 0.0180, 0.0255, 0.0336, 0.0402, 0.0476, 0.0562, 0.0654, 0.0723, 0.0808, 0.0990, 0.1110, 0.1257, 0.1440, 0.1593, 0.1821, 0.2122, 0.2225, 0.2452, 0.2521, 0.2908, 0.3141, 0.3533, 0.4188, 0.4814 ]
    else:
        message="Energy "+ energy + " is currently not supported!"
        raise ValueError(message)
  else:
      message="Element " + element +  " is currently not supported!"
      raise ValueError(message)

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

  ##---------------------------------------------------------------------------##
  ## -------------------------- EVENT HANDLER SETUP -------------------------- ##
  ##---------------------------------------------------------------------------##

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

  ##---------------------------------------------------------------------------##
  ## ----------------------- SIMULATION MANAGER SETUP ------------------------ ##
  ##---------------------------------------------------------------------------##

  data_directory = os.path.dirname(database_path)

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
  model = Collision.FilledGeometryModel( data_directory, scattering_center_definition_database, material_definition_database, properties, geom_model, True )

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
## -------------------------- setSimulationName -----------------------------##
##---------------------------------------------------------------------------##
# Define a function for naming an electron simulation
def setSimulationName( properties, file_type ):

  if file_type == Data.ElectroatomicDataProperties.ACE_EPR_FILE:
    # Use ACE EPR14 data
    name = "epr14"
  else:
    # Use Native analog data
    name = ""

  # Set the interp in title
  title = ""
  if properties.getElectronTwoDInterpPolicy() == MonteCarlo.LOGLOGLOG_INTERPOLATION:
      interp = "loglog"
      title = "Log-log"
  elif properties.getElectronTwoDInterpPolicy() == MonteCarlo.LINLINLIN_INTERPOLATION:
      interp = "linlin"
      title = "Lin-lin"
  else:
      interp = "linlog"
      title = "Lin-log"

  # Set the sampling name
  sample_name=""
  if properties.getElectronTwoDGridPolicy() == MonteCarlo.UNIT_BASE_CORRELATED_GRID:
      sample_name = "unit_correlated"
      title += " Unit-base Correlated"
  elif properties.getElectronTwoDGridPolicy() == MonteCarlo.CORRELATED_GRID:
      sample_name = "correlated"
      title += " Correlated"
  else:
      sample_name = "unit_base"
      title += " Unit-base"

  # Set the name reaction and extention
  name_extention = ""
  name_reaction = ""
  if properties.isElasticModeOn():
    if properties.getElasticElectronDistributionMode() == MonteCarlo.COUPLED_DISTRIBUTION:
      if properties.getCoupledElasticSamplingMode() == MonteCarlo.SIMPLIFIED_UNION:
        name_extention += "_m2d"
        title += " M2D"
      elif properties.getCoupledElasticSamplingMode() == MonteCarlo.TWO_D_UNION:
        name_extention += "_2d"
        title += " 2D"
      else:
        name_extention += "_1d"
        title += " 1D"
    elif properties.getElasticElectronDistributionMode() == MonteCarlo.DECOUPLED_DISTRIBUTION:
      name_extention += "_decoupled"
      title += " DE"
    elif properties.getElasticElectronDistributionMode() == MonteCarlo.HYBRID_DISTRIBUTION:
      name_extention += "_hybrid"
      title += " HE"
  else:
    name_reaction = name_reaction + "_no_elastic"

  if not properties.isBremsstrahlungModeOn():
    name_reaction += "_no_brem"
  if not properties.isElectroionizationModeOn():
      name_reaction += "_no_ionization"
  if not properties.isAtomicExcitationModeOn():
      name_reaction += "_no_excitation"

  date = str(datetime.datetime.today()).split()[0]
  if name == "epr14":
    name = "lockwood_" + str(test_number) + "_" + name + name_reaction
    title = "FRENSIE-ACE"
  else:
    name = "lockwood_" + str(test_number) + "_" + interp + "_" + sample_name + name_extention + name_reaction

  output = createResultsDirectory() + "/" + name

  return (output, title)

# This function pulls pulse height estimator data outputs it to a separate file.
def processData( estimator, filename, title, range, calorimeter_thickness ):

  ids = estimator.getEntityIds()

  energy_dep_mev = estimator.getEntityBinDataFirstMoments(ids[0])[0]
  rel_error = estimator.getEntityBinDataSecondMoments(ids[0])[0]

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
