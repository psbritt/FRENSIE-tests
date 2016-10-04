#!/bin/bash
##---------------------------------------------------------------------------##
## MCNP6 test runner
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
CROSS_SECTION_XML_PATH=/home/software/mcnpdata/

echo -n "Enter the energy to process in keV (1, 10, 100) > "
read INPUT
ENERGY="${INPUT}kev"
echo "You entered: $ENERGY"

# Set cross_section.xml directory path.
NAME="h_spheres_${ENERGY}.inp"

echo "Running MCNP6:"
mcnp6 n="$NAME" tasks = 12

echo "Processing the results:"
echo $INPUT | ./data_processor.py

