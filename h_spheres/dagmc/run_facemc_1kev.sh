#!/bin/bash
##---------------------------------------------------------------------------##
## FACEMC test runner
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/ljkerst/software/MCNP/ccc810/MCNP_DATA

# Run Facemc
../../../bin/facemc --sim_info=sim_info.xml --geom_def=h_spheres_geom.xml --mat_def=h_spheres_mat.xml --resp_def=h_spheres_rsp_fn.xml --est_def=h_spheres_est_1kev.xml --src_def=h_spheres_source_1kev.xml --cross_sec_dir=$CROSS_SECTION_XML_PATH --simulation_name="h_spheres_1kev" --threads=12
