import numpy
import os
import sys
from argparse import *
from estimators import *
import PyFrensie.Geometry as Geometry
import PyFrensie.Geometry.DagMC as DagMC
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
import PyFrensie.Utility.Mesh as Mesh

# Produce an importance sampled source for forward/adjoint particles
def getImportanceSource( importance_dictionary, \
                         real_spatial_distribution,
                         spatial_bounds,
                         real_energy_distribution,
                         energy_bounds,\
                         real_direction_distribution,\
                         direction_bounds,
                         source_mesh,
                         source_direction_discretization,
                         particle_type,\
                         model):
  
  # Initial instantiation
  importance_sampled_particle_distribution = ActiveRegion.GenericHistogramImportanceParticleDistribution(" importance source distribution")

  # Set mesh and direction discretization objects for particle distribution
  importance_sampled_particle_distribution.setMeshIndexDimensionDistributionObject(source_mesh)
  importance_sampled_particle_distribution.setDirectionIndexDimensionDistributionObject(source_direction_discretization)
  
  # Set up an independent distribution that I'm not actually using (because I designed it this way for some reason, time=0 is just the default anyway)
  raw_time_distribution = Distribution.DeltaDistribution(0.0)
  time_distribution = ActiveRegion.IndependentTimeDimensionDistribution(raw_time_distribution)
  importance_sampled_particle_distribution.setIndependentDimensionDistribution(time_distribution, True)

  # Set up dimension order
  dimension_order_vector = ActiveRegion.dimensionOrderArray()
  dimension_order_vector.push_back(ActiveRegion.SPATIAL_INDEX_DIMENSION)
  dimension_order_vector.push_back(ActiveRegion.DIRECTION_INDEX_DIMENSION)
  dimension_order_vector.push_back(ActiveRegion.ENERGY_DIMENSION)

  # Set up dimension boundary map
  dimension_boundary_map = {ActiveRegion.SPATIAL_INDEX_DIMENSION: spatial_bounds, \
                            ActiveRegion.DIRECTION_INDEX_DIMENSION: direction_bounds, \
                            ActiveRegion.ENERGY_DIMENSION: energy_bounds}

  # Initialize some useful variables so code is less messy
  num_spatial_elements = len(spatial_bounds)-1
  num_direction_elements = len(direction_bounds)-1
  num_energy_elements = len(energy_bounds)-1

  # Set up importance distribution map
  spatial_distribution_vector = ActiveRegion.importanceDistributionPointerVector()
  direction_distribution_vector = ActiveRegion.importanceDistributionPointerVector()
  energy_distribution_vector = ActiveRegion.importanceDistributionPointerVector()
  
  # Set up distributions
  mesh_value_list = []
  for mesh_element in range(num_spatial_elements):
    mesh_element_direction_sum = 0
    direction_value_list = []

    for direction_element in range(num_direction_elements):
      direction_element_energy_sum = 0
      energy_value_list = []

      for energy_element in range(num_energy_elements):
        local_index = energy_element + direction_element*num_energy_elements
        local_importance_value = importance_dictionary[mesh_element][local_index]
        energy_value_list.append(local_importance_value)
        direction_element_energy_sum += local_importance_value

      # Make energy distribution
      raw_energy_importance_distribution = Distribution.HistogramDistribution(energy_bounds, energy_value_list)
      energy_distribution = ActiveRegion.ImportanceSampledIndependentEnergyDimensionDistribution(real_energy_distribution, raw_energy_importance_distribution)
      energy_distribution_vector.push_back(energy_distribution)

      # Local direction value equal to sum of energy values
      direction_value_list.append(direction_element_energy_sum)
      
      mesh_element_direction_sum += direction_element_energy_sum

    # Make direction distribution
    raw_direction_importance_distribution = Distribution.HistogramDistribution(direction_bounds, direction_value_list)
    direction_distribution = ActiveRegion.ImportanceSampledIndependentDirectionIndexDimensionDistribution(real_direction_distribution, raw_direction_importance_distribution)
    direction_distribution_vector.push_back(direction_distribution)

    # Local mesh value equal to sum of direction values
    mesh_value_list.append(mesh_element_direction_sum)

  raw_mesh_importance_distribution = Distribution.HistogramDistribution(spatial_bounds, mesh_value_list)
  mesh_distribution = ActiveRegion.ImportanceSampledIndependentSpatialIndexDimensionDistribution(real_spatial_distribution, raw_mesh_importance_distribution)
  spatial_distribution_vector.push_back(mesh_distribution)

  distribution_map = { ActiveRegion.SPATIAL_INDEX_DIMENSION: spatial_distribution_vector,
                       ActiveRegion.DIRECTION_INDEX_DIMENSION: direction_distribution_vector,
                       ActiveRegion.ENERGY_DIMENSION: energy_distribution_vector }

  importance_sampled_particle_distribution.setImportanceDimensionDistributions(distribution_map, dimension_boundary_map, dimension_order_vector)

  # Form source component vector
  source_component_vector = []
  if particle_type == MonteCarlo.PHOTON:
    component = ActiveRegion.StandardPhotonSourceComponent(1, 1.0, model, importance_sampled_particle_distribution)
    source_component_vector.append(component)
  else:
    component = ActiveRegion.StandardAdjointPhotonSourceComponent(1, 1.0, model, importance_sampled_particle_distribution)
    source_component_vector.append(component)

  # Plug into actual source
  source = ActiveRegion.StandardParticleSource(source_component_vector)

  return source



##---------------------------------------------------------------------------##
## Set up and run the forward simulation
def simulate( sim_name,
              simulation_properties,
              threads,
              model,
              filled_model,
              direction_discretization,
              geometry_VR_estimator,
              source_VR_estimator,
              geometry_mesh,
              source_mesh,
              source_mesh_discretization_bounds,
              detector_mesh,
              geometry_mesh_observer_energy_discretization,
              source_energy_discretization_bounds,
              detector_energy_discretization,
              direction_discretization_bounds,
              real_source_mesh_distribution,
              real_source_direction_distribution,
              real_source_energy_distribution,
              particle_type):       
    #--------------------------------------------------------------------------------#
    # CREATE SOURCE
    #--------------------------------------------------------------------------------#
    source_model = None
    if particle_type == MonteCarlo.PHOTON:
      source_model = model
    elif particle_type == MonteCarlo.ADJOINT_PHOTON:
      source_model = filled_model

    source = getImportanceSource(source_VR_estimator.getImportanceDictionary(), \
                                  real_source_mesh_distribution, \
                                  source_mesh_discretization_bounds, \
                                  real_source_energy_distribution, \
                                  source_energy_discretization_bounds,\
                                  real_source_direction_distribution, \
                                  direction_discretization_bounds, \
                                  source_mesh, \
                                  direction_discretization, \
                                  particle_type,
                                  source_model)

    #--------------------------------------------------------------------------------#
    # FORWARD WEIGHT IMPORTANCE MESH INITIALIZATION
    #--------------------------------------------------------------------------------#

    # Initial weight-importance mesh for first forward simulation
    weight_importance_dictionary = geometry_VR_estimator.getFlatDictionary( 1 )

    weight_importance_map = Event.ImportanceMap( weight_importance_dictionary )

    weight_importance_mesh = Event.WeightImportanceMesh()

    weight_importance_mesh.setMesh( geometry_mesh )
    weight_importance_mesh.setDirectionDiscretization( Event.PQLA, 2, True )
    weight_importance_mesh.setEnergyDiscretization( geometry_mesh_observer_energy_discretization )
    weight_importance_mesh.setWeightImportanceMap(weight_importance_map)

    # Set up the event handler
    event_handler = Event.EventHandler( model, simulation_properties )
    
    # Detector Collision Estimator (main estimator, not VR producing estimator)
    event_handler.getEstimator( 1 ).setEnergyDiscretization( [ detector_energy_discretization[0], detector_energy_discretization[-1] ] )
    
    # Mesh estimator (weight importance mesh producing estimator)
    mesh_estimator = Event.WeightMultipliedMeshTrackLengthFluxEstimator(2, 1.0, geometry_mesh)
    
    mesh_estimator.setDirectionDiscretization( Event.PQLA, 2, False)
    mesh_estimator.setEnergyDiscretization( geometry_mesh_observer_energy_discretization )
    mesh_estimator.setParticleTypes( [particle_type] )
    event_handler.addEstimator(mesh_estimator)
    
    # Detector mesh estimator (for adjoint source biasing)
    mesh_detector_estimator = Event.WeightMultipliedMeshTrackLengthFluxEstimator(3, 1.0, detector_mesh)
    
    mesh_detector_estimator.setDirectionDiscretization( Event.PQLA, 2, False )
    mesh_detector_estimator.setEnergyDiscretization( detector_energy_discretization )
    mesh_detector_estimator.setParticleTypes( [particle_type] )
    event_handler.addEstimator( mesh_detector_estimator )

    # Set up the simulation manager
    factory = Manager.ParticleSimulationManagerFactory( filled_model,
                                                        source,
                                                        event_handler,
                                                        simulation_properties,
                                                        sim_name + "_forward",
                                                        "bin",
                                                        threads )
                                                        
    # Create the simulation manager
    factory.setPopulationControl( weight_importance_mesh )
    manager = factory.getManager()
    manager.useSingleRendezvousFile()
    
    ## Run the simulation
    manager.runSimulation()

    estimator_1_data = manager.getEventHandler().getEstimator(1).getTotalProcessedData()

    estimator_2_data = {}
    for i in range(geometry_mesh.getNumberOfElements()):
      estimator_2_data[i] = manager.getEventHandler().getEstimator(2).getEntityBinProcessedData(i)

    estimator_3_data = {}
    for i in range(detector_mesh.getNumberOfElements()):
      estimator_3_data[i] = manager.getEventHandler().getEstimator(3).getEntityBinProcessedData(i)

    return estimator_1_data,\
           estimator_2_data,\
           estimator_3_data

