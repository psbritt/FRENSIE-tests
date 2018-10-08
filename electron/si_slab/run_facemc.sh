#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
##---------------------------------------------------------------------------##

# Run Facemc
../../bin/facemc --sim_info=sim_info.xml --geom_def=root-geom.xml --mat_def=mat.xml --resp_def=rsp_fn.xml --est_def=est.xml --src_def=source.xml --cross_sec_dir=/home/lkersting/frensie/src/packages/test_files --threads=12
