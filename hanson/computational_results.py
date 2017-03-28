#! /usr/bin/env python
import csv
import math
import argparse as ap

# Set up the argument parser
description = "This script takes #/square degree data from MCNP, Native-ACE, "\
              "Native-LinLog and Native-LinLin runs and combines them."

parser = ap.ArgumentParser(description=description)

mcnp_msg = "MCNP #/square degree data .txt file"
parser.add_argument('-m', help=mcnp_msg, required=True)

ace_msg = "Native-ACE #/square degree data .txt file"
parser.add_argument('-a', help=ace_msg, required=True)

log_msg = "Native-LinLog #/square degree data .txt file"
parser.add_argument('-l', help=log_msg, required=True)

lin_msg = "Native-LinLin #/square degree data .txt file"
parser.add_argument('-f', help=lin_msg, required=True)

# Parse the user's arguments
user_args = parser.parse_args()

# Get MCNP data
with open(user_args.m) as input:
    data = zip(*(line.strip().split(' ') for line in input))
    name = data[0][0] + data[1][0] + data[2][0]
    mcnp_angles = data[0][1:]
    mcnp_result = data[1][1:]
    mcnp_error = data[2][1:]

# Get Native-ACE data
with open(user_args.a) as input:
    data = zip(*(line.strip().split(' ') for line in input))
    name = data[0][0] + data[1][0] + data[2][0]
    ace_angles = data[0][1:]
    ace_result = data[1][1:]
    ace_error = data[2][1:]

# Get Native-LinLog data
with open(user_args.l) as input:
    data = zip(*(line.strip().split(' ') for line in input))
    name = data[0][0] + data[1][0] + data[2][0]
    log_angles = data[0][1:]
    log_result = data[1][1:]
    log_error = data[2][1:]

# Get Native-LinLin data
with open(user_args.f) as input:
    data = zip(*(line.strip().split(' ') for line in input))
    name = data[0][0] + data[1][0] + data[2][0]
    lin_angles = data[0][1:]
    lin_result = data[1][1:]
    lin_error = data[2][1:]


# Make sure the data is all the same size
if mcnp_angles == ace_angles == log_angles == lin_angles:

    out_file = open("computational_results.txt", "w")
    out_file.write("# MCNP\tACE\tLinLin\tLinLog\n")
    out_file.write("# Angle (degrees)\t#/square degree\tError\n")

    for i in range(0, len(mcnp_angles)):
        output = '%.3e'% float(mcnp_angles[i]) + " " + \
                 '%.6e' % float(mcnp_result[i]) + " " + \
                 '%.6e' % float(mcnp_error[i]) + " " + \
                 '%.10e' % float(ace_result[i]) + " " + \
                 '%.10e' % float(ace_error[i]) + " " + \
                 '%.10e' % float(lin_result[i]) + " " + \
                 '%.10e' % float(lin_error[i]) + " " + \
                 '%.10e' % float(log_result[i]) + " " + \
                 '%.10e' % float(log_error[i]) + "\n"
        out_file.write( output )
    out_file.close()

else:
    print "Error: data in files does not match!"
