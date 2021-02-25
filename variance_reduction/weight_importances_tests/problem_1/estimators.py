import numpy
import os
import sys
import math
from argparse import *
import PyFrensie.Geometry as Geometry
from problem_1_run_simulation import simulate
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


class collisionEstimatorOfEstimators:
  def __init__(self):
    self.sum_of_scores = 0
    self.sum_of_weights = 0
  # Takes an iteration result and processes it for mean of means and variance of mean of means
  def processEstimator(self, estimator):

    iteration_mean = estimator["mean"]
    iteration_RE = estimator["re"]
    if iteration_mean > 0:
      iteration_weight = 1/(iteration_RE*iteration_mean)**2
      self.sum_of_scores += iteration_weight*iteration_mean
      self.sum_of_weights += iteration_weight

  # Gives the current mean
  def getMean(self):

    if self.sum_of_scores > 0:
      return self.sum_of_scores/self.sum_of_weights
    else:
      return 0

  def getRelativeError(self):

    if self.getMean() > 0:
      return math.sqrt(1/self.sum_of_weights)/self.getMean()
    else:
      return 0

# Class that handles the estimator of estimators for the VR portion
class meshVREstimatorOfEstimators:
  def __init__(self, num_mesh_elements, num_direction_elements, num_energy_elements):
    
    # Store this data b/c it's useful
    self.num_mesh_elements = num_mesh_elements
    self.num_direction_elements = num_direction_elements
    self.num_energy_elements = num_energy_elements

    # Initialize estimator numerators/denominators
    self.mesh_sum_of_weights_dictionary = self.getFlatDictionary( 0 )
    self.mesh_sum_of_scores_dictionary = self.getFlatDictionary( 0 )

  # Function to initialize estimator of estimator
  def getFlatDictionary( self, initialization_value ):

    estimator_dictionary = {}
    for mesh_element in range( self.num_mesh_elements ):

      local_score_vector = []
      for direction_element in range( self.num_direction_elements ):
        
        for energy_element in range( self.num_energy_elements ):
          
          local_score_vector.append(initialization_value)

      estimator_dictionary[mesh_element] = local_score_vector
    return estimator_dictionary

  # Process simulation estimators to update local estimator of estimator
  def processEstimator(self, element_estimator_results, mesh_element):

    # Loop over all direction bins and energy bins to process estimator
    for direction_element in range(self.num_direction_elements):

      for energy_element in range(self.num_energy_elements):

        local_index = energy_element + self.num_energy_elements*direction_element
        iteration_local_mean = element_estimator_results["mean"][local_index]
        iteration_local_RE = element_estimator_results["re"][local_index]

        if iteration_local_mean > 0:

          iteration_local_weight = 1/(iteration_local_RE*iteration_local_mean)**2
          self.mesh_sum_of_scores_dictionary[mesh_element][local_index] += iteration_local_weight*iteration_local_mean
          self.mesh_sum_of_weights_dictionary[mesh_element][local_index] += iteration_local_weight

  # Form and return importance dictionary
  def getImportanceDictionary(self):
    importance_dictionary = {}
    non_zero_estimator_element_found = False
    # Loop through mesh to check if any element has non-zero answer
    for mesh_element in range(self.num_mesh_elements):

      for direction_element in range(self.num_direction_elements):

        for energy_element in range(self.num_energy_elements):
          
          local_index = energy_element + direction_element*self.num_energy_elements
          local_value = self.mesh_sum_of_scores_dictionary[mesh_element][local_index]*self.mesh_sum_of_weights_dictionary[mesh_element][local_index]

          if local_value > 0:

            if non_zero_estimator_element_found:

              if local_value < min:
                min = local_value

            else:
              non_zero_estimator_element_found = True
              #Also set min for next search
              min = local_value

    if not non_zero_estimator_element_found:

      importance_dictionary = self.getFlatDictionary(1)

    else:

      for mesh_element in range(self.num_mesh_elements):

        local_vector = []
        for direction_element in range(self.num_direction_elements):
          
          for energy_element in range(self.num_energy_elements):
            
            local_index = energy_element + direction_element*self.num_energy_elements
            local_value = self.mesh_sum_of_scores_dictionary[mesh_element][local_index]*self.mesh_sum_of_weights_dictionary[mesh_element][local_index]
            
            if local_value > 0:

              local_vector.append(local_value)
            
            else:

              local_vector.append(min)

        importance_dictionary[mesh_element] = local_vector

    return importance_dictionary

  # Produce a weight importance dictionary. Note: reference_weight and reference_importance must be for the SAME element. Must have non-zero importances/weights
  def getWeightImportanceDictionary( self, reference_weight, reference_importance, importance_dictionary ):
    weight_importance_dictionary = {}

    for mesh_element in range(self.num_mesh_elements):

      local_weight_importance_vector = []

      for direction_element in range(self.num_direction_elements):

        for energy_element in range(self.num_energy_elements):

          local_index = energy_element + direction_element*energy_element
          local_importance = importance_dictionary[mesh_element][local_index]
          local_weight_importance_vector.append( reference_weight*reference_importance/local_importance)

      weight_importance_dictionary[mesh_element] = local_weight_importance_vector