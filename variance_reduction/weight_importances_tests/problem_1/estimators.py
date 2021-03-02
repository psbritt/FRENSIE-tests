
import math
from argparse import *

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
  def processEstimator(self, estimator_results):
    # Loop over all direction bins and energy bins to process estimator
    for mesh_element in range(self.num_mesh_elements):

      for direction_element in range(self.num_direction_elements):

        for energy_element in range(self.num_energy_elements):

          local_index = energy_element + self.num_energy_elements*direction_element
          iteration_local_mean = estimator_results[mesh_element]["mean"][local_index]
          iteration_local_RE = estimator_results[mesh_element]["re"][local_index]

          if iteration_local_mean > 0:

            iteration_local_weight = 1/(iteration_local_RE*iteration_local_mean)**2
            self.mesh_sum_of_scores_dictionary[mesh_element][local_index] += iteration_local_weight*iteration_local_mean
            self.mesh_sum_of_weights_dictionary[mesh_element][local_index] += iteration_local_weight

  # Form and return importance dictionary
  def getImportanceDictionary(self):
    importance_dictionary = {}
    non_zero_estimator_element_found = False
    min = 0
    # Loop through mesh to check if any element has non-zero answer
    for mesh_element in range(self.num_mesh_elements):
      local_importance_vector = []
      for direction_element in range(self.num_direction_elements):

        for energy_element in range(self.num_energy_elements):
          
          local_index = energy_element + direction_element*self.num_energy_elements
          local_sum_of_scores = self.mesh_sum_of_scores_dictionary[mesh_element][local_index]
          local_sum_of_weights = self.mesh_sum_of_weights_dictionary[mesh_element][local_index]

          if local_sum_of_weights > 0 and local_sum_of_scores > 0:
            local_importance_value = local_sum_of_scores / local_sum_of_weights
            local_importance_vector.append(local_importance_value)

            if not non_zero_estimator_element_found:
              min = local_importance_value
              non_zero_estimator_element_found = True
            else:
              if min > local_importance_value:
                min = local_importance_value
          else:
            local_importance_vector.append(0)
      importance_dictionary[mesh_element] = local_importance_vector
    
    # Estimator has no results, just give a flat importance function
    if not non_zero_estimator_element_found:
      importance_dictionary = self.getFlatDictionary(1)

    # Estimator has results, give zero values same value as minimum importance value
    else:
      for mesh_element in range(self.num_mesh_elements):
        
        for direction_element in range(self.num_direction_elements):

          for energy_element in range(self.num_energy_elements):

            if importance_dictionary[mesh_element][local_index] == 0:
              importance_dictionary[mesh_element][local_index] = min

    return importance_dictionary

  # Produce a weight importance dictionary. Note: reference_weight and reference_importance must be for the SAME element. Must have non-zero importances/weights
  def getWeightImportanceDictionary( self, reference_weight, reference_importance, importance_dictionary ):
    weight_importance_dictionary = {}

    for mesh_element in range(self.num_mesh_elements):

      local_weight_importance_vector = []

      for direction_element in range(self.num_direction_elements):

        for energy_element in range(self.num_energy_elements):

          local_index = energy_element + direction_element*self.num_energy_elements
          local_importance = importance_dictionary[mesh_element][local_index]
          local_weight_importance_vector.append( reference_weight*reference_importance/local_importance)

      weight_importance_dictionary[mesh_element] = local_weight_importance_vector