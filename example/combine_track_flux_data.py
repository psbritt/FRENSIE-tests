#!/usr/bin/python

import sys, getopt
import math as m
import datetime
import os

def main(argv):
    today = datetime.date.today()
    mcnpinputdir = ''
    facemcinputdir = ''
    outputdir = "./results/"+str(today)
    try:
        opts, args = getopt.getopt(argv,"hm:f:",["mdir=","fdir="])
    except getopt.GetoptError:
        print 'combine_track_flux_data.py -m <mcnpinputdir> -f <facemcinputdir'
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print 'combine_track_flux_datar.py -m <mcnpinputdir> -f <facemcinputdir'
            sys.exit(1)
        elif opt in ("-m", "--mdir"):
            mcnpinputdir = arg
        elif opt in ("-f", "--fdir"):
            facemcinputdir = arg

    mcnp_cell_list = ['100', '101', '102', '103', '104' ]

    # Check dir exists
    if os.path.isdir(mcnpinputdir) and os.path.isdir(facemcinputdir):

        name = "/track_flux.txt"
        for i in range(0, len(mcnp_cell_list)):
            # Get the file names
            mcnpinputfile = mcnpinputdir+name+str(mcnp_cell_list[i])+".txt"
            facemcinputfile = facemcinputdir+name+str(i+1)+".txt"
            outputfile = outputdir+name+str(i+1)+".txt"

            # Check if files exists
            if os.path.isfile(mcnpinputfile) and os.path.isfile(facemcinputfile):

                # Check if the ouput directory exists and make if necessary
                if not os.path.isdir(outputdir):
                    print "Making directory",outputdir
                    os.makedirs(outputdir)

                # Run the data combiner to get the c/e results
                command = "./data_combiner.py -m "+mcnpinputfile+" -f "+facemcinputfile+" -o "+outputfile
                print command
                os.system( command )
            else:
                print "There is no track flux data in the given directories!"
    else:
        print "One of the directories:",mcnpinputdir,facemcinputdir,"does not exist!"

if __name__ == "__main__":
    main(sys.argv[1:])
