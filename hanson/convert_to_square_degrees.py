#! /usr/bin/env python
import csv
import math
import argparse as ap

# Set up the argument parser
description = "This script takes angular binned surface current data and "\
              "return the data in #/square degree units."

parser = ap.ArgumentParser(description=description)

file_msg = "the angular binned surface current .txt file"
parser.add_argument('-f', help=file_msg, required=True)

output_msg = "the desired output file name"
parser.add_argument('-o', help=output_msg, required=False)

# Parse the user's arguments
user_args = parser.parse_args()

file_name = user_args.f
output_name = file_name[:-4] +"_spectrum.txt"
if user_args.o:
    output_name = user_args.o
print "Output file: ",output_name

degree = math.pi/180.0
square_degree = degree*degree

with open(user_args.f) as input:
    data = zip(*(line.strip().split(' ') for line in input))
    name = data[0][0] + data[1][0] + data[2][0]
    angle_cosine = data[0][1:]
    current = data[1][1:]
    error = data[2][1:]

size = len(angle_cosine)-1
num_square_degree = [None] * size
num_square_degree_error = [None] * size
avg_angle = [None] * size

for i in range(0, size):
    j = size-i
    k = j-1
    angle_diff = math.acos(float(angle_cosine[j]))/degree + math.acos(float(angle_cosine[k]))/degree
    avg_angle[i] = angle_diff/2.0
    cosine_diff = float(angle_cosine[j]) - float(angle_cosine[k])
    sterradians = 2.0*math.pi*cosine_diff
    num_per_ster = float(current[j])/sterradians
    num_square_degree[i] = num_per_ster*square_degree
    num_square_degree_error[i] = float(error[j])/sterradians*square_degree

out_file = open(output_name, "w")
out_file.write("# Degrees\t#/Square Degree\t\tError\n")
for i in range(0, size):
    output = '%.4e' % avg_angle[i] + " " + \
             '%.16e' % num_square_degree[i] + " " + \
             '%.16e' % num_square_degree_error[i] + "\n"
    out_file.write( output )

out_file.close()

