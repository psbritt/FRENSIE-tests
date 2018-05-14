#! /usr/bin/env python
# Luke Kersting
# This script asks for energy deposition data and run names which it then plots.
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import argparse as ap

# Set up the argument parser
description = "This script asks for energy deposition data and run names which "\
              "which it then plots."

parser = ap.ArgumentParser(description=description)


experimental_msg = "Flag to add the experimental data to the generated plot."
parser.add_argument('-e', help=experimental_msg, action='store_true')

output_msg = "The output file name."
parser.add_argument('-o', help=output_msg, required=False)

parser.add_argument("input_files", nargs='*')

# Parse the user's arguments
user_args = parser.parse_args()
file_paths = user_args.input_files

# Number of files
N = len(file_paths)

# Number of data points in each file
M = 11
data_x = [[0 for x in range(N)] for y in range(M)]
data_y = [[0 for x in range(N)] for y in range(M)]
data_error = [[0 for x in range(N)] for y in range(M)]
names = [0 for x in range(N)]

# Get computational results
for n in range(N):
    # question = "Enter the desired plot name to data file (" + file_paths[n] + "): "
    # names[n] = raw_input(question)

    with open(file_paths[n]) as input:
        names[n] = input.readline().strip()[1:]
        print names[n]
        data = zip(*(line.strip().split('\t') for line in input))
        data_name = data[0][0] + data[1][0] + data[2][0]
        data_x[n][0:M] = data[0][1:]
        data_y[n][0:M] = data[1][1:]
        data_error[n][0:M] = data[2][1:]

        # for i in range(0, M):
        #   data_y[n][i] = float(data_y[n][i])/float(data_x[n][i])
        #   data_error[n][i] = float(data_error[n][i])/float(data_x[n][i])

fig = plt.figure(num=1, figsize=(10,5))
plt.xlabel('Range ($\mathrm{g/cm^2}$)', size=14)
plt.ylabel('Dose ($\mathrm{MeV\/cm^2/g}$)', size=14)
plt.title('$\mathrm{Energy\/Deposition\/from\/0.314\/MeV\/Electron\/in\/Aluminum}$', size=16)
ax=plt.gca()

plt.xlim(0.0,0.1)
plt.ylim(0.0,6.0)

if user_args.e:
    # Get experimental data
    with open("./Al_0.314/experimental_results.txt") as input:
        data = zip(*(line.strip().split('\t') for line in input))
        data_name = data[0][0] + data[1][0] + data[2][0]
        exp_x = data[0][1:]
        exp_y = data[1][1:]
        # Error is given in %
        exp_error = data[2][1:]

    # Calculate the experimental from the % error
    x = map(float, exp_x)
    y = map(float, exp_y)
    # plt.scatter(x, y, label="Lockwood (Exp.)", marker='s' )
    yerr = map(float, exp_error)
    for i in range(0, len(yerr)):
        yerr[i] = yerr[i]*y[i]/100.0
    plt.errorbar(x, y, yerr=yerr, label="Lockwood (Exp.)", fmt="s", markersize=5 )


markers = ["v","o","^","<",">","+","x","1","2","3","4","8","p","P","*","h","H","X","D","d"]
markerssizes = [6,5,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
marker_color = ['g', 'r', 'c', 'm', 'y', 'k', 'w', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
for n in range(N):
    x = map(float, data_x[n])
    y = map(float, data_y[n])
    yerr = map(float, data_error[n])
    plt.errorbar(x, y, yerr=yerr, label=names[n], fmt=markers[n], markersize=markerssizes[n], color=marker_color[n])
plt.legend(loc=1)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#ax.xaxis.set_major_formatter(FormatStrFormatter('%.4f'))

output = "lockwood_results.pdf"
if user_args.o:
    output = user_args.o

print "Plot outputted to: ",output
fig.savefig(output, bbox_inches='tight', dpi=300)
plt.show()