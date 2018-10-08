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

    mcnp_surface_list = ['10', '11', '12', '13', '14' ]
    facemc_surface_list = ['12', '9', '6', '3', '1' ]

    energy = input("Enter the energy to process in keV (1, 10, 100): ")

    name = "/"+str(energy)+"kev_current_"
    for i in range(0, len(mcnp_surface_list)):
        # Get the file names
        mcnpinputfile = mcnpinputdir+name+str(mcnp_surface_list[i])+".txt"
        facemcinputfile = facemcinputdir+name+str(facemc_surface_list[i])+".txt"
        outputfile = outputdir+name+str(i+1)+".txt"

        # Run the data combiner to get the c/e results
        command = "./data_combiner.py -m "+mcnpinputfile+" -f "+facemcinputfile+" -o "+outputfile
        os.system( command )

if __name__ == "__main__":
    main(sys.argv[1:])
