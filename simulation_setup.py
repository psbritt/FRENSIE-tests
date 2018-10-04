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

##----------------------------------------------------------------------------##
## ------------------------- SIMULATION PROPERTIES -------------------------- ##
##----------------------------------------------------------------------------##
def setSimulationProperties( threads, histories, time, interpolation, grid_policy, elastic_mode, elastic_sampling_method ):

  properties = MonteCarlo.SimulationProperties()

  ## -------------------------- GENERAL PROPERTIES -------------------------- ##

  # Set the particle mode
  properties.setParticleMode( MonteCarlo.ELECTRON_MODE )

  # Set the number of histories
  properties.setNumberOfHistories( histories )

  # Change time from minutes to seconds
  time_sec = time*60

  # Set the wall time
  properties.setSimulationWallTime( time_sec )

  ## -------------------------- NEUTRON PROPERTIES -------------------------- ##

  ## -------------------------- PHOTON PROPERTIES --------------------------- ##

  ## ------------------------- ELECTRON PROPERTIES -------------------------- ##

  # Set the min electron energy in MeV (Default is 100 eV)
  properties.setMinElectronEnergy( 1e-4 )

  # Set the max electron energy in MeV (Default is 20 MeV)
  properties.setMaxElectronEnergy( 20.0 )

  # Set the bivariate interpolation (LOGLOGLOG, LINLINLIN, LINLINLOG)
  properties.setElectronTwoDInterpPolicy( interpolation )

  # Set the bivariate Grid Policy (UNIT_BASE_CORRELATED, CORRELATED, UNIT_BASE)
  properties.setElectronTwoDGridPolicy( grid_policy )

  # Set the electron evaluation tolerance (Default is 1e-8)
  properties.setElectronEvaluationTolerance( 1e-8 )

  ## --- Elastic Properties ---

  # Turn elastic electron scattering off
  # properties.setElasticModeOff()

  # Set the elastic distribution mode ( DECOUPLED, COUPLED, HYBRID )
  properties.setElasticElectronDistributionMode( elastic_mode )

  # Set the elastic coupled sampling method
  # ( TWO_D_UNION, ONE_D_UNION, MODIFIED_TWO_D_UNION )
  properties.setCoupledElasticSamplingMode( elastic_sampling_method )

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

##----------------------------------------------------------------------------##
## ---------------------- setSimulationNameExtention -------------------------##
##----------------------------------------------------------------------------##
# Define a function for naming an electron simulation
def setSimulationNameExtention( properties, file_type ):

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
      if properties.getCoupledElasticSamplingMode() == MonteCarlo.MODIFIED_TWO_D_UNION:
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
    name = "_" + name + name_reaction
    title = "FRENSIE-ACE"
  else:
    name = "_" + interp + "_" + sample_name + name_extention + name_reaction

  return (name, title)


##----------------------------------------------------------------------------##
## ------------------------ Create Results Directory ------------------------ ##
##----------------------------------------------------------------------------##
def createResultsDirectory(file_type, interpolation):

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

##----------------------------------------------------------------------------##
##---------------------- processTrackFluxEnergyBinData -----------------------##
##----------------------------------------------------------------------------##
def processTrackFluxEnergyBinData( estimator, est_id, filename, title ):

  processed_data = estimator.getEntityBinProcessedData( est_id )
  flux = processed_data['mean']
  rel_error = processed_data['re']
  energy_bins = estimator.getEnergyDiscretization()

  today = datetime.date.today()

  # Write the flux data to a file
  name = filename+"_track_flux.txt"
  out_file = open(name, 'w')

  # Write title to file
  out_file.write( "# " + title +"\n")

  # Write the header to the file
  header = "# Energy (MeV)\tTrack Flux (#/cm$^2$)\tError\t"+str(today)+"\n"
  out_file.write(header)

  data = str(energy_bins) + '\t' + str(flux) + '\t' + str(rel_error)
  out_file.write(data)
  out_file.close()

##----------------------------------------------------------------------------##
##--------------------- processSurfaceFluxEnergyBinData ----------------------##
##----------------------------------------------------------------------------##
def processSurfaceFluxEnergyBinData( estimator, est_id, filename, title ):

  processed_data = estimator.getEntityBinProcessedData( est_id )
  flux = processed_data['mean']
  rel_error = processed_data['re']
  energy_bins = estimator.getEnergyDiscretization()

  today = datetime.date.today()

  # Write the flux data to a file
  name = filename+"_flux.txt"
  out_file = open(name, 'w')

  # Write title to file
  out_file.write( "# " + title +"\n")

  # Write the header to the file
  header = "# Energy (MeV)\tSurface Flux (#/cm$^2$)\tError\t"+str(today)+"\n"
  out_file.write(header)

  data = str(energy_bins) + '\t' + str(flux) + '\t' + str(rel_error)
  out_file.write(data)
  out_file.close()

##----------------------------------------------------------------------------##
##-------------------- processSurfaceCurrentEnergyBinData --------------------##
##----------------------------------------------------------------------------##
def processSurfaceCurrentEnergyBinData( estimator, est_id, filename, title ):

  processed_data = estimator.getEntityBinProcessedData( est_id )
  current = processed_data['mean']
  rel_error = processed_data['re']
  energy_bins = estimator.getEnergyDiscretization()

  today = datetime.date.today()

  # Write the current data to a file
  name = filename+"_current.txt"
  out_file = open(name, 'w')

  # Write title to file
  out_file.write( "# " + title +"\n")

  # Write the header to the file
  header = "# Energy (MeV)\tSurface Current (#)\tError\t"+str(today)+"\n"
  out_file.write(header)

  data = str(energy_bins) + '\t' + str(current) + '\t' + str(rel_error)
  out_file.write(data)
  out_file.close()

##----------------------------------------------------------------------------##
##-------------------- processSurfaceCurrentCosineBinData --------------------##
##----------------------------------------------------------------------------##
def processSurfaceCurrentCosineBinData( estimator, est_id, filename, title ):

  processed_data = estimator.getEntityBinProcessedData( est_id )
  current = processed_data['mean']
  rel_error = processed_data['re']
  cosine_bins = estimator.getCosineDiscretization()

  today = datetime.date.today()

  # Write the current data to a file
  name = filename+"_current.txt"
  out_file = open(name, 'w')

  # Write title to file
  out_file.write( "# " + title +"\n")

  # Write the header to the file
  header = "# Cosine \tSurface Current (#)\tError\t"+str(today)+"\n"
  out_file.write(header)

  data = str(energy_bins) + '\t' + str(current) + '\t' + str(rel_error)
  out_file.write(data)
  out_file.close()