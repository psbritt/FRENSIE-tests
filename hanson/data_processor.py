#! /usr/bin/env python
import datetime
import argparse as ap
import subprocess
import sys
import os
import math

def main(argv):

  # Set up the argument parser
  description = "This script pulls estimator information from the "\
                "simulation.h5 file generated after running facemc and "\
                "outputs it to a separate file."

  parser = ap.ArgumentParser(description=description)

  filename_msg = "the simulation.h5 file (with path)"
  parser.add_argument('-f', help=filename_msg, required=True)

  title_msg = "the title of the simulation (e.g. Log-log Correlated Decoupled)"
  parser.add_argument('-t', help=title_msg, required=True)

  # Parse the user's arguments
  user_args = parser.parse_args()

  filename = user_args.f

  # Get output file name
  base = filename[:-3]

  # Check if file exists
  if os.path.isfile(filename):

    today = datetime.date.today()

    degree = math.pi/180.0
    square_degree = degree*degree

    # Read the data file for surface tallies
    with open(filename) as data:
      name = base+"_spectrum.txt"
      out_file = open(name, 'w')

      # Read data from file into lines
      command = "python ../edump.py -f " + filename + " -e 1 -i 48 -b Cosine"
      data = subprocess.check_output(command, shell=True).splitlines()

      # Split lines into columns
      size = len(data)-1
      cosines = [None] * size
      current = [None] * size
      current_error = [None] * size

      for i in range(1,len(data)):
        cosines[i-1], current[i-1], current_error[i-1] = data[i].split(' ')

      # Convert to #/Square Degree
      size = len(cosines)-1
      num_square_degree = [None] * size
      num_square_degree_error = [None] * size
      avg_angle = [None] * size

      for i in range(0, size):
        j = size-i
        k = j-1
        angle_sum = math.acos(float(cosines[j]))/degree + math.acos(float(cosines[k]))/degree
        avg_angle[i] = angle_sum/2.0
        cosine_diff = float(cosines[j]) - float(cosines[k])
        sterradians = 2.0*math.pi*cosine_diff
        num_per_ster = float(current[j])/sterradians
        num_square_degree[i] = num_per_ster*square_degree
        num_square_degree_error[i] = float(current_error[j])/sterradians*square_degree

      # Write title to file
      out_file.write( "# " + user_args.t +"\n")
      # Write data header to file
      header = "# Degrees\t#/Square Degree\tError\t"+str(today)+"\n"
      out_file.write(header)

      # Write data to file
      for i in range(0, size):
          output = '%.4e' % avg_angle[i] + " " + \
                  '%.16e' % num_square_degree[i] + " " + \
                  '%.16e' % num_square_degree_error[i] + "\n"
          out_file.write( output )

  else:
    print "File ",filename," does not exist!"

if __name__ == "__main__":
   main(sys.argv[1:])
