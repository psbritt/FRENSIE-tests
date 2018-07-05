#! /usr/bin/env python
# Luke Kersting
# This script asks for albedo data and run names which it then plots.
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib import gridspec
import argparse as ap
import inspect, os
import pylab

# Set up the argument parser
description = "This script asks for albedo data and run names which "\
              "which it then plots against experimental data."

parser = ap.ArgumentParser(description=description)


mcnp_msg = "Flag to plot a comparison with mcnp (the first file should be for mcnp)."
parser.add_argument('-m', help=mcnp_msg, action='store_true')

all_experimental_msg = "Flag to add all experimental data to the generated plot."
parser.add_argument('-a', help=all_experimental_msg, action='store_true')

output_msg = "The output file name."
parser.add_argument('-o', help=output_msg, required=False)

parser.add_argument("input_files", nargs='*')

# Parse the user's arguments
user_args = parser.parse_args()
file_paths = user_args.input_files

# Number of files
N = len(file_paths)

# Number of data points in each file
data_x = [0 for x in range(N)]
data_y = [0 for x in range(N)]
data_error = [0 for x in range(N)]
names = [0 for x in range(N)]

# Get computational results
for n in range(len(file_paths)):
    with open(file_paths[n]) as input:
        names[n] = next(input)
        names[n] = names[n].replace("#","")
        names[n] = names[n].replace("\n","")
        next(input)
        data = zip(*(line.strip().split() for line in input))
        data_x[n] = data[0][:]
        data_y[n] = data[1][:]
        data_error[n] = data[2][:]

# Plot
if user_args.m:
  fig = plt.figure(num=1, figsize=(9,7))
else:
  fig = plt.figure(num=1, figsize=(10,7))

# set height ratios for sublots
if user_args.m:
  gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
else:
  gs = gridspec.GridSpec(1, 1)

# the first subplot
ax0 = plt.subplot(gs[0])

x_label = 'Energy (MeV)'
plt.xlabel(x_label, size=14)
plt.ylabel('Reflection Coef.', size=14)
plt.title('Electron Albedos for an infinite slab of Al', size=16)
ax=plt.gca()

plt.xlim(9e-5,.256)
plt.ylim(0.1,0.26)
if user_args.m:
    plt.xlim(9e-5,.256)
    plt.ylim(0.07,0.22)

markers = ["o","*","v","^","<",">","+","x","1","2","3","4","p","s","h","D","d","H","8"]
if user_args.a:
  exp_names = ['assad', 'bienlein','bishop', 'bongeler', 'bronshtein', 'cosslett', 'drescher', 'heinrich', 'kanter', 'kulenkampff', 'lockwood', 'neubert', 'palluel', 'philibert', 'reimer', 'shimizu', 'soum', 'trump', 'wittry' ]
  exp_names = ['assad', 'bienlein','bishop', 'bongeler', 'bronshtein', 'cosslett', 'drescher', 'heinrich', 'kanter', 'kulenkampff', 'lockwood', 'neubert', 'reimer', 'shimizu', 'soum', 'trump', 'wittry' ]

  # Get experimental data
  directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

  for i in range(len(exp_names)):
    filename = directory + "/al/experimental_results/" + exp_names[i] +".tsv"
    with open(filename) as input:
        name = input.readline().strip()
        input.readline()
        data = zip(*(line.strip().split('\t') for line in input))
        x = [None] * len(data[0][:])
        x = [0 for k in range(len(data[0][:]))]
        y = [0 for k in range(len(data[1][:]))]
        for j in range(len(x)):
          x[j] = float(data[0][j])/1000.0
          y[j] = float(data[1][j])

    plt.scatter(x, y, label=name +" (Exp.)", marker=markers[i], s=50, facecolors='none', edgecolors='b' )
ax.set_xscale('log')


# markers = ["v","^","<",">","s","+","x","1","2","3","4","8","p","*","h","H","X","D","d"]
# markerssizes = [7,7,7,7,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
# marker_color = ['g', 'r', 'c', 'm', 'y', 'k', 'w', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
markers = ["-s","--v","-.o",":^","--p",":*","-.h","-H","--X",":D","-.d","-8"]
markerssizes = [7,8,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]
marker_color = ['g', 'r', 'm', 'k', 'y', 'c', 'g', 'r', 'm', 'k', 'y', 'c']

if user_args.m:
    names = ['MCNP6.2','FACEMC-ACE', 'FACEMC-ENDL' ]
for n in range(N):
    x = map(float, data_x[n])
    y = map(float, data_y[n])
    yerr = map(float, data_error[n])
    plt.errorbar(x, y, yerr=yerr, label=names[n], fmt=markers[n], markersize=markerssizes[n], color=marker_color[n] )

lgd = plt.legend(loc="upper left", bbox_to_anchor=(1,1))
if user_args.m:
  pylab.legend(loc='best')
# plt.legend(loc=3)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#ax.xaxis.set_major_formatter(FormatStrFormatter('%.4f'))
# plt.ylim(0.12,0.22)
# leg = plt.legend(loc='best', ncol=2)
# leg.get_frame().set_alpha(0.5)

if user_args.m:

    # The C/E subplot (with shared x-axis)
    ax1 = plt.subplot(gs[1], sharex = ax0)
    plt.xlabel(x_label, size=14)
    plt.ylabel('C/R', size=14)

    # Get mcnp data
    mcnp_x = map(float, data_x[0])
    mcnp_y = map(float, data_y[0])
    mcnp_yerr = map(float, data_error[0])

    for n in range(1,N):
        x = map(float, data_x[n])
        y = map(float, data_y[n])
        yerr = map(float, data_error[n])

        for i in range(0, len(y)):
          y[i] = y[i]/mcnp_y[i]
          yerr[i] = yerr[i]/mcnp_y[i]
          print mcnp_x[i], ": ", (1.0-mcnp_y[i])*100, "%"

        plt.errorbar(x, y, yerr=yerr, label=names[n], fmt=markers[n], markersize=markerssizes[n], color=marker_color[n] )

        # make x ticks for first suplot invisible
        plt.setp(ax0.get_xticklabels(), visible=False)

        # remove first tick label for the first subplot
        yticks = ax0.yaxis.get_major_ticks()
        yticks[0].label1.set_visible(False)
        ax0.grid(linestyle=':')
        ax1.grid(linestyle=':')


        plt.ylim(0.0,2.0)

        # remove vertical gap between subplots
        plt.subplots_adjust(hspace=.0)

output = "albedo_results.pdf"
if user_args.o:
    output = user_args.o

print "Plot outputted to: ",output
fig.savefig(output, bbox_extra_artists=(lgd,), bbox_inches='tight', dpi=300)
plt.show()