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
        print 'data_extractor.py -m <mcnpinputdir> -f <facemcinputdir'
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print 'data_extractor.py -m <mcnpinputdir> -f <facemcinputdir'
            sys.exit(1)
        elif opt in ("-m", "--mdir"):
            mcnpinputdir = arg
        elif opt in ("-f", "--fdir"):
            facemcinputdir = arg

    # Get the file names
    name = "/current.txt"
    mcnpinputfile = mcnpinputdir+name
    facemcinputfile = facemcinputdir+name
    outputfile = outputdir+name+str(i+1)+".txt"

    # Run the data combiner to get the c/e results
    command = "./data_combiner.py -m "+mcnpinputfile+" -f "+facemcinputfile+" -o "+outputfile
    os.system( command )

if __name__ == "__main__":
    main(sys.argv[1:])
