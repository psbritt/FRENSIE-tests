#! /usr/bin/env python
import datetime
import os
import shutil
import sys, getopt
from subprocess import call

def main(argv):
    filename = ''
    try:
        opts, args = getopt.getopt(argv,"hf:r:",["file=","range="])
    except getopt.GetoptError:
        print 'mcnp_data_processor.py -f <file> -r <range>'
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print 'mcnp_data_processor.py -f <file> -r <range>'
            sys.exit(1)
        elif opt in ("-f", "--file"):
            filename = arg
        elif opt in ("-r", "--range"):
            dose_depth = arg

    cell_list = ['10']

    # Get mcnp output file name
    base = filename[:-2]

    # Check if file exists
    if os.path.isfile(filename):

        today = datetime.date.today()
        # Read the mcnp data file for surface tallies
        with open(filename) as data:
            # go through all surface tallies
            for i in cell_list:
                start=" cell  "+i
                name = base+"_energy_dep.txt"
                file = open(name, 'w')
                header = "# Range (g/cm2)\tEnergy Deposition\tError\t"+str(today)+"\n"
                file.write(header)
                # Skips text before the beginning of the interesting block:
                for line in data:
                    if line.startswith(start):
                        break
                # Reads next line:
                line  = data.next()
                line = line.lstrip()
                line = line.replace('                 ','\t')
                line = line.replace(' ','\t')
                data = dose_depth + "\t" + line
                file.write(data)
                file.close()

    else:
        print "File ",filename," does not exist!"

if __name__ == "__main__":
   main(sys.argv[1:])
