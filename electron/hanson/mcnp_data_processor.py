#! /usr/bin/env python
import datetime
import os
import shutil
import sys, getopt
from subprocess import call
import math

def main(argv):
    directory = ''
    try:
        opts, args = getopt.getopt(argv,"hf:",["filename="])
    except getopt.GetoptError:
        print 'data_processor.py -f <filename>'
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print 'data_processor.py -f <filename>'
            sys.exit(1)
        elif opt in ("-f", "--filename"):
            filename = arg

    cell_list = ['10']
    surface_list = ['101']
    angle_list = ['', 'full' ]

    # Get the directory of the mcnp file
    directory = os.path.dirname(filename)
    base = directory + '/' + os.path.basename(filename).split('.')[0]

    # Check if file exists
    if os.path.isfile(filename):

        today = datetime.date.today()
        # # Read the mcnp data file for surface tallies
        # with open(filename) as data:
        #     # go through all surface tallies
        #     for i in cell_list:
        #         start=" cell  "+i
        #         name = base+"_cell_flux.txt"
        #         file = open(name, 'w')
        #         header = "# Energy   flux \t   Sigma\t"+str(today)+"\n"
        #         file.write(header)
        #         # Skips text before the beginning of the interesting block:
        #         for line in data:
        #             if line.startswith(start):
        #                 data.next()
        #                 break
        #         # Reads text until the end of the block:
        #         for line in data:  # This keeps reading the file
        #             if line.startswith('      total'):
        #                 file.close()
        #                 break
        #             line = line.lstrip()
        #             line = line.replace('   ',' ')
        #             file.write(line)

        degree = math.pi/180.0
        square_degree = degree*degree
        cosines = [ -1.00000000000000E+00, 0.00000000000000E+00, 8.48048096156426E-01, 8.82126866017668E-01, 9.13332365617192E-01, 9.38191335922484E-01, 9.51433341895538E-01, 9.60585317886711E-01, 9.68669911264357E-01, 9.74526872786577E-01, 9.78652704312051E-01, 9.82024659632372E-01, 9.85229115235059E-01, 9.88520271746353E-01, 9.91146155097021E-01, 9.92986158373646E-01, 9.95072889372028E-01, 9.96419457128586E-01, 9.97012445565730E-01, 9.97743253476273E-01, 9.98187693254492E-01, 9.98555486558339E-01, 9.98823128276774E-01, 9.99166134342540E-01, 9.99378583910478E-01, 9.99701489781183E-01, 9.99853726281158E-01, 9.99958816007535E-01, 1.00000000000000E+00 ]
        # Finer cosine bins for CH
        # cosines = [ -1.00000000000000E+00, 9.91894442590030E-01, 9.92331937885489E-01, 9.93611310520008E-01, 9.93999199399457E-01, 9.96041065410770E-01, 9.96345296190906E-01, 9.96492859249504E-01, 9.96778878456247E-01, 9.97288851511543E-01, 9.97440782930944E-01, 9.98015754214463E-01, 9.98166626538801E-01, 9.98421217972777E-01, 9.98536670326212E-01, 9.98611205219883E-01, 9.98736956606018E-01, 9.98954674260241E-01, 9.99048221581858E-01, 9.99289472640589E-01, 9.99341123963171E-01, 9.99414947916632E-01, 9.99461728392073E-01, 9.99777013105531E-01, 9.99805523312194E-01, 9.99907336812014E-01, 9.99921044203816E-01, 9.99987190864844E-01, 9.99991942880066E-01, 1.00000000000000E+00 ]

        current = [None] * (len(cosines) -1)
        rel_error = [None] * (len(cosines) -1)

        with open(filename) as data:
            # go through all surface tallies
            for i in surface_list:
                start=" surface  "+i

                # go through the current estimators first angle
                # Skips text before the beginning of the interesting block:
                i = 0
                for line in data:
                    if line.startswith(start):
                        data.next()
                        current[i], rel_error[i] = data.next().strip().split(' ')
                        i+=1
                        if i == len(cosines):
                            break

        # Convert to #/Square Degree
        size = len(cosines)-1
        num_square_degree = [None] * size
        num_square_degree_rel_error = [None] * size
        angles = [None] * size

        for i in range(0, size):
          j = size-i
          k = j-1
          angles[i] = math.acos(float(cosines[k]))/degree
          cosine_diff = float(cosines[j]) - float(cosines[k])
          sterradians = 2.0*math.pi*cosine_diff
          num_per_ster = float(current[j-1])/sterradians
          num_square_degree[i] = num_per_ster*square_degree
          num_square_degree_rel_error[i] = float(rel_error[j-1])

        # Write title to file
        new_name = base+"_spectrum.txt"
        out_file = open(new_name, 'w')
        out_file.write( "# MCNP6.2\n")
        # Write data header to file
        header = "# Angle (degree)\tTransmission (Frac/Deg2)\tError\t"+str(today)+"\n"
        out_file.write(header)

        # Write data to file
        for i in range(0, size):
            output = '%.4e' % angles[i] + "\t" + \
                    '%.16e' % num_square_degree[i] + "\t" + \
                    '%.16e' % num_square_degree_rel_error[i] + "\n"
            out_file.write( output )

    else:
        print "File ",filename," does not exist!"

if __name__ == "__main__":
   main(sys.argv[1:])
