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

mcnp_msg = "The MCNP energy bin data file."
parser.add_argument('-m1', help=mcnp_msg)

mcnp_msg = "The MCNP energy bin data file."
parser.add_argument('-m2', help=mcnp_msg)

mcnp_msg = "The MCNP energy bin data file."
parser.add_argument('-m3', help=mcnp_msg)

output_msg = "The output file name."
parser.add_argument('-o', help=output_msg, required=False)

parser.add_argument("input_files", nargs='*')

# Plot every bth error bar
b = 3
# Set the x max and min for the main plot
xmaxes = [0.0072, 0.0072, 0.01]
xmax = 0.01
xmin = 0.0
# Set the y maxes and mins for the main plot
ymaxes = [350.0, 3e5, 9e5]
ymins = [0.0, 1e3, 1e4]

scales = ['linear', 'log', 'log']

# Parse the user's arguments
user_args = parser.parse_args()
file_paths = user_args.input_files

# Number of files
N = len(file_paths)

# Number of data points in each file
data_x = [[] for y in range(N)]
data_y = [[] for y in range(N)]
data_rel_error = [[] for y in range(N)]
mcnp_x = [[] for y in range(N)]
mcnp_y = [[] for y in range(N)]
mcnp_rel_error = [[] for y in range(N)]
labels = [0 for x in range(N)]
names = [0 for x in range(N)]

mcnp_avg_x = [[] for y in range(N)]
mcnp_avg_y = [[] for y in range(N)]
mcnp_avg_error = [[] for y in range(N)]

avg_x = [[] for y in range(N)]
avg_y = [[] for y in range(N)]
avg_error = [[] for y in range(N)]

nmax = [0 for x in range(N)]

# Get computational results
for n in range(N):
  with open(file_paths[n]) as input:
    # Read name of data
    names[n] = input.readline()[1:].strip()
    # Read the data header
    input.readline()[1:].strip()
    # Read the data
    data = zip(*(line.strip().split('\t') for line in input))
    # get bins within max energy
    for i in range(1,len(data[0])):
      if float(data[0][i]) <= xmaxes[n]+1e-5:
        nmax[n] = i

    data_x[n] = np.asfarray(data[0][:nmax[n]])
    data_y[n] = np.asfarray(data[1][:nmax[n]])
    data_rel_error[n] = np.asfarray(data[2][:nmax[n]])

  # Calculate the average value in the bin
  avg_x[n] = 0.5*(data_x[n][1:] + data_x[n][:-1])
  avg_y[n] = data_y[n][1:]/(data_x[n][1:]-data_x[n][:-1])
  avg_error[n] = data_rel_error[n][1:]*avg_y[n]

# Get MCNP results
mcnp_files = [user_args.m1,user_args.m2,user_args.m3]
for n in range(N):
  if os.path.isfile(mcnp_files[n]):
    with open(mcnp_files[n]) as input:
        # Read name of data
        mcnp_name = input.readline()[1:].strip()
        # Read the data header
        labels[n] = input.readline()[1:].strip().split('\t')
        # Read the data
        data = zip(*(line.strip().split('\t') for line in input))
        mcnp_x[n] = np.asfarray(data[0][:nmax[n]])
        mcnp_y[n] = np.asfarray(data[1][:nmax[n]])
        mcnp_rel_error[n] = np.asfarray(data[2][:nmax[n]])

  for x in range(len(data_x[n])):
    diff = mcnp_x[n][x] - data_x[n][x]
    if diff > 0.0:
      print mcnp_x[n][x], " diff = ", mcnp_x[n][x] - data_x[n][x]

  # Calculate the average value in the bin
  mcnp_avg_x[n] = 0.5*(mcnp_x[n][1:] + mcnp_x[n][:-1])
  mcnp_avg_y[n] = mcnp_y[n][1:]/(mcnp_x[n][1:]-mcnp_x[n][:-1])
  mcnp_avg_error[n] = mcnp_rel_error[n][1:]*mcnp_avg_y[n]

gs = [[] for y in range(N)]
axes = [[] for y in range(2*N)]

fig = plt.figure(num=1, figsize=(10,12))

for i in range(N):
  # We'll use two separate gridspecs to have different margins, hspace, etc
  top = 0.95 -i/100.0
  bottom = 0.1 -i/100.0
  gs[i] = gridspec.GridSpec(6, 1, height_ratios=[2, 1, 2, 1, 2, 1], top=top, bottom=bottom, hspace=0)

y_labels = [labels[0][1], 'C/R', labels[1][1], 'C/R', labels[2][1], 'C/R']

# Set the first plot
axes[0] = fig.add_subplot(gs[0][0,:])
axes[0].set_ylabel(y_labels[0], size=14)
axes[0].set_title('Results for a 0.01 MeV Point Source in a H Sphere', size=16)

for i in range(1,len(axes)):
  j = i/2
  print j
  # Shared axes with C/R
  axes[i] = fig.add_subplot(gs[j][i,:], sharex=axes[i-1])
  # Hide shared x-tick labels
  plt.setp(axes[i-1].get_xticklabels(), visible=False)
  # Set the y labels
  axes[i].set_ylabel(y_labels[i], size=14)


# Set the x label
x_label = labels[0][0]
axes[5].set_xlabel(x_label, size=14)

ax=plt.gca()


# Plot the MCNP data
for n in range(N):
  j = n*2
  axes[j].errorbar(mcnp_avg_x[n], mcnp_avg_y[n], yerr=mcnp_avg_error[n], linestyle='-', label=mcnp_name, errorevery=b )


# linestyles: 'solid', 'dashed', 'dashdotted', 'densely dotted', 'dashdotdotted', 'densely dashed', 'densely dashdotted', 'densely dashdotdotted', 'dotted', 'loosely dashed', 'loosely dashdotted', 'loosely dashdotdotted')
linestyles = [(0, (5, 5)), (0, (3, 5, 1, 5)), (0, (1, 1)), (0, (3, 5, 1, 5, 1, 5)), (0, (5, 1)), (0, (3, 1, 1, 1)), (0, (3, 1, 1, 1, 1, 1)), (0, (1, 5)), (0, (5, 10)), (0, (3, 10, 1, 10)), (0, (3, 10, 1, 10, 1, 10))]

markers = ["--v","-.o",":^","--<","-.>",":+","--x","-.1",":2","--3","-.4",":8","--p","-.P",":*","--h","-.H",":X","--D","-.d"]
linestyle = ["--","-.",":","--","-.",":","--","-.",":","--3","-.",":","--","-.",":","--","-.",":","--","-."]
markerssizes = [6,5,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
marker_color = ['g', 'r', 'm', 'k', 'y', 'c', 'g', 'r', 'm', 'k', 'y', 'c']

# Plot the Computational data
for n in range(N):
  j = n*2
  axes[j].errorbar(avg_x[n], avg_y[n], yerr=avg_error[n], linestyle='--', dashes=linestyles[n][1], label=names[n], color=marker_color[n], errorevery=b )

  axes[j].set_ylim(ymins[n],ymaxes[n])
  # Set the y scale
  axes[j].set_yscale(scales[n])

pylab.legend(loc='best')


# The C/R subplots (with shared x-axis)

# Got through files
for n in range(N):
    # Calculate the C/R value
    y = avg_y[n][:]/mcnp_avg_y[n][:]
    # Calculate the propagated uncertainty
    prop_uncert = np.sqrt( ((1.0/mcnp_avg_y[n][:])**2)*(avg_error[n][:])**2 + ((avg_y[n][:]/mcnp_avg_y[n][:]**2)**2)*(mcnp_avg_error[n][:])**2 )

    # Print C/R results
    print '\n',names[n], ' C/R:\n--------------------------------------------------------'
    max_diff = 0.0
    diff_energy = 0.0
    diff_error = 0.0
    for k in range(len(avg_x[n])):
      diff = (1.0-y[k])*100.0
      print avg_x[n][k], ": ",diff, u"\u00B1", prop_uncert[k]*100.0, "%"
      if abs(diff) > abs(max_diff) and avg_x[n][k] < 0.0075:
        max_diff = diff
        diff_energy = avg_x[n][k]
        diff_error = prop_uncert[k]*100.0
    print '--------------------------------------------------------'
    print "Maximum percent relative difference at ", diff_energy, ": ", max_diff, u"\u00B1", diff_error, "%"

    j = n*2+1
    axes[j].errorbar(avg_x[n], y, yerr=prop_uncert, linestyle='--', dashes=linestyles[n][1], label=names[n], color=marker_color[n] )
    axes[j].set_ylim(0.96,1.06)

plt.xlim(xmin,xmax)

# remove first y tick label for the first subplots
yticks = axes[0].yaxis.get_major_ticks()
yticks[0].label1.set_visible(False)

yticks = axes[2].yaxis.get_major_ticks()
yticks[1].label1.set_visible(False)
yticks[2].label1.set_visible(False)

yticks = axes[4].yaxis.get_major_ticks()
yticks[1].label1.set_visible(False)

# Add grid to plots
for n in range(len(axes)):
  axes[n].grid(linestyle=':')

output = "energy_bin_results.pdf"
if user_args.o:
    output = user_args.o

print "Plot outputted to: ",output
# fig.savefig(output, bbox_inches='tight', dpi=600)
plt.show()