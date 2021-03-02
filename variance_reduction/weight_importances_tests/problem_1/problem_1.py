import os
import sys
from argparse import *
from problem_1_run_simulation import simulate
from estimators import *
import PyFrensie.Geometry.DagMC as DagMC
import PyFrensie.Utility.Mesh as Mesh
import PyFrensie.Utility.Distribution as Distribution
import PyFrensie.Utility.DirectionDiscretization as DirectionDiscretization
import PyFrensie.MonteCarlo.ActiveRegion as ActiveRegion
import PyFrensie.MonteCarlo.Event as Event
import PyFrensie.Data as Data
import PyFrensie.MonteCarlo.Collision as Collision
import PyFrensie.MonteCarlo as MonteCarlo

def initializeModelProperties(geometry_file_name):
  model_properties = DagMC.DagMCModelProperties(geometry_file_name)
  model_properties.setMaterialPropertyName( "material" )
  model_properties.setDensityPropertyName( "density" )
  model_properties.setTerminationCellPropertyName( "termination.cell" )
  model_properties.setCellCollisionFluxName( "cell.c.flux" )
  model_properties.useFastIdLookup()
  model = DagMC.DagMCModel( model_properties )
  return model

def fillGeometryModel(db_path, model, num_particles, forward_adjoint_string):
    ## Set the simulation properties
    simulation_properties = MonteCarlo.SimulationProperties()

    # simulate adjoint or forward photons
    data_file_type = None
    if forward_adjoint_string == "forward":
      simulation_properties.setParticleMode( MonteCarlo.PHOTON_MODE )
      data_file_type = Data.PhotoatomicDataProperties.Native_EPR_FILE
    else:
      simulation_properties.setParticleMode( MonteCarlo.ADJOINT_PHOTON_MODE )
      data_file_type = Data.AdjointPhotoatomicDataProperties.Native_EPR_FILE
    
    # Set the number of histories to run and the number of rendezvous
    simulation_properties.setNumberOfHistories( num_particles )
    simulation_properties.setMinNumberOfRendezvous( 1 )
    simulation_properties.setNumberOfSnapshotsPerBatch( 1 )
    simulation_properties.setNumberOfPhotonHashGridBins( 100 )
    
    ## Set up the materials
    database = Data.ScatteringCenterPropertiesDatabase( db_path )
    
    # Extract the properties for H from the database
    H_properties = database.getAtomProperties( Data.ZAID(1000) )
    
    # Extract the properties for Pb from the database
    Pb_properties = database.getAtomProperties( Data.ZAID(82000) )
    
    # Extract the properties for K from the database
    K_properties = database.getAtomProperties( Data.ZAID(19000) )
    
    # Extract the properties for Ge from the database
    Ge_properties = database.getAtomProperties( Data.ZAID(32000) )
    
    # Set the definition for H, Pb, K, Ge for this simulation
    scattering_center_definitions = Collision.ScatteringCenterDefinitionDatabase()
    H_definition = scattering_center_definitions.createDefinition( "H", Data.ZAID(1000) )
    Pb_definition = scattering_center_definitions.createDefinition( "Pb", Data.ZAID(82000) )
    K_definition = scattering_center_definitions.createDefinition( "K", Data.ZAID(19000) )
    Ge_definition = scattering_center_definitions.createDefinition( "Ge", Data.ZAID(32000) )
    
    
    file_version = 0
    
    if forward_adjoint_string == "forward":
      H_definition.setPhotoatomicDataProperties( H_properties.getSharedPhotoatomicDataProperties( data_file_type, file_version) )
      Pb_definition.setPhotoatomicDataProperties( Pb_properties.getSharedPhotoatomicDataProperties( data_file_type, file_version) )
      K_definition.setPhotoatomicDataProperties( K_properties.getSharedPhotoatomicDataProperties( data_file_type, file_version) )
      Ge_definition.setPhotoatomicDataProperties( Ge_properties.getSharedPhotoatomicDataProperties( data_file_type, file_version) )
    else:
      H_definition.setAdjointPhotoatomicDataProperties( H_properties.getSharedAdjointPhotoatomicDataProperties( data_file_type, file_version) )
      Pb_definition.setAdjointPhotoatomicDataProperties( Pb_properties.getSharedAdjointPhotoatomicDataProperties( data_file_type, file_version) )
      K_definition.setAdjointPhotoatomicDataProperties( K_properties.getSharedAdjointPhotoatomicDataProperties( data_file_type, file_version) )
      Ge_definition.setAdjointPhotoatomicDataProperties( Ge_properties.getSharedAdjointPhotoatomicDataProperties( data_file_type, file_version) )
    
    # Set the definition for materials
    material_definitions = Collision.MaterialDefinitionDatabase()
    material_definitions.addDefinition( "H", 1, ["H"], [1.0] )
    material_definitions.addDefinition( "Pb", 2, ["Pb"], [1.0] )
    material_definitions.addDefinition( "K", 3, ["K"], [1.0] )
    material_definitions.addDefinition( "Ge", 4, ["Ge"], [1.0] )
    
    filled_model = Collision.FilledGeometryModel( db_path, scattering_center_definitions, material_definitions, simulation_properties, model, True )

    return filled_model, simulation_properties


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

def setSimProperties(num_particles, particle_type):
      ## Set the simulation properties
    simulation_properties = MonteCarlo.SimulationProperties()

    # Simulate photons only
    simulation_properties.setParticleMode( particle_type )
    
    # Set the number of histories to run and the number of rendezvous
    simulation_properties.setNumberOfHistories( num_particles )
    simulation_properties.setMinNumberOfRendezvous( 1 )
    simulation_properties.setNumberOfSnapshotsPerBatch( 1 )
    simulation_properties.setNumberOfPhotonHashGridBins( 100 )

    return simulation_properties

if __name__ == "__main__":
    #--------------------------------------------------------------------------------#
    # SIMULATION PARAMETERS
    #--------------------------------------------------------------------------------#
    db_path = os.environ.get("DATABASE_PATH")
    print(db_path)
    sim_name = "problem_1"
    num_particles = 1e2
    threads = 1
    num_iterations = 1
    
    if db_path is None:
        print('The database path must be specified!')
        sys.exit(1)
    #--------------------------------------------------------------------------------#
    # SIMULATION PROPERTIES
    #--------------------------------------------------------------------------------#
    forward_simulation_properties = setSimProperties(num_particles, MonteCarlo.PHOTON)
    adjoint_simulation_properties = setSimProperties(num_particles, MonteCarlo.ADJOINT_PHOTON)

    #--------------------------------------------------------------------------------#
    # MODELS
    #--------------------------------------------------------------------------------#
    
    # Forward model (must be seperate due to estimator-geometry simultaneous declaration)
    forward_model = initializeModelProperties("problem_1_forward.h5m")
    
    # Adjoint model
    adjoint_model = initializeModelProperties("problem_1_adjoint.h5m")

    #Filled models
    forward_filled_model, forward_simulation_properties = fillGeometryModel( db_path, forward_model, num_particles, "forward" )
    adjoint_filled_model, adjoint_simulation_properties = fillGeometryModel( db_path, adjoint_model, num_particles, "adjoint")
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
    
    # Initialize response mesh estimators of estimators
    forward_response_mesh_estimator = meshVREstimatorOfEstimators(number_of_adjoint_source_mesh_elements,
                                                                direction_discretization.getNumberOfTriangles(),
                                                                len(raw_detector_energy_distribution_values))
    adjoint_response_mesh_estimator = meshVREstimatorOfEstimators(number_of_forward_source_mesh_elements,
                                                                direction_discretization.getNumberOfTriangles(),
                                                                len(raw_source_energy_distribution_values))



    #--------------------------------------------------------------------------------#
    # ITERATIONS
    #--------------------------------------------------------------------------------#

    for i in range(num_iterations):
        print("On forward/adjoint iteration ", i)
        cell_collision_estimator_data, geometry_mesh_estimator_data, detector_mesh_estimator_data = simulate( sim_name + "_forward",
                                                                                                              forward_simulation_properties,
                                                                                                              threads,
                                                                                                              forward_model,
                                                                                                              forward_filled_model,
                                                                                                              direction_discretization,
                                                                                                              forward_geometry_mesh_estimator,
                                                                                                              adjoint_response_mesh_estimator,
                                                                                                              geometry_mesh,
                                                                                                              source_mesh,
                                                                                                              raw_source_mesh_distribution_bounds,
                                                                                                              response_mesh,
                                                                                                              geometry_mesh_observer_energy_discretization,
                                                                                                              raw_source_energy_distribution_bounds,
                                                                                                              raw_detector_energy_distribution_bounds,
                                                                                                              raw_source_direction_distribution_bounds,
                                                                                                              real_forward_source_raw_mesh_distribution,
                                                                                                              real_forward_source_raw_direction_distribution,
                                                                                                              real_forward_source_raw_energy_distribution,
                                                                                                              MonteCarlo.PHOTON)

        forward_collision_mean_estimator.processEstimator( cell_collision_estimator_data )
        forward_response_mesh_estimator.processEstimator( detector_mesh_estimator_data )
        forward_geometry_mesh_estimator.processEstimator( geometry_mesh_estimator_data )

        #
        adjoint_cell_collision_estimator_data, adjoint_geometry_mesh_estimator_data, source_mesh_estimator_data = simulate( sim_name + "_adjoint",
                                                                                                              adjoint_simulation_properties,
                                                                                                              threads,
                                                                                                              adjoint_model,
                                                                                                              adjoint_filled_model,
                                                                                                              direction_discretization,
                                                                                                              adjoint_geometry_mesh_estimator,
                                                                                                              forward_response_mesh_estimator,
                                                                                                              geometry_mesh,
                                                                                                              response_mesh,
                                                                                                              raw_detector_mesh_distribution_bounds,
                                                                                                              source_mesh,
                                                                                                              geometry_mesh_observer_energy_discretization,
                                                                                                              raw_detector_energy_distribution_bounds,
                                                                                                              raw_source_energy_distribution_bounds,
                                                                                                              raw_detector_direction_distribution_bounds,
                                                                                                              real_adjoint_source_raw_mesh_distribution,
                                                                                                              real_adjoint_source_raw_direction_distribution,
                                                                                                              real_adjoint_source_raw_energy_distribution,
                                                                                                              MonteCarlo.ADJOINT_PHOTON)

        adjoint_collision_mean_estimator.processEstimator( adjoint_cell_collision_estimator_data )
        adjoint_response_mesh_estimator.processEstimator( source_mesh_estimator_data )
        adjoint_geometry_mesh_estimator.processEstimator( adjoint_geometry_mesh_estimator_data )

