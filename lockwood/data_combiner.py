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

parser.add_argument("input_files", nargs='*')

# Parse the user's arguments
user_args = parser.parse_args()
file_paths = user_args.input_files

# Number of files
N = len(file_paths)

if N == 0:
  print "No files albedo specified!"
else:
  # Get computational results
  data = np.zeros((3,N))
  for n in range(N):
      data[:,n] = np.loadtxt(file_paths[n], skiprows=1, dtype=str)

  # Get the sorted indices
  ind = np.argsort(data[0,:])

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

  for i in ind:
      line = str(data[0,i])
      line = line + '\t' + str(data[1,i])
      line = line + '\t' + str(data[2,i])
      line = '\n' + line

      f.write( line )

  print "Combined data saved to: ",outputfile