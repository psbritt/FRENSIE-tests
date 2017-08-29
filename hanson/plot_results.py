#! /usr/bin/env python
# Luke Kersting
# This script asks for #/square degree data and run names which it then plots.
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import argparse as ap

# Set up the argument parser
description = "This script asks for #/square degree data and run names which "\
              "which it then plots."

parser = ap.ArgumentParser(description=description)

mcnp_msg = "MCNP #/square degree data .txt file"
parser.add_argument("input_files", nargs='*')

# Parse the user's arguments
user_args = parser.parse_args()
file_paths = user_args.input_files

# Number of files
N = len(file_paths) + 1

# Number of data points in each file
M = 18
data_x = [[0 for x in range(N)] for y in range(M)]
data_y = [[0 for x in range(N)] for y in range(M)]
data_error = [[0 for x in range(N)] for y in range(M)]
names = [0 for x in range(N)]

# Get experimental data
names[0] = "Hanson"
with open("experimental_results.txt") as input:
    data = zip(*(line.strip().split(' ') for line in input))
    data_name = data[0][0] + data[1][0] + data[2][0]
    data_x[0][0:17] = data[0][1:]
    data_y[0][0:17] = data[1][1:]
    data_error[0][0:17] = data[2][1:]

# Get computational results
for n in range(len(file_paths)):
    question = "Enter the desired plot name to data file (" + file_paths[n] + "): "
    names[n+1] = raw_input(question)

    with open(file_paths[n]) as input:
        data = zip(*(line.strip().split(' ') for line in input))
        data_name = data[0][0] + data[1][0] + data[2][0]
        data_x[n+1][0:17] = data[0][1:]
        data_y[n+1][0:17] = data[1][1:]
        data_error[n+1][0:17] = data[2][1:]

fig = plt.figure(num=1, figsize=(10,5))
plt.xlabel('Angle (Degree)', size=14)
plt.ylabel('#/Square Degrees', size=14)
plt.title('$\mathrm{15.7\/MeV\/Electron\/Angular\/Distribution\/from\/a\/9.658\/\mu m\/Gold\/Foil}$', size=16)
ax=plt.gca()

plt.xlim(0.0,30.0)
plt.ylim(-0.005,0.06)

markers = ["o","v","s","+","x","^","<",">","1","2","3","4","8","p","P","*","h","H","X","D","d"]
for n in range(N):
    x = map(float, data_x[n])
    y = map(float, data_y[n])
    yerr = map(float, data_error[n])
    plt.errorbar(x, y, yerr=yerr, label=names[n], fmt=markers[n] )
plt.legend(loc=1)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#ax.xaxis.set_major_formatter(FormatStrFormatter('%.4f'))
fig.savefig('./hanson_results.pdf', bbox_inches='tight')

## Get MCNP data
#mcnp_file ="/home/lkersting/frensie/tests/hanson/results/mcnp/latest/mcnp_spectrum.txt"
#if user_args.m:
#    mcnp_file = user_args.m
#with open(mcnp_file) as input:
#    data = zip(*(line.strip().split(' ') for line in input))
#    name = data[0][0] + data[1][0] + data[2][0]
#    mcnp_angles = data[0][1:]
#    mcnp_result = data[1][1:]
#    mcnp_error = data[2][1:]

## Get Native-ACE data
#ace_file ="/home/lkersting/frensie/tests/hanson/results/ace/latest/hanson_ace_spectrum.txt"
#if user_args.a:
#    ace_file = user_args.a
#with open(ace_file) as input:
#    data = zip(*(line.strip().split(' ') for line in input))
#    name = data[0][0] + data[1][0] + data[2][0]
#    ace_angles = data[0][1:]
#    ace_result = data[1][1:]
#    ace_error = data[2][1:]

## Get Native-LinLog data
#with open(user_args.l) as input:
#    data = zip(*(line.strip().split(' ') for line in input))
#    name = data[0][0] + data[1][0] + data[2][0]
#    log_angles = data[0][1:]
#    log_result = data[1][1:]
#    log_error = data[2][1:]

## Get Native-LinLin data
#with open(user_args.f) as input:
#    data = zip(*(line.strip().split(' ') for line in input))
#    name = data[0][0] + data[1][0] + data[2][0]
#    lin_angles = data[0][1:]
#    lin_result = data[1][1:]
#    lin_error = data[2][1:]


## Make sure the data is all the same size
#if mcnp_angles == ace_angles == log_angles == lin_angles:

#    out_file = open("computational_results.txt", "w")
#    out_file.write("# MCNP\tACE\tLinLin\tLinLog\n")
#    out_file.write("# Angle (degrees)\t#/square degree\tError\n")

#    for i in range(0, len(mcnp_angles)):
#        output = '%.3e'% float(mcnp_angles[i]) + " " + \
#                 '%.6e' % float(mcnp_result[i]) + " " + \
#                 '%.6e' % float(mcnp_error[i]) + " " + \
#                 '%.10e' % float(ace_result[i]) + " " + \
#                 '%.10e' % float(ace_error[i]) + " " + \
#                 '%.10e' % float(lin_result[i]) + " " + \
#                 '%.10e' % float(lin_error[i]) + " " + \
#                 '%.10e' % float(log_result[i]) + " " + \
#                 '%.10e' % float(log_error[i]) + "\n"
#        out_file.write( output )
#    out_file.close()

#else:
#    print "Error: data in files does not match!"
