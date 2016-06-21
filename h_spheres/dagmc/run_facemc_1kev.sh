#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
##---------------------------------------------------------------------------##

# Set data directory path.
#echo -n "Enter cross_section.xml directory: > "
#read cross_section_directory

# Run Facemc
../../../bin/facemc --sim_info=sim_info.xml --geom_def=h_spheres_geom.xml --mat_def=h_spheres_mat.xml --resp_def=h_spheres_rsp_fn.xml --est_def=h_spheres_est_1kev.xml --src_def=h_spheres_source.xml --cross_sec_dir=/home/ljkerst/software/frensie/src/packages/test_files --threads=12
