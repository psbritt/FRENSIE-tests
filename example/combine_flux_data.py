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
        print 'data_extractor.py -m <mcnpinputdir> -f <facemcinputdir>'
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print 'data_extractor.py -m <mcnpinputdir> -f <facemcinputdir>'
            sys.exit(1)
        elif opt in ("-m", "--mdir"):
            mcnpinputdir = arg
        elif opt in ("-f", "--fdir"):
            facemcinputdir = arg

    # Check dir exists
    if os.path.isdir(mcnpinputdir) and os.path.isdir(facemcinputdir):

        name = "/flux.txt"
        # Get the file names
        mcnpinputfile = mcnpinputdir+name
        facemcinputfile = facemcinputdir+name
        outputfile = outputdir+name+".txt"

        # Check if files exists
        if os.path.isfile(mcnpinputfile) and os.path.isfile(facemcinputfile):

            # Check if the output directory exists and make if necessary
            if not os.path.isdir(outputdir):
                print "Making directory",outputdir
                os.makedirs(outputdir)

            # Run the data combiner to get the c/e results
            command = "./data_combiner.py -m "+mcnpinputfile+" -f "+facemcinputfile+" -o "+outputfile
            print command
            os.system( command )
        else:
            print "There is no flux data in the given directories!"
    else:
        print "One of the directories:",mcnpinputdir,facemcinputdir,"does not exist!"

if __name__ == "__main__":
    main(sys.argv[1:])
