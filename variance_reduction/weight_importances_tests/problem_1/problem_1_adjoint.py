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
def runAdjointSimulation( sim_name,
                          db_path,
                          num_particles,
                          threads,
                          session,
                          model,
                          response_distribution,
                          source_distribution):       
        
    ## Set the simulation properties
    simulation_properties = MonteCarlo.SimulationProperties()

    # Simulate photons only
    simulation_properties.setParticleMode( MonteCarlo.ADJOINT_PHOTON_MODE )
    simulation_properties.setMinAdjointPhotonEnergy( 1e-3 )
    simulation_properties.setMaxAdjointPhotonEnergy( 20.0 )
    # Set the number of histories to run and the number of rendezvous
    simulation_properties.setNumberOfHistories( num_particles )
    simulation_properties.setMinNumberOfRendezvous( 1 )
    simulation_properties.setNumberOfSnapshotsPerBatch( 1 )
    simulation_properties.setAdjointPhotonRouletteThresholdWeight( 0.0025 )
    simulation_properties.setAdjointPhotonRouletteSurvivalWeight(  0.005 )
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
    
    data_file_type = Data.AdjointPhotoatomicDataProperties.Native_EPR_FILE
    file_version = 0
    
    H_definition.setAdjointPhotoatomicDataProperties( H_properties.getSharedAdjointPhotoatomicDataProperties( data_file_type, file_version) )
    K_definition.setAdjointPhotoatomicDataProperties( K_properties.getSharedAdjointPhotoatomicDataProperties( data_file_type, file_version) )
    Ge_definition.setAdjointPhotoatomicDataProperties( Ge_properties.getSharedAdjointPhotoatomicDataProperties( data_file_type, file_version) )
    
    # Set the definition for materials
    material_definitions = Collision.MaterialDefinitionDatabase()
    material_definitions.addDefinition( "H", 1, ["H"], [1.0] )
    material_definitions.addDefinition( "K", 2, ["K"], [1.0] )
    material_definitions.addDefinition( "Ge", 3, ["Ge"], [1.0] )
    
    filled_model = Collision.FilledGeometryModel( db_path, scattering_center_definitions, material_definitions, simulation_properties, model, True )
    
    # Set up the event handler
    event_handler = Event.EventHandler( model, simulation_properties )
    
    # Detector Collision Estimator
    adjoint_estimator_id = 1
    adjoint_estimator_cell_id = [2]
    
    adjoint_collision_flux_estimator = Event.WeightMultipliedCellCollisionFluxEstimator( adjoint_estimator_id, 1.0, adjoint_estimator_cell_id, model)
    
    adjoint_collision_flux_estimator.setParticleTypes( [MonteCarlo.ADJOINT_PHOTON] )
    
    source_function = ActiveRegion.EnergyParticleResponseFunction( source_distribution )
    
    source = ActiveRegion.StandardParticleResponse( source_function )
    
    adjoint_collision_flux_estimator.setResponseFunctions( [source] )
    
    event_handler.addEstimator(adjoint_collision_flux_estimator)
    
    # Source
    particle_distribution = ActiveRegion.StandardParticleDistribution( "response function distribution" )
    
    energy_dimension_dist = ActiveRegion.IndependentEnergyDimensionDistribution( response_distribution)
    
    particle_distribution.setDimensionDistribution( energy_dimension_dist )
    
    uniform_x_position_distribution = Distribution.UniformDistribution( 905, 895 )
    uniform_y_z_position_distribution = Distribution.UniformDistribution( -5, 5 )
    
    x_position_dimension_dist = ActiveRegion.IndependentPrimarySpatialDimensionDistribution( uniform_x_position_distribution )
    y_position_dimension_dist = ActiveRegion.IndependentSecondarySpatialDimensionDistribution( uniform_y_z_position_distribution )
    z_position_dimension_dist = ActiveRegion.IndependentTertiarySpatialDimensionDistribution( uniform_y_z_position_distribution )
    
    particle_distribution.setDimensionDistribution( x_position_dimension_dist )
    particle_distribution.setDimensionDistribution( y_position_dimension_dist )
    particle_distribution.setDimensionDistribution( z_position_dimension_dist )
    
    particle_distribution.constructDimensionDistributionDependencyTree()
    
    adjoint_photon_distribution = ActiveRegion.StandardPhotonSourceComponent( 0, 1.0, model, particle_distribution )
    
    # Assign the photon source component to the source
    source = ActiveRegion.StandardParticleSource( [adjoint_photon_distribution] )
    
    # Set up the simulation manager
    factory = Manager.ParticleSimulationManagerFactory( filled_model,
                                                        source,
                                                        event_handler,
                                                        simulation_properties,
                                                        sim_name + "_adjoint",
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
        

