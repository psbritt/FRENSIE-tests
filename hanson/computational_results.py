#! /usr/bin/env python
import csv
import math
import argparse as ap

# Set up the argument parser
description = "This script takes #/square degree data from MCNP, Native-ACE, "\
              "Native-LinLog and Native-LinLin runs and combines them."

parser = ap.ArgumentParser(description=description)

msg = "#/square degree data .txt files"
parser.add_argument("files", nargs='*', help=msg)

# Parse the user's arguments
user_args = parser.parse_args()
files = user_args.files

# Number of files
N = len(files)
# Number of data points in each file
M = 18

data_x = [[0 for x in range(N)] for y in range(M)]
data_y = [[0 for x in range(N)] for y in range(M)]
data_error = [[0 for x in range(N)] for y in range(M)]

for n in range(N):
    with open(files[n]) as input:
        data = zip(*(line.strip().split(' ') for line in input))
        name = data[0][0] + data[1][0] + data[2][0]
        data_x[n][:] = data[0][1:]
        data_y[n][:] = data[1][1:]
        data_error[n][:] = data[2][1:]


out_file = open("computational_results.txt", "w")
out_file.write("# MCNP\tACE\tLogLogLog\tLinLinLin\tLinLinLog\n")
out_file.write("# Angle (degrees)\t#/square degree\tError\n")

for i in range(M):
    output = data_x[0][i]
    for n in range(N):
        output = output + " " + '%.6e' % float(data_y[n][i]) + " " + \
                                '%.6e' % float(data_error[n][i])
    output = output + "\n"
    out_file.write( output )
out_file.close()

