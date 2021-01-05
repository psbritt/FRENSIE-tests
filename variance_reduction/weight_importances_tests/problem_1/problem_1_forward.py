import numpy
import os
import sys
from argparse import *
import PyFrensie.Geometry as Geometry
import PyFrensie.Geometry.ROOT as ROOT
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
import PyFrensie.Data.Native as Native

##---------------------------------------------------------------------------##
## Set up and run the forward simulation
def runForwardSimulation( sim_name,
                          db_path,
                          num_particles,
                          threads,
                          session,
                          model,
                          response_distribution,
                          source_distribution,
                          geometry_mesh,
                          source_mesh,
                          response_mesh):       
        
    ## Set the simulation properties
    simulation_properties = MonteCarlo.SimulationProperties()

    # Simulate photons only
    simulation_properties.setParticleMode( MonteCarlo.PHOTON_MODE )
    
    # Set the number of histories to run and the number of rendezvous
    simulation_properties.setNumberOfHistories( num_particles )
    simulation_properties.setMinNumberOfRendezvous( 1 )
    simulation_properties.setNumberOfSnapshotsPerBatch( 1 )
    
    ## Set up the materials
    database = Data.ScatteringCenterPropertiesDatabase( db_path )
    
    # Extract the properties for H from the database
    H_properties = database.getAtomProperties( Data.ZAID(1000) )
    
    # Extract the properties for K from the database
    K_properties = database.getAtomProperties( Data.ZAID(19000) )
    
    # Extract the properties for Ge from the database
    Ge_properties = database.getAtomProperties( Data.ZAID(32000) )
    
    # Set the definition for H, K, Ge for this simulation
    scattering_center_definitions = Collision.ScatteringCenterDefinitionDatabase()
    H_definition = scattering_center_definitions.createDefinition( "H", Data.ZAID(1000) )
    K_definition = scattering_center_definitions.createDefinition( "K", Data.ZAID(19000) )
    Ge_definition = scattering_center_definitions.createDefinition( "Ge", Data.ZAID(32000) )
    
    data_file_type = Data.PhotoatomicDataProperties.Native_EPR_FILE
    file_version = 0
    
    H_definition.setPhotoatomicDataProperties( H_properties.getSharedPhotoatomicDataProperties( data_file_type, file_version) )
    K_definition.setPhotoatomicDataProperties( K_properties.getSharedPhotoatomicDataProperties( data_file_type, file_version) )
    Ge_definition.setPhotoatomicDataProperties( Ge_properties.getSharedPhotoatomicDataProperties( data_file_type, file_version) )
    
    # Set the definition for materials
    material_definitions = Collision.MaterialDefinitionDatabase()
    material_definitions.addDefinition( "H", 1, ["H"], [1.0] )
    material_definitions.addDefinition( "K", 2, ["K"], [1.0] )
    material_definitions.addDefinition( "Ge", 3, ["Ge"], [1.0] )
    
    filled_model = Collision.FilledGeometryModel( db_path, scattering_center_definitions, material_definitions, simulation_properties, model, True )
    
    # Set up the event handler
    event_handler = Event.EventHandler( model, simulation_properties )
    
    # Detector Collision Estimator (main estimator, not VR producing estimator)
    forward_estimator_id = 0
    forward_estimator_cell_id = [3]
    
    forward_collision_flux_estimator = Event.WeightMultipliedCellCollisionFluxEstimator( forward_estimator_id, 1.0, forward_estimator_cell_id, model)
    
    forward_collision_flux_estimator.setParticleTypes( [MonteCarlo.PHOTON] )
    
    response_function = ActiveRegion.EnergyParticleResponseFunction( response_distribution )
    
    response = ActiveRegion.StandardParticleResponse( response_function )
    
    forward_collision_flux_estimator.setResponseFunctions( [response] )
    
    event_handler.addEstimator(forward_collision_flux_estimator)
    
    # Source
    particle_distribution = ActiveRegion.StandardParticleDistribution( "source distribution" )
    
    energy_dimension_dist = ActiveRegion.IndependentEnergyDimensionDistribution( source_distribution)
    
    particle_distribution.setDimensionDistribution( energy_dimension_dist )
    
    uniform_x_position_distribution = Distribution.UniformDistribution( -905, -895 )
    uniform_y_z_position_distribution = Distribution.UniformDistribution( -5, 5 )
    
    x_position_dimension_dist = ActiveRegion.IndependentPrimarySpatialDimensionDistribution( uniform_x_position_distribution )
    y_position_dimension_dist = ActiveRegion.IndependentSecondarySpatialDimensionDistribution( uniform_y_z_position_distribution )
    z_position_dimension_dist = ActiveRegion.IndependentTertiarySpatialDimensionDistribution( uniform_y_z_position_distribution )
    
    particle_distribution.setDimensionDistribution( x_position_dimension_dist )
    particle_distribution.setDimensionDistribution( y_position_dimension_dist )
    particle_distribution.setDimensionDistribution( z_position_dimension_dist )
    
    particle_distribution.constructDimensionDistributionDependencyTree()
    
    photon_distribution = ActiveRegion.StandardPhotonSourceComponent( 0, 1.0, model, particle_distribution )
    
    # Assign the photon source component to the source
    source = ActiveRegion.StandardParticleSource( [photon_distribution] )
    
    # Set up the simulation manager
    factory = Manager.ParticleSimulationManagerFactory( filled_model,
                                                        source,
                                                        event_handler,
                                                        simulation_properties,
                                                        sim_name + "_forward",
                                                        "xml",
                                                        threads )
                                                        
    # Create the simulation manager
    manager = factory.getManager()
    manager.useSingleRendezvousFile()
    
    ## Run the simulation
    if session.size() == 1:
        manager.runInterruptibleSimulation()
    else:
        manager.runSimulation()
        

