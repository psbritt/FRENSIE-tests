#! /usr/bin/env python
# Luke Kersting
# This script asks for energy deposition data and run names which it then plots.
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter
import argparse as ap
import inspect, os

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

    with open(file_paths[n]) as input:
        names[n] = input.readline().strip()[1:]
        data = zip(*(line.strip().split('\t') for line in input))
        data_name = data[0][0] + data[1][0] + data[2][0]
        data_x[n][0:M] = data[0][1:]
        data_y[n][0:M] = data[1][1:]
        data_error[n][0:M] = data[2][1:]

# Plot
fig = plt.figure(num=1, figsize=(10,6))

# set height ratios for sublots
gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])

# the first subplot
ax0 = plt.subplot(gs[0])

# x_label = 'Range ($\mathrm{g/cm^2}$)'
x_label = 'Fraction of a Mean Range'
x_data =[0.0045, 0.0165, 0.0317, 0.0448, 0.0591, 0.0707, 0.0836, 0.0987, 0.1150, 0.1270, 0.1420, 0.1740, 0.1950, 0.2210, 0.2530, 0.2800, 0.3200, 0.3730, 0.3910, 0.4310, 0.4430, 0.5110, 0.5520, 0.6210, 0.7360, 0.8460]

plt.xlabel(x_label, size=14)
plt.ylabel('Dose ($\mathrm{MeV\/cm^2/g}$)', size=14)
plt.title('$\mathrm{Energy\/Deposition\/from\/0.314\/MeV\/Electron\/in\/Aluminum}$', size=16)
ax=plt.gca()


plt.xlim(0.0,0.9)
# plt.ylim(0.0,6.0)
plt.ylim(0.0,12.0)

if user_args.e:
    # Get experimental data
    directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = directory + "/experimental_results.txt"
    with open(filename) as input:
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
    line0,err0,arg3, = ax0.errorbar(x_data[0:12], y[0:12], yerr=yerr[0:12], label="Lockwood (Exp.)", fmt="-s", markersize=5 )


markers = ["--v","-.o",":^","--<","-.>",":+","--x","-.1",":2","--3","-.4",":8","--p","-.P",":*","--h","-.H",":X","--D","-.d"]
markerssizes = [6,5,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
marker_color = ['g', 'r', 'c', 'm', 'y', 'k', 'w', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
# names = ['MCNP6.2','FRENSIE-ACE', 'FRENSIE-ENDL' ]
for n in range(N):
    x = map(float, data_x[n])
    y = map(float, data_y[n])
    yerr = map(float, data_error[n])
    plt.errorbar(x_data[0:12], y[0:12], yerr=yerr[0:12], label=names[n], fmt=markers[n], markersize=markerssizes[n], color=marker_color[n])
# plt.legend(loc=3)
plt.legend(loc=1)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#ax.xaxis.set_major_formatter(FormatStrFormatter('%.4f'))

markers = ["v","o","^","<",">","+","x","1","2","3","4","8","p","P","*","h","H","X","D","d"]
if user_args.e:

    # The C/E subplot (with shared x-axis)
    ax1 = plt.subplot(gs[1], sharex = ax0)
    plt.xlabel(x_label, size=14)
    plt.ylabel('C/E', size=14)

    # Get experimental data
    directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = directory + "/experimental_results.txt"
    with open(filename) as input:
        data = zip(*(line.strip().split('\t') for line in input))
        data_name = data[0][0] + data[1][0] + data[2][0]
        exp_x = data[0][1:]
        exp_y = data[1][1:]
        # Error is given in %
        exp_error = data[2][1:]

    # Calculate the experimental from the % error
    x = map(float, exp_x)
    experimental_y = map(float, exp_y)

    for n in range(N):
        x = map(float, data_x[n])
        y = map(float, data_y[n])
        yerr = map(float, data_error[n])

        print names[n]
        for i in range(0, len(y)):
          # print "y: ", y[i], "\ty_exp: ", experimental_y[i]
          y[i] = y[i]/experimental_y[i]
          yerr[i] = yerr[i]/experimental_y[i]
          print i, ": ", (1.0-y[i])*100, "%"
        ax1.errorbar(x_data[0:12], y[0:12], yerr=yerr[0:12], label=names[n], fmt=markers[n], markersize=markerssizes[n], color=marker_color[n])

    # make x ticks for first suplot invisible
    plt.setp(ax0.get_xticklabels(), visible=False)

    # remove first tick label for the first subplot
    yticks = ax0.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    ax0.grid(linestyle=':')
    ax1.grid(linestyle=':')

    # plt.ylim(0.5,3.0)
    # plt.ylim(0.85,1.15)
    plt.ylim(0.0,2.5)

    # remove vertical gap between subplots
    plt.subplots_adjust(hspace=.0)

output = "lockwood_results.pdf"
if user_args.o:
    output = user_args.o

print "Plot outputted to: ",output
fig.savefig(output, bbox_inches='tight', dpi=600)
plt.show()