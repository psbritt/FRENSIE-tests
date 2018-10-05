#! /usr/bin/env python
import argparse as ap
import h5py

# Set up the argument parser
description = "This script allows one to pull attribute information from the "\
              "simulation.h5 file generated after running facemc. The output "\
              "is dumped to the screen."

parser = ap.ArgumentParser(description=description)

simulation_file_msg = "the simulation.h5 file (with path)"
parser.add_argument('-f', help=simulation_file_msg, required=True)

# Parse the user's arguments
user_args = parser.parse_args()

# Open the simulation.h5 file
hdf5_file = h5py.File(user_args.f,'r')
for item in hdf5_file.attrs.keys():
    print item + ":", hdf5_file.attrs[item]

hdf5_file.close()

