#! /usr/bin/env python
import argparse as ap
import xml.etree.ElementTree as ET
from ElementTree_pretty import prettify
import os.path

# Set up the argument parser
description = "This script allows one to write the sim_info.xml file for FACEMC."

parser = ap.ArgumentParser(description=description)

energy_msg = "source energy (in MeV)"
parser.add_argument('-e', help=energy_msg, required=True)

history_msg = "the number of histories as an int (ie: 1000 not 1e-4)"
parser.add_argument('-n', help=history_msg, required=True)

interp_msg = "electron interpolation policy (logloglog, linlinlin, linlinlog)"
parser.add_argument('-l', help=interp_msg, required=True)

grid_msg = "electron grid policy (1 = unit-base correlated, 2 = correlated, 3 = unit-base)"
parser.add_argument('-s', help=grid_msg, required=True)

elastic_dist_msg = "elastic electron distribution ( Coupled, Decoupled, Hybrid )"
parser.add_argument('-d', help=elastic_dist_msg, required=True)

sampling_method_msg = "coupled elastic sampling method ( 1D, 2D, 2DM)"
parser.add_argument('-c', help=sampling_method_msg, required=True )

elastic_msg = "elastic electron reaction on (true/false)"
parser.add_argument('-t', help=elastic_msg, required=True)

brem_msg = "bremsstrahlung electron reaction on (true/false)"
parser.add_argument('-b', help=brem_msg, required=True)

ionization_msg = "electroionization electron reaction on (true/false)"
parser.add_argument('-i', help=ionization_msg, required=True)

excitation_msg = "atomic excitation electron reaction on (true/false)"
parser.add_argument('-a', help=excitation_msg, required=True)

min_energy_msg = "min electron energy (in MeV)"
parser.add_argument('-m', help=min_energy_msg, required=False)

# Parse the user's arguments
user_args = parser.parse_args()

energy = user_args.e
number_of_histories = user_args.n

# Two D Grid parameters
interp = user_args.l

if user_args.s == "1":
  grid = "Unit-base Correlated"
  grid_name = "unit_correlated"
elif user_args.s == "2":
  grid = "Correlated"
  grid_name = "correlated"
elif user_args.s == "3":
  grid = "Unit-base"
  grid_name = "unit_base"
else:
  # Nothing selected cause an error
  grid = "ERROR"
  grid_name = "ERROR"

# Turn reactions on/off
elastic_bool = user_args.t
brem_bool = user_args.b
ionization_bool = user_args.i
excitation_bool = user_args.a

# Elastic Hybrid Cutoff Angle
cutoff_cosine = 1.0
# Elastic Distribution (Coupled, Decoupled, Hybrid)
elastic_distribution = user_args.d
# Elastic Coupled Distribution Sampling Method ( One D Union, Two D Union, Modified Two D Union)
coupled_sampling_method = user_args.c

# Set xml file name
name_base = "sim_info_"+interp+"_"+grid_name+"_"+energy

if elastic_bool == "false":
    name_base += "_no_elastic"
else:
    if elastic_distribution == "Coupled":
        name_base+="_coupled"
        if coupled_sampling_method == "1D":
            name_base+="_1D"
            coupled_sampling_method = "One D Union"
        elif coupled_sampling_method == "2D":
            name_base+="_2D"
            coupled_sampling_method = "Two D Union"
        elif coupled_sampling_method == "2DM":
            name_base+="_2DM"
            coupled_sampling_method = "Modified Two D Union"
        else:
            coupled_sampling_method = ""
    elif elastic_distribution == "Hybrid":
        name_base+="_0.9"
        cutoff_cosine = 0.9

if brem_bool == "false":
    name_base += "_no_brem"
if ionization_bool == "false":
    name_base += "_no_ionization"
if excitation_bool == "false":
    name_base += "_no_excitation"

min_energy="1e-4"
if user_args.m:
  min_energy=user_args.m

root = ET.Element("ParameterList", name="Simulation Info")

parameter_1 = ET.SubElement(root, "ParameterList", name="General Properties")

ET.SubElement(parameter_1, "Parameter", name="Mode", type="string", value="Electron")

ET.SubElement(parameter_1, "Parameter", name="Histories", type="unsigned int", value=number_of_histories)



parameter_2 = ET.SubElement(root, "ParameterList", name="Electron Properties")

ET.SubElement(parameter_2, "Parameter", name="Min Electron Energy", type="double", value=min_energy)
ET.SubElement(parameter_2, "Parameter", name="Max Electron Energy", type="double", value=str(energy))
ET.SubElement(parameter_2, "Parameter", name="Electron Atomic Relaxation", type="bool", value="true" )
ET.SubElement(parameter_2, "Parameter", name="Electron Grid Policy", type="string", value=grid )
ET.SubElement(parameter_2, "Parameter", name="Electron Interpolation Policy", type="string", value=interp )

ET.SubElement(parameter_2, "Parameter", name="Electron Bremsstrahlung", type="bool", value=brem_bool )
ET.SubElement(parameter_2, "Parameter", name="Electron Electroionization", type="bool", value=ionization_bool )
ET.SubElement(parameter_2, "Parameter", name="Electron Atomic Excitation", type="bool", value=excitation_bool )
ET.SubElement(parameter_2, "Parameter", name="Electron Elastic", type="bool", value=elastic_bool )

if elastic_bool:
  ET.SubElement(parameter_2, "Parameter", name="Elastic Cutoff Angle Cosine", type="double", value=str(cutoff_cosine) )
  ET.SubElement(parameter_2, "Parameter", name="Electron Elastic Distribution", type="string", value=elastic_distribution )

  if elastic_distribution == "Coupled":
    ET.SubElement(parameter_2, "Parameter", name="Coupled Elastic Sampling Method", type="string", value=coupled_sampling_method )

name = name_base + ".xml"
i=1
while os.path.isfile(name):
  name = name_base+"_"+str(i)+".xml"
  i=i+1

prettify(root,name)
print name