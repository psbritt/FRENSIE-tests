#! /usr/bin/env python
import datetime
import argparse as ap
import subprocess
import sys
import os

def main(argv):

    # Set up the argument parser
    description = "This script pulls energy deposition information from the "\
                  "simulation.h5 file generated after running facemc and "\
                  "outputs it to a separate file."

    parser = ap.ArgumentParser(description=description)

    filename_msg = "the simulation.h5 file (with path)"
    parser.add_argument('-f', help=filename_msg, required=True)

    depth_msg = "the range for the simulation in g/cm2"
    parser.add_argument('-r', help=depth_msg, required=True)

    cal_thickness_msg = "the thickness of the calorimeter for the simulation in g/cm2"
    parser.add_argument('-t', help=cal_thickness_msg, required=True)

    # Parse the user's arguments
    user_args = parser.parse_args()

    filename = user_args.f
    dose_depth = user_args.r
    cal_thickness = user_args.t

    # Get mcnp output file name
    base = filename[:-3]

    # Check if file exists
    if os.path.isfile(filename):

        today = datetime.date.today()
        # Read the mcnp data file for surface tallies
        with open(filename) as data:
            name = base+"_energy_dep.txt"
            file = open(name, 'w')
            header = "# Range (g/cm2)\tEnergy Deposition (MeV cm2/g)\tError\t"+str(today)+"\n"
            file.write(header)
            command = "python ../edump.py -f " + filename + " -e 1 -i total"
            output = subprocess.check_output(command, shell=True)
            header, output, newline = output.split('\n')
            energy_dep_mev, error = output.split(' ')
            data = str(dose_depth) + '\t' + str(float(energy_dep_mev)/float(cal_thickness)) + '\t' + str(float(error)/float(cal_thickness))
            file.write(data)
            file.close()

    else:
        print "File ",filename," does not exist!"

if __name__ == "__main__":
   main(sys.argv[1:])
