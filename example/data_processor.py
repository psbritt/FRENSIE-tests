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
    tallies = ["track_flux", "flux", "current"]
    names = ["Track Flux (#/cm$^2$)", "Surface Flux (#/cm$^2$)", "Surface Current (#)"]
    # Read the data file for surface tallies
    with open(filename) as data:
      for j in range(len(tallies)):
        name = base+"_"+tallies[j]+".txt"
        out_file = open(name, 'w')

        # Read data from file into lines
        command = "python ../edump.py -f " + filename + " -e " + str(j+1) +" -i 1 -b Energy"
        data = subprocess.check_output(command, shell=True).splitlines()
        data = data[1:]

        # Split lines into columns
        size = len(data)-1
        x = [None] * size
        y = [None] * size
        error = [None] * size

        for i in range(1,len(data)):
          x[i-1], y[i-1], error[i-1] = data[i].split(' ')

        # Write title to file
        out_file.write( "# " + user_args.t +"\n")
        # Write data header to file
        header = "# Energy (MeV)\t" + names[j] + "\tSigma\t"+str(today)+"\n"
        out_file.write(header)

        # Write data to file
        for i in range(0, size):
            output = x[i] + "\t" + \
                     y[i] + "\t" + \
                     error[i] + "\n"
            out_file.write( output )

  else:
    print "File ",filename," does not exist!"

if __name__ == "__main__":
   main(sys.argv[1:])
