#! /usr/bin/env python
# Luke Kersting
# This script asks for #/square degree data and run names which it then plots.
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter
import argparse as ap
import inspect, os

# Set up the argument parser
description = "This script asks for #/square degree data and run names which "\
              "which it then plots."

parser = ap.ArgumentParser(description=description)

experimental_msg = "Flag to add the experimental data to the generated plot."
parser.add_argument('-e', help=experimental_msg, action='store_true')

mcnp_comparison_msg = "Flag to compare against mcnp data run."
parser.add_argument('-m', help=mcnp_comparison_msg, action='store_true')

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
data_x = [[0 for x in range(N)] for y in range(M)]
data_y = [[0 for x in range(N)] for y in range(M)]
data_error = [[0 for x in range(N)] for y in range(M)]
names = [0 for x in range(N)]

# Get computational results
for n in range(N):

    with open(file_paths[n]) as input:
        names[n] = input.readline().strip()[1:]
        print names[n]
        print input.readline().strip()[1:]
        data = zip(*(line.strip().split('\t') for line in input))
        data_x[n][:] = data[0][:]
        data_y[n][:] = data[1][:]
        data_error[n][:] = data[2][:]

# Plot
# fig = plt.figure(num=1, figsize=(9,9))
fig = plt.figure(num=1, figsize=(9,7))

# set height ratios for sublots
# gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
gs = gridspec.GridSpec(1, 1)

# the first subplot
ax0 = plt.subplot(gs[0])

x_label = 'Angle (Degree)'
plt.xlabel(x_label, size=14)
plt.ylabel('#/Square Degrees', size=14)
plt.title('$\mathrm{15.7\/MeV\/Electron\/Angular\/Distribution\/from\/a\/9.658\/\mu m\/Gold\/Foil}$', size=16)
ax=plt.gca()

plt.xlim(0.0,7.0)
plt.ylim(0.0,0.05)
if user_args.m:
    plt.ylim(0.0,0.04)

if user_args.e:
    # Get experimental data
    directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = directory + "/experimental_results.tsv"
    with open(filename) as input:
        data = zip(*(line.strip().split('\t') for line in input))
        exp_x = data[0][1:]
        exp_y = data[1][1:]
        # exp_error = data[2][1:]

    x = map(float, exp_x)
    y = map(float, exp_y)

    # yerr = map(float, exp_error)
    # plt.errorbar(x, y, yerr=yerr, label="Hanson (Exp.)", fmt="s", markersize=5 )
    plt.plot(x, y, label="Hanson (Exp.)", marker='s', markersize=5 )


markers = ["--v","-.o",":^","--<","-.>",":+","--x","-.1",":2","--3","-.4",":8","--p","-.P",":*","--h","-.H",":X","--D","-.d"]
markerssizes = [6,5,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
marker_color = ['g', 'r', 'm', 'k', 'y', 'c', 'g', 'r', 'm', 'k', 'y', 'c']

# linestyles: 'solid', 'dashed', 'dashdotted', 'densely dotted', 'dashdotdotted', 'densely dashed', 'densely dashdotted', 'densely dashdotdotted', 'dotted', 'loosely dashed', 'loosely dashdotted', 'loosely dashdotdotted')

linestyles = [(0, ()), (0, (5, 5)), (0, (3, 5, 1, 5)), (0, (1, 1)), (0, (3, 5, 1, 5, 1, 5)), (0, (5, 1)), (0, (3, 1, 1, 1)), (0, (3, 1, 1, 1, 1, 1)), (0, (1, 5)), (0, (5, 10)), (0, (3, 10, 1, 10)), (0, (3, 10, 1, 10, 1, 10))]

if user_args.m:
    names = ['MCNP6.2','FACEMC-ACE', 'FACEMC-ENDL' ]
# names = ['MCNP6.2','FACEMC-ACE', 'FACEMC-ENDL' ]
for n in range(N):
    x = map(float, data_x[n])
    y = map(float, data_y[n])
    yerr = map(float, data_error[n])

    # Insert first bin lower bounds as an angle of 0
    x.insert(0,0.0)

    # Plot histogram of results
    m, bins, _ = plt.hist(x[:-1], bins=x, weights=y, histtype='step', label=names[n], color=marker_color[n], linestyle=linestyles[n], linewidth=1.8 )
    # Plot error bars
    mid = 0.5*(bins[1:] + bins[:-1])
    plt.errorbar(mid, m, yerr=yerr, ecolor=marker_color[n], fmt=None)

plt.legend(loc=1)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
if user_args.m:
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

markers = ["v","o","^","<",">","+","x","1","2","3","4","8","p","P","*","h","H","X","D","d"]
if user_args.e:
  empty = True

#     # The C/E subplot (with shared x-axis)
#     ax1 = plt.subplot(gs[1], sharex = ax0)
#     plt.xlabel(x_label, size=14)
#     plt.ylabel('C/E', size=14)

#     # Get experimental data
#     directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#     filename = directory + "/experimental_results.tsv"
#     with open(filename) as input:
#         data = zip(*(line.strip().split('\t') for line in input))
#         exp_x = data[0][1:]
#         exp_y = data[1][1:]

#     # Calculate the experimental from the % error
#     experimental_x = map(float, exp_x)
#     experimental_y = map(float, exp_y)

#     for n in range(N):
#         x = map(float, data_x[n][:-2])
#         y = map(float, data_y[n][:-2])
#         yerr = map(float, data_error[n][:-2])

#         # Insert first bin lower bounds as an angle of 0
#         x.insert(0,0.0)

#         for i in range(0, len(y)):
#           # print "y: ", y[i], "\ty_exp: ", experimental_y[i]
#           y[i] = y[i]/experimental_y[i]
#           yerr[i] = yerr[i]/experimental_y[i]
#           print i, ": ", (1.0-y[i])*100, "%"

#         # Plot histogram of results
#         m, bins, _ = ax1.hist(x[:-1], bins=x, weights=y, histtype='step', label=names[n], color=marker_color[n], linestyle=linestyles[n], linewidth=1.8 )
#         # Plot error bars
#         mid = 0.5*(bins[1:] + bins[:-1])
#         ax1.errorbar(mid, m, yerr=yerr, ecolor=marker_color[n], fmt=None)

#         # for i in range(0, len(y)):
#         #   print i, ": ", (experimental_x[i]-mid[i])/experimental_x[i], "relative diff in x"

#         # ax1.errorbar(mid, y, yerr=yerr, label=names[n], fmt=markers[n], markersize=markerssizes[n], color=marker_color[n])

#     # make x ticks for first suplot invisible
#     plt.setp(ax0.get_xticklabels(), visible=False)

#     # remove first tick label for the first subplot
#     yticks = ax0.yaxis.get_major_ticks()
#     yticks[0].label1.set_visible(False)
#     ax0.grid(linestyle=':')
#     ax1.grid(linestyle=':')

#     plt.xlim(0.0,6.78)
#     plt.ylim(0.8,1.3)
#     # plt.ylim(0.5,1.8)
#     # plt.ylim(0.3,2.3)

#     # remove vertical gap between subplots
#     plt.subplots_adjust(hspace=.0)

elif user_args.m:

    # The C/E subplot (with shared x-axis)
    ax1 = plt.subplot(gs[1], sharex = ax0)
    plt.xlabel(x_label, size=14)
    plt.ylabel('FACEMC/MCNP', size=14)

    # Get mcnp data
    experimental_x = x = map(float, data_x[0][:-2])
    experimental_y = y = map(float, data_y[0][:-2])
    experimental_error = map(float, data_error[0][:-2])

    for n in range(1,N):
        x = map(float, data_x[n][:-2])
        y = map(float, data_y[n][:-2])
        yerr = map(float, data_error[n][:-2])

        # Insert first bin lower bounds as an angle of 0
        x.insert(0,0.0)

        for i in range(0, len(y)):
          y[i] = y[i]/experimental_y[i]
          yerr[i] = yerr[i]/experimental_y[i]
          print x[i], ": ", (1.0-y[i])*100, "%"

        # Plot histogram of results
        m, bins, _ = ax1.hist(x[:-1], bins=x, weights=y, histtype='step', label=names[n], color=marker_color[n], linestyle=linestyles[n], linewidth=1.8 )
        # Plot error bars
        mid = 0.5*(bins[1:] + bins[:-1])
        ax1.errorbar(mid, m, yerr=yerr, ecolor=marker_color[n], fmt=None)

    # make x ticks for first suplot invisible
    plt.setp(ax0.get_xticklabels(), visible=False)

    # remove first tick label for the first subplot
    yticks = ax0.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    ax0.grid(linestyle=':')
    ax1.grid(linestyle=':')

    plt.xlim(0.0,6.78)
    plt.ylim(0.96,1.04)

    # remove vertical gap between subplots
    plt.subplots_adjust(hspace=.0)

output = "hanson_results.pdf"
if user_args.o:
    output = user_args.o

print "Plot outputted to: ",output
fig.savefig(output, bbox_inches='tight', dpi=600)
plt.show()