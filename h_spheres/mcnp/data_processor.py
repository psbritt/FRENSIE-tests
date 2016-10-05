#! /usr/bin/env python
import datetime
import os
import shutil
import sys, getopt
from subprocess import call

def main(argv):
    directory = ''
    try:
        opts, args = getopt.getopt(argv,"hd:",["out_dir="])
    except getopt.GetoptError:
        print 'data_processor.py -d <directory>'
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print 'data_processor.py -d <directory>'
            sys.exit(1)
        elif opt in ("-d", "--out_dir"):
            directory = arg

    cell_list = ['100', '101', '102', '103', '104']
    surface_list = ['10', '11', '12', '13', '14' ]
    estimator_list = ['current', 'flux' ]

    energy = input("Enter the energy to process in keV (1, 10, 100): ")

    # Get mcnp output file name
    base = "h_spheres_"+str(energy)+"kev"
    mcnp_output = base+".inpo"

    # Check if file exists
    if os.path.isfile(mcnp_output):
        # Check if the ouput directory exists and make if necessary
        if not os.path.isdir(directory):
            print "Making directory",directory
            os.makedirs(directory)

        today = datetime.date.today()
        # Read the mcnp data file for surface tallys
        with open(mcnp_output) as data:
            # go through all surface tallies
            for i in surface_list:
                start=" surface  "+i

                # go through the current and flux estimators
                for j in estimator_list:
                    name = str(directory)+str(energy)+"kev_"+j+"_"+i+".txt"
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

                # go through the current and flux estimators
                name = str(directory)+str(energy)+"kev_track_flux_"+i+".txt"
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

        date = today.strftime("%b%d")
        new_name = "../../../results/mcnp/"+str(base)+"_"+date+".inpo"
        shutil.copy(mcnp_output,new_name)
        if os.path.isfile(base+".inpm"):
            os.remove(base+".inpm")
        if os.path.isfile(base+".inpr"):
            os.remove(base+".inpr")

        # Move to output data directory
        os.chdir(directory)
        plot = "../../plot_"+str(energy)+"kev.p"
        call(["gnuplot", plot])

    else:
        print "File ",mcnp_output," does not exist!"

if __name__ == "__main__":
   main(sys.argv[1:])
