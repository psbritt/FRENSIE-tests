#! /usr/bin/env python
import datetime
import os
import shutil
import sys, getopt
from subprocess import call

def main(argv):
    filename = ''
    try:
        opts, args = getopt.getopt(argv,"hf:",["file="])
    except getopt.GetoptError:
        print 'data_processor.py -f <file name minus .h5>'
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print 'data_processor.py -f <file name minus .h5>'
            sys.exit(1)
        elif opt in ("-f", "--file"):
            filename = arg

    cell_list = ['100']
    surface_list = ['10']
    estimator_list = ['current', 'flux' ]

    # Get mcnp output file name
    mcnp_output = filename+".o"

    # Check if file exists
    if os.path.isfile(mcnp_output):

        today = datetime.date.today()
        # Read the mcnp data file for surface tallys
        with open(mcnp_output) as data:
            # go through all surface tallies
            for i in surface_list:
                start=" surface  "+i

                # go through the current and flux estimators
                for j in estimator_list:
                    name = j+".txt"
                    file = open(name, 'w')
                    header = "# Energy   "+j+" \t   Sigma\t"+str(today)+"\n"
                    file.write(header)
                    # Skips text before the beginning of the interesting block:
                    for line in data:
                        if line.startswith(start):
                            data.next()
                            break
                    # Reads text until the end of the block:
                    for line in data:  # This keeps reading the file
                        if line.startswith('      total'):
                            file.close()
                            break
                        line = line.lstrip()
                        line = line.replace('   ',' ')
                        file.write(line)

        with open(mcnp_output) as data:
            # go through all surface tallies
            for i in cell_list:
                start=" cell  "+i

                # go track_flux estimator
                name = "track_flux.txt"
                file = open(name, 'w')
                header = "# Energy   "+"Track Flux  "+"Sigma\t"+str(today)+"\n"
                file.write(header)
                # Skips text before the beginning of the interesting block:
                for line in data:
                    if line.startswith(start):
                        data.next()
                        break
                # Reads text until the end of the block:
                for line in data:  # This keeps reading the file
                    if line.startswith('      total'):
                        file.close()
                        break
                    line = line.lstrip()
                    line = line.replace('   ',' ')
                    file.write(line)

        # Plot results
        plot = "../../../plot.p"
        call(["gnuplot", plot])

    else:
        print "File: ",mcnp_output," does not exist!"

if __name__ == "__main__":
   main(sys.argv[1:])
