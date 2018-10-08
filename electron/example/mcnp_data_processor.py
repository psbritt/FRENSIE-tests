#! /usr/bin/env python
import datetime
import argparse as ap
import os
import shutil
import sys, getopt
from subprocess import call

def main(argv):

  # Set up the argument parser
  description = "This script pulls estimator information from the "\
                "simulation.o file generated after running mcnp and "\
                "outputs it to a separate file."

  parser = ap.ArgumentParser(description=description)

  filename_msg = "the simulation.o file (with path)"
  parser.add_argument('-f', help=filename_msg, required=True)

  # Parse the user's arguments
  user_args = parser.parse_args()

  filename = user_args.f

  # Get output file name
  base = filename[:-2]

  cell_list = ['100']
  surface_list = ['10']
  estimator_list = ['current', 'flux' ]
  estimator_names = ["Surface Current (#)", "Surface Flux (#/cm$^2$)" ]

  # Get mcnp output file name
  mcnp_output = filename+".o"

  # Check if file exists
  if os.path.isfile(filename):

      today = datetime.date.today()
      # Read the mcnp data file for surface tallies
      with open(filename) as data:
          # go through all surface tallies
          for i in surface_list:
              start=" surface  "+i

              # go through the current and flux estimators
              for j in range(len(estimator_list)):
                  name = base + "_" + estimator_list[j] + ".txt"
                  file = open(name, 'w')
                  # Write title to file
                  file.write( "# MCNP6.2\n")
                  # Write data header to file
                  header = "# Energy (MeV)\t"+estimator_names[j]+"\tSigma\t"+str(today)+"\n"
                  file.write(header)
                  # Skips text before the beginning of the interesting block:
                  for line in data:
                      if line.startswith(start):
                          data.next()
                          break
                  # Reads text until the end of the block:
                  for line in data:  # This keeps reading the file
                      if line.startswith('      total'):
                          file.close()
                          break
                      line = line.lstrip()
                      line = line.replace('   ','\t')
                      line = line.replace(' ','\t')
                      file.write(line)

      with open(filename) as data:
          # go through all surface tallies
          for i in cell_list:
              start=" cell  "+i

              # go track_flux estimator
              name = base+"_track_flux.txt"
              file = open(name, 'w')
              # Write title to file
              file.write( "# MCNP6.2\n")
              # Write data header to file
              header = "# Energy (MeV)\t"+"Track Flux (#/cm$^2$)"+"\tSigma\t"+str(today)+"\n"
              file.write(header)
              # Skips text before the beginning of the interesting block:
              for line in data:
                  if line.startswith(start):
                      data.next()
                      break
              # Reads text until the end of the block:
              for line in data:  # This keeps reading the file
                  if line.startswith('      total'):
                      file.close()
                      break
                  line = line.lstrip()
                  line = line.replace('   ','\t')
                  line = line.replace(' ','\t')
                  file.write(line)

  else:
      print "File: ",filename," does not exist!"

if __name__ == "__main__":
   main(sys.argv[1:])
