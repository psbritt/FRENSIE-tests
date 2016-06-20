#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
##---------------------------------------------------------------------------##

# Run Facemc
./facemc --sim_info=sim_info.xml --geom_def=h_spheres_geom.xml --mat_def=h_spheres_mat.xml --resp_def=h_spheres_rsp_fn.xml --est_def=h_spheres_est_10kev.xml --src_def=h_spheres_source.xml --cross_sec_dir=/home/lkersting/frensie/src/packages/test_files --threads=12
