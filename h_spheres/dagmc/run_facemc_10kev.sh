#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/software/mcnpdata/

# Run Facemc
../../../bin/facemc --sim_info=sim_info.xml --geom_def=h_spheres_geom.xml --mat_def=h_spheres_mat.xml --resp_def=h_spheres_rsp_fn.xml --est_def=h_spheres_est_10kev.xml --src_def=h_spheres_source_10kev.xml --cross_sec_dir=$CROSS_SECTION_XML_PATH --simulation_name="h_spheres_10kev" --threads=12

# Extract the flux data
../../../bin/edump.py -f h_spheres_10kev.h5 -e 1 -i 1 > results/10kev_flux_1.txt
../../../bin/edump.py -f h_spheres_10kev.h5 -e 1 -i 3 > results/10kev_flux_3.txt
../../../bin/edump.py -f h_spheres_10kev.h5 -e 1 -i 6 > results/10kev_flux_6.txt
../../../bin/edump.py -f h_spheres_10kev.h5 -e 1 -i 9 > results/10kev_flux_9.txt
../../../bin/edump.py -f h_spheres_10kev.h5 -e 1 -i 12 > results/10kev_flux_12.txt

# Extract the current data
../../../bin/edump.py -f h_spheres_10kev.h5 -e 2 -i 1 > results/10kev_current_1.txt
../../../bin/edump.py -f h_spheres_10kev.h5 -e 2 -i 3 > results/10kev_current_3.txt
../../../bin/edump.py -f h_spheres_10kev.h5 -e 2 -i 6 > results/10kev_current_6.txt
../../../bin/edump.py -f h_spheres_10kev.h5 -e 2 -i 9 > results/10kev_current_9.txt
../../../bin/edump.py -f h_spheres_10kev.h5 -e 2 -i 12 > results/10kev_current_12.txt
