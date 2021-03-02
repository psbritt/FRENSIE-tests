import os
import sys
import math
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from estimators import collisionEstimatorOfEstimators
from estimators import meshVREstimatorOfEstimators

def isClose( test_value, expected_value, reasonable_difference):
  result = False
  if( test_value - reasonable_difference < expected_value and expected_value < test_value + reasonable_difference):
    result = True

  return result

def runCollisionEstimatorTestSuite():
  test_estimator = collisionEstimatorOfEstimators()

  estimator_1_results = {"mean": 1.2, "re": 0.56}
  test_estimator.processEstimator(estimator_1_results)

  if( test_estimator.getMean() != 1.2):
    print('Initial collision mean failure')
  if( test_estimator.getRelativeError() != 0.56):
    print('Initial collision RE Error')

  estimator_2_results = {"mean": 2.5, "re": 0.02}
  test_estimator.processEstimator(estimator_2_results)
  expected_weight_1 = ( 1 / ( 0.56 * 1.2 ) ) ** 2
  expected_weight_2 = ( 1 / ( 2.5 * 0.02 ) ) ** 2
  expected_mean = (expected_weight_1*1.2 + expected_weight_2*2.5)/(expected_weight_1+expected_weight_2)
  if(not isClose(test_estimator.getMean(), expected_mean, 1e-15)):
    print("2nd estimator mean failure")
    print("Expected mean: ", expected_mean)
    print("Resulting mean: ", test_estimator.getMean())

  expected_re = math.sqrt(1/(expected_weight_1+expected_weight_2))/expected_mean
  if(not isClose(test_estimator.getRelativeError(), expected_re, 1e-15)):
    print("2nd estimator RE failure")
    print("Expected RE: ", expected_re)
    print("Resulting RE: ", test_estimator.getRelativeError())

  estimator_3_results = {"mean": 80, "re": 0.99}
  test_estimator.processEstimator(estimator_3_results)
  expected_weight_3 = ( 1 / ( 80 * 0.99 ) ) ** 2
  expected_mean = (expected_weight_1*1.2 + expected_weight_2*2.5 + expected_weight_3*80)/(expected_weight_1+expected_weight_2+expected_weight_3)
  expected_re = math.sqrt(1/(expected_weight_1+expected_weight_2+expected_weight_3))/expected_mean

  if(not isClose(test_estimator.getMean(), expected_mean, 1e-15)):
    print("3rd estimator mean failure")
    print("Expected mean: ", expected_mean)
    print("Resulting mean: ", test_estimator.getMean())

  if(not isClose(test_estimator.getRelativeError(), expected_re, 1e-15)):
    print("3rd estimator RE failure")
    print("Expected RE: ", expected_re)
    print("Resulting RE: ", test_estimator.getRelativeError())

def runMeshVREstimatorTestSuite():
  test_estimator = meshVREstimatorOfEstimators(2, 8, 2)

  estimator_1_results = {0: {"mean": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                             "re":   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, \
                         1: {"mean": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                             "re":   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}}
  test_estimator.processEstimator(estimator_1_results)

  expected_importance_map = {0: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], \
                             1: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
  result_importance_map = test_estimator.getImportanceDictionary()
  for mesh_element in range(2):
    local_expected_importance_list = expected_importance_map[mesh_element]
    local_result_importance_list = result_importance_map[mesh_element]
    for direction_element in range(8):
      for energy_element in range(2):
        local_index = energy_element + direction_element*2
        if not isClose(local_expected_importance_list[local_index], local_result_importance_list[local_index], 1e-15):
          print("Error at ", mesh_element, direction_element, energy_element)
          print("Expected value: ", local_expected_importance_list[local_index])
          print("Result value: ", local_result_importance_list[local_index])

  estimator_2_results = {0: {"mean": [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4], \
                             "re":   [0.1, 0.2, 0.3, 0.4, 0.1, 0.2, 0.3, 0.4, 0.1, 0.2, 0.3, 0.4, 0.1, 0.2, 0.3, 0.4]}, \
                        1: {"mean": [2, 4, 6, 8, 2, 4, 6, 8, 2, 4, 6, 8, 2, 4, 6, 0], \
                            "re":   [0.2, 0.4, 0.6, 0.8, 0.2, 0.4, 0.6, 0.8, 0.2, 0.4, 0.6, 0.8, 0.2, 0.4, 0.6, 0]}}
  test_estimator.processEstimator(estimator_2_results)
  expected_importance_map = {0: [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4], \
                             1: [2, 4, 6, 8, 2, 4, 6, 8, 2, 4, 6, 8, 2, 4, 6, 1] }
  result_importance_map = test_estimator.getImportanceDictionary()                         
  for mesh_element in range(2):
    local_expected_importance_list = expected_importance_map[mesh_element]
    local_result_importance_list = result_importance_map[mesh_element]
    for direction_element in range(8):
      for energy_element in range(2):
        local_index = energy_element + direction_element*2
        if not isClose(local_expected_importance_list[local_index], local_result_importance_list[local_index], 1e-15):
          print("Error at ", mesh_element, direction_element, energy_element)
          print("Expected value: ", local_expected_importance_list[local_index])
          print("Result value: ", local_result_importance_list[local_index])

  estimator_3_results = {0: {"mean": [5, 6, 7, 8, 5, 6, 7, 8, 5, 6, 7, 8, 5, 6, 7, 8], \
                             "re":   [0.5, 0.6, 0.7, 0.8, 0.5, 0.6, 0.7, 0.8, 0.5, 0.6, 0.7, 0.8, 0.5, 0.6, 0.7, 0.8]}, \
                        1: {"mean": [3, 5, 7, 9, 3, 5, 7, 9, 3, 5, 7, 9, 3, 5, 7, 9], \
                            "re":   [0.3, 0.5, 0.7, 0.9, 0.3, 0.5, 0.7, 0.9, 0.3, 0.5, 0.7, 0.9, 0.3, 0.5, 0.7, 0.9]}}
  test_estimator.processEstimator(estimator_3_results)

  #check 2 values since this would be a lot of work
  expected_importance_value_000 = (5*(1/(0.5*5)**2) + 1*(1/(0.1*1)**2)) / ((1/(0.5*5)**2) + (1/(0.1*1)**2))
  expected_importance_value_110 = (7*(1/(0.7*7)**2) + 6*(1/(0.6*6)**2)) / ((1/(0.7*7)**2) + (1/(0.6*6)**2))

  result_importance_map = test_estimator.getImportanceDictionary()
  if( not isClose(result_importance_map[0][0], expected_importance_value_000, 1e-15)):
    print("result importance 000 wrong: ")
    print("expected: ", expected_importance_value_000)
    print("result: ", result_importance_map[0][0])
  if( not isClose(result_importance_map[1][2], expected_importance_value_110, 1e-15)):
    print("result importance 110 wrong: ")
    print("expected: ", expected_importance_value_110)
    print("result: ", result_importance_map[1][2])
  

if __name__ == "__main__":
  runCollisionEstimatorTestSuite()
  runMeshVREstimatorTestSuite()