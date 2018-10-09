#! /usr/bin/env python
# Luke Kersting
# This script asks for transmission (Frac/Deg2) data and run names which it then plots.
import numpy as np
from numpy import exp, linspace
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter
import argparse as ap
import inspect, os
from lmfit import Model

def gaussian(x, amp, wid):
  return amp * exp(-x*x /(wid*wid) )

# Set up the argument parser
description = "This script asks for transmission (Frac/Deg2) data and run names which "\
              "which it then fits and plots."

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
M = 14
data_x = [[] for y in range(N)]
data_y = [[] for y in range(N)]
data_error = [[] for y in range(N)]
names = [0 for x in range(N)]

# Get computational results
for n in range(N):

    with open(file_paths[n]) as input:
        names[n] = input.readline().strip()[1:]
        print names[n]
        input.readline().strip()[1:]
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

plots = []
labels = []
if user_args.e:
    # Get experimental data
    directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = directory + "/experimental_results.tsv"
    with open(filename) as input:
        data = zip(*(line.strip().split('\t') for line in input))
        exp_x = np.asfarray(data[0][1:14])
        exp_y = np.asfarray(data[1][1:14])

    # Plot the experimental data
    pl1, =plt.plot(exp_x, exp_y, linestyle='None', marker='s', markersize=5 )

    # Plot a least squares fit
    gmodel = Model(gaussian)
    result = gmodel.fit(exp_y, x=exp_x, amp=0.0441, wid=2.58)
    x = linspace(0, exp_x[len(exp_x)-1])
    y = result.eval(x=x)
    pl2, = plt.plot(x, y, 'b--' )

    # Plot the Gaussian fit given by Hanson
    y = [None] * len(x)
    for i in range(len(y)):
      y[i] = gaussian(x[i], 0.0441, 2.58)
    pl3, = plt.plot(x, y, color='b' )
    plots = [(pl1,pl3),(pl2)]
    labels = ["Hanson (Exp.)","Least Square Fit (Hanson)" ]

markers = ["v","o","^","<",">","+","x","1","2","3","4","8","p","P","*","h","H","X","D","d"]
linestyle = ["--","-.",":","--","-.",":","--","-.",":","--3","-.",":","--","-.",":","--","-.",":","--","-."]
markerssizes = [6,5,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
marker_color = ['g', 'r', 'k', 'm', 'y', 'c', 'w', 'g', 'r', 'k', 'm', 'y', 'c', 'w']
# names = ['MCNP6.2','FRENSIE-ACE', 'FRENSIE-ENDL' ]
for n in range(N):
    # Insert first bin lower bounds as an angle of 0
    x = np.insert( data_x[n], 0, 0.0)

    # Calculate bin mid points
    mid = 0.5*(x[1:] + x[:-1])

    # Plot the data at the midpoints
    plt1 = plt.errorbar(mid, data_y[n], yerr=data_error[n], fmt=markers[n], markersize=markerssizes[n], color=marker_color[n] )

    # Plot a least squares fit
    gmodel = Model(gaussian)
    result = gmodel.fit(data_y[n], x=mid, amp=0.0441, wid=2.58)
    x = linspace(0, mid[len(mid)-1], num=100)
    y = result.eval(x=x)
    plt2, = plt.plot(x, y, color=marker_color[n], linestyle=linestyle[n] )
    plots.append( (plt1[0],plt2) )
    labels.append(names[n])

plt.legend(plots, labels, loc=1)
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