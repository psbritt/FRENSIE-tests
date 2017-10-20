#! /usr/bin/env python
# Luke Kersting
# This script asks for data from multiple albedo runs and combines thems to give
# an energy distribution of albedos.
import math
import numpy as np
import argparse as ap

# Set up the argument parser
description = "This script asks for data from multiple albedo runs and "\
              "combines thems to give an energy distribution of albedos."

parser = ap.ArgumentParser(description=description)

output_msg = "The output file name."
parser.add_argument('-o', help=output_msg, required=False)

parser.add_argument("input_files", nargs='*')

# Parse the user's arguments
user_args = parser.parse_args()
file_paths = user_args.input_files

# Number of files
N = len(file_paths)

# Get computational results
data = np.zeros((3,N))
for n in range(N):
    data[:,n] = np.loadtxt(file_paths[n], skiprows=1, dtype=str)

# Get the sorted indices
ind = np.lexsort(data)

# Create the output file
outputfile = "combined_data.txt"
if user_args.o:
    outputfile = user_args.o

f = open(outputfile, 'w')
f.write( "#Energy\tAlbedo\tError\n" )

for i in ind:
    line = str(data[0,i])
    line = line + ' ' + str(data[1,i])
    line = line + ' ' + str(data[2,i])
    line = line + '\n'

    f.write( line )

print "Combined data saved to: ",outputfile