#! /usr/bin/env python
# Luke Kersting
# This script asks for data from multiple energy deposition runs and combines
# them to give the energy deposition by depth.
import math
import numpy as np
import argparse as ap

# Set up the argument parser
description = "This script asks for data from multiple energy deposition runs "\
              "and combines them to give the energy deposition by depth."

parser = ap.ArgumentParser(description=description)

output_msg = "The output file name."
parser.add_argument('-o', help=output_msg, required=False)

calorimeter_msg = "The calorimeter thickness (g/cm2)."
parser.add_argument('-c', help=calorimeter_msg, required=True)

parser.add_argument("input_files", nargs='*')

# Parse the user's arguments
user_args = parser.parse_args()
calorimeter_thickness = float(user_args.c)
file_paths = user_args.input_files

# Number of files
N = len(file_paths)

if N == 0:
  print "No files albedo specified!"
else:
  # Get computational results
  data = np.zeros((2,N))
  depth = np.zeros(N)
  for n in range(N):
      data[:,n] = np.loadtxt(file_paths[n], skiprows=1, dtype=str)
      print file_paths[n]
      question2 = "Enter the range (g/cm2) for this file: "
      depth[n] = raw_input(question2)

  # Get the sorted indices
  # ind = np.argsort(data[0,:])

  # Create the output file
  outputfile = "combined_data.txt"
  if user_args.o:
      outputfile = user_args.o

  question1 = "Enter the desired header name for data file: "
  name = raw_input(question1)

  f = open(outputfile, 'w')
  f.write( "#" )
  f.write( name )
  f.write( "\n#Range (g/cm2)\tEnergy Deposition (MeV-cm2/g)\tError" )

  for i in range(N):
      line = str(depth[i])
      line = line + '\t' + str(data[0,i]/calorimeter_thickness)
      line = line + '\t' + str(data[1,i]/calorimeter_thickness)
      line = '\n' + line

      f.write( line )

  print "Combined data saved to: ",outputfile