import numpy
import os
import sys
import math
from argparse import *
from problem_1_run_simulation import simulate
from estimators import *
import PyFrensie.Geometry as Geometry
import PyFrensie.Geometry.DagMC as DagMC
import PyFrensie.Utility as Utility
import PyFrensie.Utility.Mesh as Mesh
import PyFrensie.Utility.MPI as MPI
import PyFrensie.Utility.Prng as Prng
import PyFrensie.Utility.Coordinate as Coordinate
import PyFrensie.Utility.Distribution as Distribution
import PyFrensie.Utility.DirectionDiscretization as DirectionDiscretization
import PyFrensie.MonteCarlo as MonteCarlo
import PyFrensie.MonteCarlo.Collision as Collision
import PyFrensie.MonteCarlo.ActiveRegion as ActiveRegion
import PyFrensie.MonteCarlo.Event as Event
import PyFrensie.MonteCarlo.Manager as Manager
import PyFrensie.Data as Data
import PyFrensie.Data.Native as Native

#Class that contains and processes the relevant statistical data for the estimator of collision estimator results



def initializeModelProperties(geometry_file_name):
  model_properties = DagMC.DagMCModelProperties(geometry_file_name)
  model_properties.setMaterialPropertyName( "material" )
  model_properties.setDensityPropertyName( "density" )
  model_properties.setTerminationCellPropertyName( "termination.cell" )
  model_properties.setCellCollisionFluxName( "cell.c.flux" )
  model_properties.useFastIdLookup()
  model = DagMC.DagMCModel( model_properties )
  return model

#Assumes equal x, y, z size for elements
def initializeMesh(mesh_increment, \
                   x0, x_distance, \
                   y0, y_distance, \
                   z0, z_distance):

  x_planes = []
  for i in range( int((x_distance/mesh_increment) + 1) ):
    x_planes.append( i*mesh_increment + x0 )

  y_planes = []
  for i in range( int((y_distance/mesh_increment) + 1) ):
    y_planes.append( i*mesh_increment + y0 )

  z_planes = []
  for i in range( int((z_distance/mesh_increment) + 1) ):
    z_planes.append( i*mesh_increment + z0 )

  mesh = Mesh.StructuredHexMesh( x_planes, y_planes, z_planes )

  return mesh
  
if __name__ == "__main__":
    #--------------------------------------------------------------------------------#
    # SIMULATION PARAMETERS
    #--------------------------------------------------------------------------------#
    db_path = os.environ.get("DATABASE_PATH")
    print(db_path)
    sim_name = "problem_1"
    num_particles = 1e2
    threads = 8
    num_iterations = 1
    
    if db_path is None:
        print('The database path must be specified!')
        sys.exit(1)

    #--------------------------------------------------------------------------------#
    # MODELS
    #--------------------------------------------------------------------------------#
    
    # Forward model (must be seperate due to estimator-geometry simultaneous declaration)
    forward_model = initializeModelProperties("problem_1_forward.h5m")
    
    # Adjoint model
    adjoint_model = initializeModelProperties("problem_1_adjoint.h5m")

    #--------------------------------------------------------------------------------#
    # MESH FORMATION
    #--------------------------------------------------------------------------------#

    # Needs to be the same for all 3 meshes to avoid split/terminate on birth
    mesh_increment = 50.0
    geometry_mesh_x_distance = 5000
    geometry_mesh_y_distance = 1000
    geometry_mesh_z_distance = 1000
    # Form the mesh for the entire geometry
    geometry_mesh_x0 = -2500.0        
    geometry_mesh_y0 = -500.0
    geometry_mesh_z0 = -500.0
    
    # entire geometry mesh
    geometry_mesh = initializeMesh( mesh_increment, \
                                    geometry_mesh_x0, geometry_mesh_x_distance, \
                                    geometry_mesh_y0, geometry_mesh_y_distance, \
                                    geometry_mesh_z0, geometry_mesh_z_distance )
    
    # Form the mesh for the source and response function
    x0_src = -2350
    x0_resp = 2300
    y0 = -300
    z0 = -300
        
    # source/detector mesh objects
    source_mesh = initializeMesh( mesh_increment, \
                                  x0_src, 50, \
                                  y0, 600, \
                                  z0, 600 )
    response_mesh = initializeMesh( mesh_increment, \
                                  x0_resp, 50, \
                                  y0, 600, \
                                  z0, 600 )
    number_of_forward_source_mesh_elements = source_mesh.getNumberOfElements()
    number_of_adjoint_source_mesh_elements = response_mesh.getNumberOfElements()
    #--------------------------------------------------------------------------------#
    # DIRECTION DISCRETIZATION
    #--------------------------------------------------------------------------------#

    # Direction Discretization
    PQLA_quadrature_order = 2
    direction_discretization = DirectionDiscretization.PQLAQuadrature( PQLA_quadrature_order )

    #--------------------------------------------------------------------------------#
    # FORWARD SOURCE DISTRIBUTIONS / ADJOINT ESTIMATOR DISCRETIZATIONS
    #--------------------------------------------------------------------------------#

    # Forward mesh distribution used for source initialization and eventual "real" distribution
    raw_source_mesh_distribution_bounds = []
    raw_source_mesh_distribution_values = []
    for i in range( number_of_forward_source_mesh_elements + 1 ):

      raw_source_mesh_distribution_bounds.append( i )

      if i < number_of_forward_source_mesh_elements:

        raw_source_mesh_distribution_values.append( 1.0 )

    real_forward_source_raw_mesh_distribution = Distribution.HistogramDistribution( raw_source_mesh_distribution_bounds, \
                                                                                    raw_source_mesh_distribution_values )

    # Direction distribution for eventual "real" distribution for importance sampling
    raw_source_direction_distribution_bounds = []
    raw_source_direction_distribution_values = []
    for i in range( direction_discretization.getNumberOfTriangles() + 1 ):

      raw_source_direction_distribution_bounds.append(i)

      if i < direction_discretization.getNumberOfTriangles():

        raw_source_direction_distribution_values.append( direction_discretization.getTriangleArea( i ))

    real_forward_source_raw_direction_distribution = Distribution.HistogramDistribution( raw_source_direction_distribution_bounds, \
                                                                                         raw_source_direction_distribution_values )

    # Forward energy distribution used for source initialization and eventual "real" distribution
    raw_source_energy_distribution_bounds = [7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
    raw_source_energy_distribution_values = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Energy distribution used for source initialization and eventual "real" distribution
    real_forward_source_raw_energy_distribution = Distribution.HistogramDistribution( raw_source_energy_distribution_bounds,\
                                                                                      raw_source_energy_distribution_values )

    #--------------------------------------------------------------------------------#
    # INITIAL FORWARD SOURCE
    #--------------------------------------------------------------------------------#

    # Only needs mesh and energy - direction is isotropic by default
    forward_source_mesh_distribution = ActiveRegion.IndependentSpatialIndexDimensionDistribution( real_forward_source_raw_mesh_distribution )
    forward_source_energy_distribution = ActiveRegion.IndependentEnergyDimensionDistribution( real_forward_source_raw_energy_distribution )

    forward_source_particle_distribution = ActiveRegion.StandardParticleDistribution( "Initial forward source" )
    forward_source_particle_distribution.setMeshIndexDimensionDistribution( forward_source_mesh_distribution, source_mesh )
    forward_source_particle_distribution.setDimensionDistribution( forward_source_energy_distribution )
    forward_source_particle_distribution.constructDimensionDistributionDependencyTree()

    forward_source_component = ActiveRegion.StandardPhotonSourceComponent( 1, 1.0, forward_model, forward_source_particle_distribution )

    forward_source = ActiveRegion.StandardParticleSource( [forward_source_component] )

    #--------------------------------------------------------------------------------#
    # ADJOINT SOURCE DISTRIBUTIONS / FORWARD ESTIMATOR DISCRETIZATIONS
    #--------------------------------------------------------------------------------#

    # adjoint mesh distribution used for eventual "real" distribution in importance sampling

    raw_detector_mesh_distribution_bounds = []
    raw_detector_mesh_distribution_values = []
    for i in range( number_of_adjoint_source_mesh_elements + 1 ):

      raw_detector_mesh_distribution_bounds.append( i )

      if i < number_of_forward_source_mesh_elements:

        raw_detector_mesh_distribution_values.append( 1.0 )

    real_adjoint_source_raw_mesh_distribution = Distribution.HistogramDistribution( raw_detector_mesh_distribution_bounds, \
                                                                                    raw_detector_mesh_distribution_values )

    # Direction distribution for eventual "real" distribution for importance sampling
    raw_detector_direction_distribution_bounds = []
    raw_detector_direction_distribution_values = []
    for i in range( direction_discretization.getNumberOfTriangles() + 1):

      raw_detector_direction_distribution_bounds.append(i)

      if i < direction_discretization.getNumberOfTriangles():

        raw_detector_direction_distribution_values.append( direction_discretization.getTriangleArea( i ))

    real_adjoint_source_raw_direction_distribution = Distribution.HistogramDistribution( raw_detector_direction_distribution_bounds, \
                                                                                         raw_detector_direction_distribution_values )

    # Lists for adjoint source energy and forward estimator energy (non-importance sampled)
    raw_detector_energy_distribution_bounds = [0.0, 0.5, 1.0, 1.5]
    raw_detector_energy_distribution_values = [1.0, 1.0, 1.0]

    real_adjoint_source_raw_energy_distribution = Distribution.HistogramDistribution( raw_detector_energy_distribution_bounds,\
                                                                                      raw_detector_energy_distribution_values )

    #--------------------------------------------------------------------------------#
    # ESTIMATORS OF ESTIMATORS INITIALIZATIONS
    #--------------------------------------------------------------------------------#
 
    # Energy bounds for weight importance meshes and mesh estimators
    geometry_mesh_observer_energy_discretization = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]

    # Initialize collision estimator of estimators
    forward_collision_mean_estimator = collisionEstimatorOfEstimators()
    adjoint_collision_mean_estimator = collisionEstimatorOfEstimators()

    # Initialize geometry mesh estimator of estimators
    forward_geometry_mesh_estimator = meshVREstimatorOfEstimators(geometry_mesh.getNumberOfElements(), \
                                                                  direction_discretization.getNumberOfTriangles(), \
                                                                  len(geometry_mesh_observer_energy_discretization)-1 )
    adjoint_geometry_mesh_estimator = meshVREstimatorOfEstimators( geometry_mesh.getNumberOfElements(),\
                                                                  direction_discretization.getNumberOfTriangles(),\
                                                                  len(geometry_mesh_observer_energy_discretization)-1 )
    
    # Initialize source mesh estimators of estimators
    forward_source_mesh_estimator = meshVREstimatorOfEstimators(number_of_forward_source_mesh_elements,
                                                                direction_discretization.getNumberOfTriangles(),
                                                                len(raw_source_energy_distribution_values))
    adjoint_source_mesh_estimator = meshVREstimatorOfEstimators(number_of_adjoint_source_mesh_elements,
                                                                direction_discretization.getNumberOfTriangles(),
                                                                len(raw_detector_energy_distribution_values))

    #--------------------------------------------------------------------------------#
    # FORWARD WEIGHT IMPORTANCE MESH INITIALIZATION
    #--------------------------------------------------------------------------------#

    # Initial weight-importance mesh for first forward simulation
    forward_weight_importance_dictionary = forward_geometry_mesh_estimator.getFlatDictionary( 1 )

    forward_weight_importance_map = Event.ImportanceMap( forward_weight_importance_dictionary )

    forward_weight_importance_mesh = Event.WeightImportanceMesh()

    forward_weight_importance_mesh.setMesh( geometry_mesh )
    forward_weight_importance_mesh.setDirectionDiscretization( Event.PQLA, 2, True )
    forward_weight_importance_mesh.setEnergyDiscretization( geometry_mesh_observer_energy_discretization )
    forward_weight_importance_mesh.setWeightImportanceMap(forward_weight_importance_map)

    #--------------------------------------------------------------------------------#
    # ITERATIONS
    #--------------------------------------------------------------------------------#

    for i in range(num_iterations):
        print("On forward/adjoint iteration ", i)
        cell_collision_estimator, geometry_mesh_estimator, detector_mesh_estimator = simulate( sim_name, \
                                                                                          db_path, \
                                                                                          num_particles, \
                                                                                          threads, \
                                                                                          forward_model, \
                                                                                          forward_source,
                                                                                          forward_weight_importance_mesh,
                                                                                          geometry_mesh, \
                                                                                          response_mesh, \
                                                                                          geometry_mesh_observer_energy_discretization, \
                                                                                          raw_detector_energy_distribution_bounds)
        #forward_collision_mean_estimator.processEstimator(cell_collision_estimator.getTotalProcessedData())

        #adjoint_cell_collision_estimator, adjoint_geometry_mesh_estimator, source_mesh_estimator = simulate( sim_name, \
        #                                                                                                db_path, \
        #                                                                                                num_particles, \
        #                                                                                                threads, \
        #                                                                                                adjoint_model, \
        #                                                                                                adjoint_source, \
        #                                                                                                adjoint_weight_importance_mesh, \
        #                                                                                                geometry_mesh, \
        #                                                                                                source_mesh, \
        #                                                                                                geometry_mesh_observer_energy_discretization, \
        #                                                                                                raw_source_energy_distribution_bounds )
        #adjoint_collision_mean_estimator.processEstimator(cell_collision_estimator.getTotalProcessedData())

