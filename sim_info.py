#! /usr/bin/env python
import argparse as ap
import xml.etree.ElementTree as ET
from ElementTree_pretty import prettify

# Set up the argument parser
description = "This script allows one to write the sim_info.xml file for FACEMC."

parser = ap.ArgumentParser(description=description)

energy_msg = "source energy (in MeV)"
parser.add_argument('-e', help=energy_msg, required=True)

history_msg = "the number of histories as an int (ie: 1000 not 1e-4)"
parser.add_argument('-n', help=history_msg, required=True)

interp_msg = "electron interpolation (logloglog, linlinlin, loglinlin)"
parser.add_argument('-l', help=interp_msg, required=True)

sampling_msg = "correlated electron sampling on (true/false)"
parser.add_argument('-s', help=sampling_msg, required=True)

unit_based_msg = "unit based electron interpolation on (true/false)"
parser.add_argument('-u', help=unit_based_msg, required=True)

elastic_dist_msg = "elastic electron distribution ( Coupled, Decoupled, Hybrid )"
parser.add_argument('-d', help=elastic_dist_msg, required=True)

sampling_method_msg = "coupled elastic sampling method ( 1D, 2D, Simplified)"
parser.add_argument('-c', help=sampling_method_msg, required=True )

elastic_msg = "elastic electron reaction on (true/false)"
parser.add_argument('-t', help=elastic_msg, required=True)

brem_msg = "bremsstrahlung electron reaction on (true/false)"
parser.add_argument('-b', help=brem_msg, required=True)

ionization_msg = "electroionization electron reaction on (true/false)"
parser.add_argument('-i', help=ionization_msg, required=True)

excitation_msg = "atomic excitation electron reaction on (true/false)"
parser.add_argument('-a', help=excitation_msg, required=True)

# Parse the user's arguments
user_args = parser.parse_args()

energy = user_args.e
number_of_histories = user_args.n

# Two D Sampling parameters
interp = user_args.l
correlated_bool = user_args.s
unit_based_bool = user_args.u

# Turn reactions on/off
elastic_bool = user_args.t
brem_bool = user_args.b
ionization_bool = user_args.i
excitation_bool = user_args.a

# Elastic Hybrid Cutoff Angle
cutoff_cosine = 1.0
# Elastic Distribution (Coupled, Decoupled, Hybrid)
elastic_distribution = user_args.d
# Elastic Coupled Distribution Sampling Method ( One D Union, Two D Union, Simplified Union)
couled_sampling_method = user_args.c

# Set xml file name
name = "sim_info_"+interp+"_"+energy
if correlated_bool == "false":
    name += "_stochastic"
if unit_based_bool == "false":
    name += "_exact"

if elastic_bool == "false":
    name += "_no_elastic"
else:
    if elastic_distribution == "Coupled":
        name+="_coupled"
        if couled_sampling_method == "1D":
            name+="_1D"
            couled_sampling_method = "One D Union"
        elif couled_sampling_method == "2D":
            name+="_2D"
            couled_sampling_method = "Two D Union"
        else:
            couled_sampling_method = "Simplified Union"
    elif elastic_distribution == "Hybrid":
        name+="_0.9"
        cutoff_cosine = 0.9

if brem_bool == "false":
    name += "_no_brem"
if ionization_bool == "false":
    name += "_no_ionization"
if excitation_bool == "false":
    name += "_no_excitation"
name += ".xml"


root = ET.Element("ParameterList", name="Simulation Info")

parameter_1 = ET.SubElement(root, "ParameterList", name="General Properties")

ET.SubElement(parameter_1, "Parameter", name="Mode", type="string", value="Electron")

ET.SubElement(parameter_1, "Parameter", name="Histories", type="unsigned int", value=number_of_histories)



parameter_2 = ET.SubElement(root, "ParameterList", name="Electron Properties")

ET.SubElement(parameter_2, "Parameter", name="Max Electron Energy", type="double", value=str(energy))
ET.SubElement(parameter_2, "Parameter", name="Electron Atomic Relaxation", type="bool", value="true" )

ET.SubElement(parameter_2, "Parameter", name="Electron Correlated Sampling", type="bool", value=correlated_bool )
ET.SubElement(parameter_2, "Parameter", name="Electron Unit Based Interpolation", type="bool", value=unit_based_bool )

ET.SubElement(parameter_2, "Parameter", name="Electron Elastic", type="bool", value=elastic_bool )

if elastic_bool:
  ET.SubElement(parameter_2, "Parameter", name="Elastic Cutoff Angle Cosine", type="double", value=str(cutoff_cosine) )
  ET.SubElement(parameter_2, "Parameter", name="Electron Elastic Interpolation", type="string", value=interp )
  ET.SubElement(parameter_2, "Parameter", name="Electron Elastic Distribution", type="string", value=elastic_distribution )

  if elastic_distribution == "Coupled":
    ET.SubElement(parameter_2, "Parameter", name="Coupled Elastic Sampling Method", type="string", value=couled_sampling_method )

ET.SubElement(parameter_2, "Parameter", name="Electron Bremsstrahlung", type="bool", value=brem_bool )

if brem_bool:
  ET.SubElement(parameter_2, "Parameter", name="Electron Bremsstrahlung Interpolation", type="string", value=interp )

ET.SubElement(parameter_2, "Parameter", name="Electron Electroionization", type="bool", value=ionization_bool )

if ionization_bool:
  ET.SubElement(parameter_2, "Parameter", name="Electron Electroionization Interpolation", type="string", value=interp )

ET.SubElement(parameter_2, "Parameter", name="Electron Atomic Excitation", type="bool", value=excitation_bool )

prettify(root,name)
print name