import numpy
import os
import sys
from argparse import *
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
import PyFrensie.Data.Native as Native

##---------------------------------------------------------------------------##
## Set up and run the forward simulation
def simulate( sim_name,
                          db_path,
                          num_particles,
                          threads,
                          model,
                          source,
                          weight_importance_mesh,
                          geometry_mesh,
                          detector_mesh,
                          geometry_mesh_observer_energy_discretization,
                          detector_energy_discretization):       
        
    ## Set the simulation properties
    simulation_properties = MonteCarlo.SimulationProperties()

    # Simulate photons only
    simulation_properties.setParticleMode( MonteCarlo.PHOTON_MODE )
    
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
    
    data_file_type = Data.PhotoatomicDataProperties.Native_EPR_FILE
    file_version = 0
    
    H_definition.setPhotoatomicDataProperties( H_properties.getSharedPhotoatomicDataProperties( data_file_type, file_version) )
    
    Pb_definition.setPhotoatomicDataProperties( Pb_properties.getSharedPhotoatomicDataProperties( data_file_type, file_version) )
    
    K_definition.setPhotoatomicDataProperties( K_properties.getSharedPhotoatomicDataProperties( data_file_type, file_version) )
    
    Ge_definition.setPhotoatomicDataProperties( Ge_properties.getSharedPhotoatomicDataProperties( data_file_type, file_version) )
    
    # Set the definition for materials
    material_definitions = Collision.MaterialDefinitionDatabase()
    material_definitions.addDefinition( "H", 1, ["H"], [1.0] )
    material_definitions.addDefinition( "Pb", 2, ["Pb"], [1.0] )
    material_definitions.addDefinition( "K", 3, ["K"], [1.0] )
    material_definitions.addDefinition( "Ge", 4, ["Ge"], [1.0] )
    
    filled_model = Collision.FilledGeometryModel( db_path, scattering_center_definitions, material_definitions, simulation_properties, model, True )
    
    # Set up the event handler
    event_handler = Event.EventHandler( model, simulation_properties )
    
    # Detector Collision Estimator (main estimator, not VR producing estimator)
    event_handler.getEstimator( 1 ).setEnergyDiscretization( [ detector_energy_discretization[0], detector_energy_discretization[-1] ] )
    
    # Mesh estimator (weight importance mesh producing estimator)
    mesh_estimator = Event.WeightMultipliedMeshTrackLengthFluxEstimator(2, 1.0, geometry_mesh)
    
    mesh_estimator.setDirectionDiscretization( Event.PQLA, 2, False)
    mesh_estimator.setEnergyDiscretization( geometry_mesh_observer_energy_discretization )
    mesh_estimator.setParticleTypes( [MonteCarlo.PHOTON] )
    event_handler.addEstimator(mesh_estimator)
    
    # Detector mesh estimator (for adjoint source biasing)
    mesh_detector_estimator = Event.WeightMultipliedMeshTrackLengthFluxEstimator(3, 1.0, detector_mesh)
    
    mesh_detector_estimator.setDirectionDiscretization( Event.PQLA, 2, False )
    mesh_detector_estimator.setEnergyDiscretization( detector_energy_discretization )
    mesh_detector_estimator.setParticleTypes( [MonteCarlo.PHOTON] )
    event_handler.addEstimator( mesh_detector_estimator )

    # Set up the simulation manager
    factory = Manager.ParticleSimulationManagerFactory( filled_model,
                                                        source,
                                                        event_handler,
                                                        simulation_properties,
                                                        sim_name + "_forward",
                                                        "xml",
                                                        threads )
                                                        
    # Create the simulation manager
    #factory.setPopulationControl( weight_importance_mesh )
    manager = factory.getManager()
    manager.useSingleRendezvousFile()
    
    ## Run the simulation
    manager.runSimulation()

    return manager.getEventHandler().getEstimator(1),\
           manager.getEventHandler().getEstimator(2),\
           manager.getEventHandler().getEstimator(3)

