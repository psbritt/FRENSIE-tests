#! /usr/bin/env python
# Luke Kersting
# This script asks for albedo data and run names which it then plots.
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import argparse as ap
import inspect, os

# Set up the argument parser
description = "This script asks for albedo data and run names which "\
              "which it then plots against the experimental data from CREEP paper."

parser = ap.ArgumentParser(description=description)


experimental_msg = "Flag to add CREEP experimental data to the generated plot."
parser.add_argument('-e', help=experimental_msg, action='store_true')

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

fig = plt.figure(num=1, figsize=(10,7))
plt.xlabel('Energy (MeV)', size=14)
plt.ylabel('Reflection Coef.', size=14)
plt.title('Electron Albedos for an infinite slab of Al', size=16)
plt.xscale('log')
ax=plt.gca()

plt.xlim(9e-5,.120)
#plt.ylim(0.12,0.19)

if user_args.e:
    # Get experimental data
    data = np.loadtxt("./creep_experimental.txt", skiprows=2)
    plt.scatter(data[:,0], data[:,1], label="CREEP", marker='s' )

markers = ["o","*","v","^","<",">","+","x","1","2","3","4","8","p","*","h","H","X","D","d"]
if user_args.a:
  exp_names = ['assad','bishop', 'bongeler', 'bronstein', 'cosslett', 'drescher', 'heinrich', 'kanter', 'neubert', 'palluel', 'philibert', 'reimer', 'shimizu', 'wittry' ]
  exp_names = ['assad','bishop', 'bronstein', 'drescher', 'heinrich', 'neubert', 'shimizu' ]
  # exp_names = ['assad','bishop', 'bronstein', 'drescher', 'neubert' ]

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
  # ax.set_xscale('log')


# markers = ["v","^","<",">","s","+","x","1","2","3","4","8","p","*","h","H","X","D","d"]
# markerssizes = [7,7,7,7,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
# marker_color = ['g', 'r', 'c', 'm', 'y', 'k', 'w', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
markers = ["s","<","x","+","8","p","*","h","H","X","D","d"]
markerssizes = [8,8,8,8,5,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]
marker_color = ['y', 'c', 'g', 'r', 'm', 'k', 'w', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
for n in range(N):
    x = map(float, data_x[n])
    y = map(float, data_y[n])
    yerr = map(float, data_error[n])
    plt.errorbar(x, y, yerr=yerr, label=names[n], fmt=markers[n], markersize=markerssizes[n], color=marker_color[n] )
plt.legend(loc=1)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#ax.xaxis.set_major_formatter(FormatStrFormatter('%.4f'))
# plt.ylim(0.12,0.22)
# leg = plt.legend(loc='best', ncol=2)
# leg.get_frame().set_alpha(0.5)

output = "albedo_results.pdf"
if user_args.o:
    output = user_args.o

print "Plot outputted to: ",output
fig.savefig(output, bbox_inches='tight', dpi=300)
plt.show()