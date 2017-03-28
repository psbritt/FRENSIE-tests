#! /usr/bin/env python
import argparse as ap
import xml.etree.ElementTree as ET
from ElementTree_pretty import prettify

# Set up the argument parser
description = "This script allows one to write the sim_info.xml file for FACEMC. "\
              "The input parameter is the source energy."

parser = ap.ArgumentParser(description=description)

history_msg = "the number of histories as an int (ie: 1000 not 1e-4)"
parser.add_argument('-n', help=history_msg, required=True)

cutoff_msg = "the cutoff angle cosine"
parser.add_argument('-c', help=cutoff_msg, required=True)

linlinlog_msg = "lin-lin-log electron interpolation on (true/false)"
parser.add_argument('-l', help=linlinlog_msg, required=True)

sampling_msg = "correlated electron sampling on (true/false)"
parser.add_argument('-s', help=sampling_msg, required=True)

unit_based_msg = "unit based electron interpolation on (true/false)"
parser.add_argument('-u', help=unit_based_msg, required=True)

elastic_msg = "elastic electron reaction on (true/false)"
parser.add_argument('-e', help=elastic_msg, required=True)

brem_msg = "bremsstrahlung electron reaction on (true/false)"
parser.add_argument('-b', help=brem_msg, required=True)

ionization_msg = "electroionization electron reaction on (true/false)"
parser.add_argument('-i', help=ionization_msg, required=True)

excitation_msg = "atomic excitation electron reaction on (true/false)"
parser.add_argument('-a', help=excitation_msg, required=True)

# Parse the user's arguments
user_args = parser.parse_args()
energy = 15.7
number_of_histories = user_args.n
cutoff_cosine = user_args.c
linlinlog_bool = user_args.l
correlated_bool = user_args.s
unit_based_bool = user_args.u
elastic_bool = user_args.e
brem_bool = user_args.b
ionization_bool = user_args.i
excitation_bool = user_args.a

# Set xml file name
name = "sim_info_"+str(cutoff_cosine)
if linlinlog_bool == "false":
    name += "_linlinlin"
if correlated_bool == "false":
    name += "_stochastic"
if unit_based_bool == "false":
    name += "_exact"
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

ET.SubElement(parameter_2, "Parameter", name="Electron Elastic", type="bool", value=elastic_bool )
ET.SubElement(parameter_2, "Parameter", name="Bremsstrahlung Elastic", type="bool", value=brem_bool )
ET.SubElement(parameter_2, "Parameter", name="Electroionization Elastic", type="bool", value=ionization_bool )
ET.SubElement(parameter_2, "Parameter", name="Atomic Excitation Elastic", type="bool", value=excitation_bool )

ET.SubElement(parameter_2, "Parameter", name="Electron LinLinLog Interpolation", type="bool", value=linlinlog_bool )
ET.SubElement(parameter_2, "Parameter", name="Electron Correlated Sampling", type="bool", value=correlated_bool )
ET.SubElement(parameter_2, "Parameter", name="Electron Unit Based Interpolation", type="bool", value=unit_based_bool )

prettify(root,name)
