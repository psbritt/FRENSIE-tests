#! /usr/bin/env python
import datetime
import os
import shutil

today = datetime.date.today()
directory = "./results/"+str(today)+"/"

if not os.path.isdir(directory):
    os.mkdir(directory)

energy = input("Enter the energy to process in keV (1, 10, 100): ")

tally_list = ['10',
              '11',
              '12',
              '13',
              '14' ]

estimator_list = ['current', 'flux' ]

# Read the mcnp data file
mcnp_output = "h_spheres_"+str(energy)+"kev.inpo"
with open(mcnp_output) as data:
    # go through all tallies
    for i in tally_list:
        start=" surface  "+i

        # go through the current and flux estimators
        for j in estimator_list:
            name = "results/"+str(today)+"/"+str(energy)+"kev_"+j+"_"+i+".txt"
            file = open(name, 'w')
            header = "Energy     "+j+"        Sigma\t"+str(today)+"\n"
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
new_name = "../../../results/mcnp/h_spheres_"+str(energy)+"kev_"+date+".inpo"
shutil.copy(mcnp_output,new_name)
