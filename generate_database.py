#!/bin/sh
# This file is named hanson.sh
#SBATCH --partition=pre
#SBATCH --time=1-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1

##---------------------------------------------------------------------------##
##-------------------------- FRENSIE DATA GENERATOR -------------------------##
##---------------------------------------------------------------------------##
## Script to generate the frensie database.xml file on the cluster
# NOTE: The frensie bin directory must be added to PATH and the frensie python
# lib directory must be added to PYTHONPATH for the following commands to work.
# Run script in the mcnp6.2 data directory

##---------------------------------------------------------------------------##
##-------------------------------- COMMANDS ---------------------------------##
##---------------------------------------------------------------------------##
EXTRA_ARGS=$@

FRENSIE_SRC=/home/lkersting/dag_frensie/src

# Process the mcnp6.2 xsdir file
process_xsdir.py -o --xsdir=xsdir_mcnp6.2 --log_file=process_xsdir_log.txt

# Copy the endl_downloader python script to current directory
cp ${FRENSIE_SRC}/scripts/endl_downloader.py ./

# Create endl_downloader bash script
python ./endl_downloader.py -a > endl_downloader.sh

# Download the endl data
bash ./endl_downloader.sh -d ./

# Process the endl data
endl_to_native_endl.py -a

# Create a directory for native epr data
mkdir native; mkdir native/epr

# Generate native epr data
generate_native_epr.py -o --log_file=generate_native_epr_log.out