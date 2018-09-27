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
file_type=Data.ElectroatomicDataProperties.ACE_EPR_FILE

# Set database directory path (for Denali)
if socket.gethostname() == "Denali":
  database_path = "/home/lkersting/frensie/build/packages/database.xml"
  geometry_path = "/home/lkersting/frensie/tests/hanson/geom.h5m"
else: # Set database directory path (for Cluster)
  database_path = "/home/lkersting/dag_frensie/FRENSIE/packages/database.xml"
  geometry_path = "/home/lkersting/dag_frensie/tests/hanson/geom.h5m"

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

  # Set geometry path and type
  geometry_type = "DagMC" #(ROOT or DAGMC)

  # Set element zaid and name
  zaid=79000
  element="Au"

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

  # Set model
  geom_model = DagMC.DagMCModel( model_properties )

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
  cosine_bins_1 = [ -1.0, 0.0, 0.848048096156426, 0.882126866017668, 0.913332365617192, 0.938191335922484, 0.951433341895538, 0.960585317886711, 0.968669911264357, 0.974526872786577, 0.978652704312051, 0.982024659632372, 0.985229115235059, 0.988520271746353, 0.991146155097021, 0.992986158373646, 0.995072889372028, 0.996419457128586, 0.997012445565730, 0.997743253476273, 0.998187693254492, 0.998555486558339, 0.998823128276774, 0.999166134342540, 0.999378583910478, 0.999701489781183, 0.999853726281158, 0.999958816007535, 1.0 ]

  transmission_current_estimator.setCosineDiscretization( cosine_bins_1 )

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
  cosine_bins_2 = [ -1.0, -0.999999, 1.0 ]
  reflection_current_estimator.setCosineDiscretization( cosine_bins_2 )

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
  delta_energy = Distribution.DeltaDistribution( 15.7 )
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
    processCosineBinData( transmission_current_estimator, cosine_bins_1, name, title )

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
    name = "hanson_" + name + name_reaction
    title = "FRENSIE-ACE"
  else:
    name = "hanson_" + interp + "_" + sample_name + name_extention + name_reaction

  output = createResultsDirectory() + "/" + name

  return (output, title)

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


# This function pulls cosine estimator data outputs it to a separate file.
def processCosineBinData( estimator, cosine_bins, filename, title ):

  ids = list(estimator.getEntityIds() )

  today = datetime.date.today()

  degree = numpy.pi/180.0
  square_degree = degree*degree

  # Read the data file for surface tallies
  name = filename+"_spectrum.txt"
  out_file = open(name, 'w')

  # Get the current and relative error
  current = estimator.getEntityBinDataFirstMoments( ids[0] )
  current_rel_error = estimator.getEntityBinDataSecondMoments( ids[0] )

  # Convert to #/Square Degree
  num_square_degree = [None] * len(current)
  num_square_degree_rel_error = [None] * len(current_rel_error)
  angle_bins = [None] * len(cosine_bins)

  size = len(current)
  for i in range(0, size ):
    k = size - i
    j = k - 1

    # Calculate the angle from the cosine_bins
    angle_bins[i] = numpy.arccos(float(cosine_bins[k]))/degree

    # Calculate the current in 1/square degrees
    cosine_diff = float(cosine_bins[k]) - float(cosine_bins[j])
    sterradians = 2.0*numpy.pi*cosine_diff
    num_per_ster = float(current[j])/sterradians
    num_square_degree[i] = num_per_ster*square_degree

    # Set the relative error
    num_square_degree_rel_error[i] = float(current_rel_error[j])

  # Set the last angle bin boundary
  angle_bins[size] = numpy.arccos(float(cosine_bins[0]))/degree

  # Write title to file
  out_file.write( "# " + title +"\n")
  # Write data header to file
  header = "# Degrees\t#/Square Degree\tError\t"+str(today)+"\n"
  out_file.write(header)

  # Write data to file
  for i in range(0, size):
      output = '%.4e' % angle_bins[i] + "\t" + \
              '%.16e' % num_square_degree[i] + "\t" + \
              '%.16e' % num_square_degree_rel_error[i] + "\n"
      out_file.write( output )

  # Write the last angle bin boundary
  output = '%.4e' % angle_bins[size] + "\n"
  out_file.write( output )
  out_file.close()

  # Read the raw data file for surface tallies
  name = filename+"_raw_spectrum.txt"
  out_file = open(name, 'w')

  size = len(cosine_bins)

  # Write title to file
  out_file.write( "# " + title +"\n")
  # Write data header to file
  header = "# Cosine\t#/Current\tError\t"+str(today)+"\n"
  out_file.write(header)

  current = numpy.insert( current, 0, 0.0 )
  current_rel_error = numpy.insert( current_rel_error, 0, 0.0 )

  # Write data to file
  for i in range(0, size):
      output = '%.4e' % cosine_bins[i] + "\t" + \
              '%.16e' % current[i] + "\t" + \
              '%.16e' % current_rel_error[i] + "\n"
      out_file.write( output )

  out_file.write( output )
  out_file.close()