#! /usr/bin/env python
# Luke Kersting
# This script asks for energy bin data and plots the distribution and C/R.
import numpy as np
from numpy import exp, linspace
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter
from matplotlib.lines import Line2D
import argparse as ap
import inspect, os
from lmfit import Model
import os.path
import pylab

def gaussian(x, amp, wid):
  return amp * exp(-x*x /(wid*wid) )

# Set up the argument parser
description = "This script asks for energy bin data and plots the distribution and C/R."

parser = ap.ArgumentParser(description=description)

comparison_msg = "Flag to plot the C/R data."
parser.add_argument('-c', help=comparison_msg, action='store_true')

mcnp_msg = "The MCNP energy bin data file."
parser.add_argument('-m', help=mcnp_msg)

output_msg = "The output file name."
parser.add_argument('-o', help=output_msg, required=False)

parser.add_argument("input_files", nargs='*')

# Plot every bth error bar
b = 3
# Set the y max and min for the main plot
xmax = 0.0075
xmin = 0.0
# Set the y max and min for the main plot
ymax = 500.0
ymin = 0.0

# Parse the user's arguments
user_args = parser.parse_args()
file_paths = user_args.input_files

# Number of files
N = len(file_paths)

# Number of data points in each file
data_x = [[] for y in range(N)]
data_y = [[] for y in range(N)]
data_rel_error = [[] for y in range(N)]
names = [0 for x in range(N)]

nmax = 0
# Get computational results
for n in range(N):
    with open(file_paths[n]) as input:
        # Read name of data
        names[n] = input.readline()[1:].strip()
        print names[n]
        # Read the data header
        input.readline()[1:].strip()
        # Read the data
        data = zip(*(line.strip().split('\t') for line in input))
        # get bins within max energy
        for i in range(len(data[0])):
          if float(data[0][i]) <= xmax+1e-5:
            nmax = i

        data_x[n] = np.asfarray(data[0][:nmax])
        data_y[n] = np.asfarray(data[1][:nmax])
        data_rel_error[n] = np.asfarray(data[2][:nmax])

# Get MCNP results
if os.path.isfile(user_args.m):
    with open(user_args.m) as input:
        # Read name of data
        mcnp_name = input.readline()[1:].strip()
        print mcnp_name
        # Read the data header
        labels = input.readline()[1:].strip().split('\t')
        # Read the data
        data = zip(*(line.strip().split('\t') for line in input))
        mcnp_x = np.asfarray(data[0][:nmax])
        mcnp_y = np.asfarray(data[1][:nmax])
        mcnp_rel_error = np.asfarray(data[2][:nmax])

for x in range(len(data_x[0])):
  diff = mcnp_x[x] - data_x[0][x]
  if diff > 0.0:
    print mcnp_x[x], " diff = ", mcnp_x[x] - data_x[0][x]

# Calculate the average value in the bin
mcnp_avg_x = 0.5*(mcnp_x[1:] + mcnp_x[:-1])
mcnp_avg_y = mcnp_y[1:]/(mcnp_x[1:]-mcnp_x[:-1])
mcnp_avg_error = mcnp_rel_error[1:]*mcnp_avg_y

# Set plot and subplots
if user_args.c:
  fig = plt.figure(num=1, figsize=(9,7))
  gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
else:
  fig = plt.figure(num=1, figsize=(10,5))
  gs = gridspec.GridSpec(1, 1)

# the first subplot
ax0 = plt.subplot(gs[0])

# Use the labels from the mcnp file
plt.xlabel(labels[0], size=14)
plt.ylabel(labels[1], size=14)

# Get the plot title
# question = "Enter the desired title for the plot: "
# title = raw_input(question)
title = "Surface Current for a Point Source in a H Sphere"
plt.title(title, size=16)
ax=plt.gca()

plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)

# Plot MCNP results
if os.path.isfile(user_args.m):
  plt1 = plt.errorbar(mcnp_avg_x, mcnp_avg_y, yerr=mcnp_avg_error, linestyle='-', label=mcnp_name, errorevery=b )


markers = ["--v","-.o",":^","--<","-.>",":+","--x","-.1",":2","--3","-.4",":8","--p","-.P",":*","--h","-.H",":X","--D","-.d"]
linestyle = ["--","-.",":","--","-.",":","--","-.",":","--3","-.",":","--","-.",":","--","-.",":","--","-."]
markerssizes = [6,5,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
marker_color = ['g', 'r', 'm', 'k', 'y', 'c', 'g', 'r', 'm', 'k', 'y', 'c']

# linestyles: 'solid', 'dashed', 'dashdotted', 'densely dotted', 'dashdotdotted', 'densely dashed', 'densely dashdotted', 'densely dashdotdotted', 'dotted', 'loosely dashed', 'loosely dashdotted', 'loosely dashdotdotted')

linestyles = [(0, (5, 5)), (0, (3, 5, 1, 5)), (0, (1, 1)), (0, (3, 5, 1, 5, 1, 5)), (0, (5, 1)), (0, (3, 1, 1, 1)), (0, (3, 1, 1, 1, 1, 1)), (0, (1, 5)), (0, (5, 10)), (0, (3, 10, 1, 10)), (0, (3, 10, 1, 10, 1, 10))]

# Plot computational results
for n in range(N):

    # Calculate the average value in the bin
    avg_x = 0.5*(data_x[n][1:] + data_x[n][:-1])
    avg_y = data_y[n][1:]/(data_x[n][1:]-data_x[n][:-1])
    avg_error = data_rel_error[n][1:]*avg_y

    # Plot the results
    plt2 = plt.errorbar(avg_x, avg_y, yerr=avg_error, linestyle='--', dashes=linestyles[n][1], label=names[n], color=marker_color[n], errorevery=b )

pylab.legend(loc='best')

if user_args.c:
    # The C/R subplot (with shared x-axis)
    ax1 = plt.subplot(gs[1], sharex = ax0)
    plt.xlabel(labels[0], size=14)
    plt.ylabel('C/R', size=14)

    # Got through files
    for n in range(N):
        # Calculate the average value in the bin
        avg_x = 0.5*(data_x[n][1:] + data_x[n][:-1])
        avg_y = data_y[n][1:]/(data_x[n][1:]-data_x[n][:-1])
        avg_error = data_rel_error[n][1:]*avg_y

        # Calculate the C/R value
        y = avg_y[:]/mcnp_avg_y[:]
        # Calculate the propagated uncertainty
        prop_uncert = np.sqrt( ((1.0/mcnp_avg_y[:])**2)*(avg_error[:])**2 + ((avg_y[:]/mcnp_avg_y[:]**2)**2)*(mcnp_avg_error[:])**2 )

        # Print C/R results
        print '\n',names[n], ' C/R:\n--------------------------------------------------------'
        max_diff = 0.0
        diff_energy = 0.0
        diff_error = 0.0
        for k in range(len(avg_x)):
          diff = np.abs(1.0-y[k])*100
          if diff > max_diff:
            max_diff = diff
            diff_energy = avg_x[k]
            diff_error = prop_uncert[k]*100.0
          print avg_x[k], ": ",diff, u"\u00B1", prop_uncert[k]*100.0, "%"
        print '--------------------------------------------------------'
        print "Maximum percent relative difference at ", diff_energy, ": ", max_diff, u"\u00B1", diff_error, "%"

        ax1.errorbar(avg_x, y, yerr=prop_uncert, linestyle='--', dashes=linestyles[n][1], label=names[n], color=marker_color[n] )


    plt.xlim(xmin,xmax)
    plt.ylim(0.9,1.1)

    # make x ticks for first suplot invisible
    plt.setp(ax0.get_xticklabels(), visible=False)

    # remove first tick label for the first subplot
    yticks = ax0.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    ax0.grid(linestyle=':')
    ax1.grid(linestyle=':')

    # remove vertical gap between subplots
    plt.subplots_adjust(hspace=.0)

output = "energy_bin_results.pdf"
if user_args.o:
    output = user_args.o

print "Plot outputted to: ",output
# fig.savefig(output, bbox_inches='tight', dpi=600)
plt.show()