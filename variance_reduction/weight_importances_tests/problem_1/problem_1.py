import numpy
import os
import sys
from argparse import *
import PyFrensie.Geometry as Geometry
from problem_1_forward import runForwardSimulation
from problem_1_adjoint import runAdjointSimulation
import PyFrensie.Geometry.ROOT as ROOT
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

if __name__ == "__main__":
    
    # Parse the command line options
    parser = ArgumentParser()
    parser.add_argument('--threads', type=int, dest='threads', default=1,
                      help='the number of threads to use')
    parser.add_argument('--db_path', type=str, dest='db_path',
                      help='the database name (with extension)')
    parser.add_argument('--sim_name', type=str, dest='sim_name', default='sphere',
                      help='the simulation name')
    parser.add_argument('--log_file', type=str, dest='log_file',
                      help='the file that will be used for logging')
    parser.add_argument('--num_particles', type=float, dest='num_particles', default=1e3,
                      help='the number of particles to run')
    args = parser.parse_args()

    if args.db_path is None:
        print 'The database path must be specified!'
        sys.exit(1)
        
    ## Initialize the MPI session
    session = MPI.GlobalMPISession( len(sys.argv), sys.argv )
    # Suppress logging on all procs except for the master (proc=0)
    Utility.removeAllLogs()
    session.initializeLogs( 0, True )
    
    if not args.log_file is None:
        session.initializeLogs( args.log_file, 0, True )
        
    model_properties = ROOT.RootModelProperties("problem_1.root")
    model_properties.setMaterialPropertyName( "mat" )
    model = ROOT.RootModel.getInstance()
    model.initialize( model_properties )
    
    # SET UP SOURCE BIASING DISTRIBUTIONS
    
    energy_bounds = [1.0, 2.0, 3.0, 4.0, 5.0]
    energy_dist = [1.0, 1.0, 1.0, 1.0]
    
    initial_response_energy_distribution = Distribution.HistogramDistribution( energy_bounds, energy_dist )
    
    energy_bounds = [4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    energy_dist = [4.0, 4.0, 4.0, 4.0, 4.0]
    source_distribution = Distribution.UniformDistribution( 1.0, 7.0, 3.0)
    
    direction_energy_discretization = DirectionDiscretization.PQLAQuadrature(2)
    
    #Source/Response direction bias distribution
    direction_index_bounds = []
    direction_distribution = []
    i0 = 0.0
    for i in range(33):
        direction_index_bounds.append(i0 + i)
        
    for i in range(32):
        direction_distribution.append( 1.0 )
    initial_direction_distribution = Distribution.HistogramDistribution( direction_index_bounds, direction_distribution)
    
    spatial_index_bounds = []
    spatial_distribution = []
    i0 = 0.0
    for i in range( 65 ):
        spatial_index_bounds.append(i0 + i)
    for i in range( 64 ):
        spatial_distribution.append( 1.0 )
        
    initial_spatial_distribution = Distribution.HistogramDistribution( spatial_index_bounds, spatial_distribution)
    
    # Needs to be the same for all 3 meshes to avoid split/terminate on birth
    mesh_increment = 20.0
    # Form the mesh for the entire geometry
    x0 = -1000.0
    x_planes = []
    for i in range(101):
        x_planes.append( i*mesh_increment + x0 )
        
    y0 = -500.0
    z0 = -500.0
    y_planes = []
    z_planes = []
    for i in range(51):
        y_planes.append( i*mesh_increment + y0 )
        z_planes.append( i*mesh_increment + z0 )
    
    geometry_mesh = Mesh.StructuredHexMesh (x_planes, y_planes, z_planes)
    
    # Form the mesh for the source
    x0_src = -940
    x0_resp = 860
    y0 = -40
    z0 = -40
    x_planes_src = []
    x_planes_resp = []
    y_planes = []
    z_planes = []
    for i in range(5):
        x_planes_src.append( i*mesh_increment + x0_src )
        x_planes_resp.append( i*mesh_increment + x0_resp )
        y_planes.append( i*mesh_increment + y0 )
        z_planes.append( i*mesh_increment + z0 )
        
    source_mesh = Mesh.StructuredHexMesh( x_planes_src, y_planes, z_planes )
    response_mesh = Mesh.StructuredHexMesh( x_planes_resp, y_planes, z_planes )

    #runForwardSimulation( args.sim_name,
    #                      args.db_path,
    #                      args.num_particles,
    #                      args.threads,
    #                      session,
    #                      model,
    #                      response_distribution,
    #                      source_distribution,
    #                      geometry_mesh,
    #                      source_mesh,
    #                      response_mesh )
                          
    #runAdjointSimulation( args.sim_name,
    #                      args.db_path,
    #                     args.num_particles,
    #                      args.threads,
    #                      session,
    #                      model,
    #                      response_distribution,
    #                      source_distribution,
    #                      geometry_mesh,
    #                      source_mesh,
    #                      response_mesh )
