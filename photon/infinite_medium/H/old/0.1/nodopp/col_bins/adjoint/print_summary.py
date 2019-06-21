#!/usr/bin/python
import numpy
import math as m
import matplotlib.pyplot as plt
import os
import sys
import PyFrensie.Utility as Utility
import PyFrensie.Geometry.DagMC as DagMC
import PyFrensie.Utility as Utility
import PyFrensie.MonteCarlo as MonteCarlo
import PyFrensie.MonteCarlo.Collision as Collision
import PyFrensie.MonteCarlo.Event as Event
import PyFrensie.MonteCarlo.Manager as Manager
from spectrum_plot_tools import plotSpectralDataWithErrors

# Set the database path
Collision.FilledGeometryModel.setDefaultDatabasePath( os.environ['DATABASE_PATH'] )

# Reload the simulation
manager = Manager.ParticleSimulationManagerFactory( "infinite_medium_rendezvous_10.xml" ).getManager()

manager.getEventHandler().logObserverSummaries()

