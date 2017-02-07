#! /usr/bin/env python
import argparse as ap
import xml.etree.ElementTree as ET
from ElementTree_pretty import prettify

# Set up the argument parser
description = "This script allows one to write the sim_info.xml file for FACEMC. "\
              "The input parameter is the source energy."

parser = ap.ArgumentParser(description=description)

energy_msg = "the source energy (in MeV)"
parser.add_argument('-e', help=energy_msg, required=True)

history_msg = "the number of histories as an int (ie: 1000 not 1e-4)"
parser.add_argument('-n', help=history_msg, required=True)

cutoff_msg = "the cutoff angle cosine"
parser.add_argument('-c', help=cutoff_msg, required=True)

elastic_msg = "the elastic electron reaction on (true/false)"
parser.add_argument('-l', help=elastic_msg, required=True)

brem_msg = "the bremsstrahlung electron reaction on (true/false)"
parser.add_argument('-b', help=brem_msg, required=True)

ionization_msg = "the electroionization electron reaction on (true/false)"
parser.add_argument('-i', help=ionization_msg, required=True)

excitation_msg = "the atomic excitation electron reaction on (true/false)"
parser.add_argument('-a', help=excitation_msg, required=True)

# Parse the user's arguments
user_args = parser.parse_args()
energy = user_args.e
number_of_histories = user_args.n
cutoff_cosine = user_args.c
elastic_bool = user_args.l
brem_bool = user_args.b
ionization_bool = user_args.i
excitation_bool = user_args.a

# Set xml file name
name = "sim_info_"+str(energy)+"_"+str(cutoff_cosine)
if elastic_bool == "false":
    name += "_no_elastic"
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

ET.SubElement(parameter_2, "Parameter", name="Elastic Cutoff Angle Cosine", type="double", value=str(cutoff_cosine) )

ET.SubElement(parameter_2, "Parameter", name="Electron Atomic Relaxation", type="bool", value="true" )

prettify(root,name)
