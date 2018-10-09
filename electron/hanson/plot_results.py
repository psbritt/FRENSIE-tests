#! /usr/bin/env python
# Luke Kersting
# This script asks for transmission (Frac/Deg2) data and run names which it then plots.
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter
import argparse as ap
import inspect, os

# Set up the argument parser
description = "This script asks for transmission (Frac/Deg2) data and run names which "\
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
M = 18
data_x = [[] for y in range(N)]
data_y = [[] for y in range(N)]
data_error = [[] for y in range(N)]
names = [0 for x in range(N)]

# Get computational results
for n in range(N):

    with open(file_paths[n]) as input:
        names[n] = input.readline()[1:].strip()
        print names[n]
        print input.readline().strip()[1:]
        data = zip(*(line.strip().split('\t') for line in input))
        data_x[n] = np.asfarray(data[0][0:M])
        data_y[n] = np.asfarray(data[1][0:M])
        data_error[n] = np.asfarray(data[2][0:M])*data_y[n]

# Plot
fig = plt.figure(num=1, figsize=(10,6))

# set height ratios for sublots
gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])

# the first subplot
ax0 = plt.subplot(gs[0])

x_label = 'Angle (Degree)'
plt.xlabel(x_label, size=14)
plt.ylabel('#/Square Degrees', size=14)
plt.title('$\mathrm{15.7\/MeV\/Electron\/Angular\/Distribution\/from\/a\/9.658\/\mu m\/Gold\/Foil}$', size=16)
ax=plt.gca()

plt.xlim(0.0,7.0)
plt.ylim(0.0,0.05)

if user_args.e:
    # Get experimental data
    directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = directory + "/experimental_results.tsv"
    with open(filename) as input:
        data = zip(*(line.strip().split('\t') for line in input))
        exp_x = np.asfarray(data[0][1:14])
        exp_y = np.asfarray(data[1][1:14])

    plt.plot(exp_x, exp_y, label="Hanson (Exp.)", marker='s', markersize=5 )

markers = ["--v","-.o",":^","--<","-.>",":+","--x","-.1",":2","--3","-.4",":8","--p","-.P",":*","--h","-.H",":X","--D","-.d"]
markerssizes = [6,5,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
marker_color = ['g', 'r', 'c', 'm', 'y', 'k', 'w', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
# names = ['MCNP6.2','FRENSIE-ACE', 'FRENSIE-ENDL' ]
for n in range(N):
    # Insert first bin lower bounds as an angle of 0
    x = np.insert( data_x[n], 0, 0.0)

    # Calculate bin mid points
    mid = 0.5*(x[1:] + x[:-1])

    plt.errorbar(mid, data_y[n], yerr=data_error[n], label=names[n], fmt=markers[n], markersize=markerssizes[n], color=marker_color[n] )
plt.legend(loc=1)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#ax.xaxis.set_major_formatter(FormatStrFormatter('%.4f'))

markers = ["v","o","^","<",">","+","x","1","2","3","4","8","p","P","*","h","H","X","D","d"]
if user_args.e:

    # The C/E subplot (with shared x-axis)
    ax1 = plt.subplot(gs[1], sharex = ax0)
    plt.xlabel(x_label, size=14)
    plt.ylabel('C/E', size=14)

    for n in range(N):
        # Insert first bin lower bounds as an angle of 0
        x = np.insert( data_x[n], 0, 0.0)

        # Calculate C/R
        yerr = data_error[n]/exp_y
        y = data_y[n]/exp_y

        # Calculate bin mid points
        mid = 0.5*(x[1:] + x[:-1])

        for i in range(0, len(y)):
          print i, ": ", (1.0-y[i])*100, u"\u00B1", yerr[i]*100, "%"
        ax1.errorbar(mid, y, yerr=yerr, label=names[n], fmt=markers[n], markersize=markerssizes[n], color=marker_color[n])

    # make x ticks for first suplot invisible
    plt.setp(ax0.get_xticklabels(), visible=False)

    # remove first tick label for the first subplot
    yticks = ax0.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    ax0.grid(linestyle=':')
    ax1.grid(linestyle=':')

    plt.xlim(0.0,7.0)
    plt.ylim(0.8,1.3)
    # plt.ylim(0.5,1.8)
    # plt.ylim(0.2,2.5)

    # remove vertical gap between subplots
    plt.subplots_adjust(hspace=.0)

output = "hanson_results.pdf"
if user_args.o:
    output = user_args.o

print "Plot outputted to: ",output
fig.savefig(output, bbox_inches='tight', dpi=600)
plt.show()