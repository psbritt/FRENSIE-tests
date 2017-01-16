#! /usr/bin/env python
import argparse as ap
import lxml.etree as ET

# Set up the argument parser
description = "This script allows one to write the sim_info.xml file for FACEMC. "\
              "The input parameter is the source energy."

parser = ap.ArgumentParser(description=description)

energy_msg = "the source energy (in MeV)"
parser.add_argument('-e', help=energy_msg, required=True)

cutoff_msg = "the cutoff angle cosine"
parser.add_argument('-c', help=cutoff_msg, required=True)

# Parse the user's arguments
user_args = parser.parse_args()
energy = user_args.e
cutoff_cosine = user_args.c

root = ET.Element("ParameterList", name="Simulation Info")


parameter_1 = ET.SubElement(root, "ParameterList", name="General Properties")

ET.SubElement(parameter_1, "Parameter", name="Mode", type="string", value="Electron")

ET.SubElement(parameter_1, "Parameter", name="Histories", type="unsigned int", value="100")



parameter_2 = ET.SubElement(root, "ParameterList", name="Electron Properties")

ET.SubElement(parameter_2, "Parameter", name="Max Electron Energy", type="double", value=str(energy))

ET.SubElement(parameter_2, "Parameter", name="Elastic Cutoff Angle Cosine", type="double", value=str(cutoff_cosine) )

ET.SubElement(parameter_2, "Parameter", name="Electron Atomic Relaxation", type="bool", value="true" )

tree = ET.ElementTree(root)
tree.write("sim_info.xml", pretty_print=True)
