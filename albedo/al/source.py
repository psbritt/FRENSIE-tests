#! /usr/bin/env python
import argparse as ap
import xml.etree.ElementTree as ET
from ElementTree_pretty import prettify

# Set up the argument parser
description = "This script allows one to write the source.xml file for FACEMC. "\
              "The input parameter is the source energy."

parser = ap.ArgumentParser(description=description)

source_energy_msg = "the source energy (in MeV)"
parser.add_argument('-e', help=source_energy_msg, required=True)

# Parse the user's arguments
user_args = parser.parse_args()
energy = user_args.e

root = ET.Element("ParameterList", name="Source")

parameters = ET.SubElement(root, "ParameterList", name="Basic Distributed Source")

ET.SubElement(parameters, "Parameter", name="Id", type="int", value="1")

ET.SubElement(parameters, "Parameter", name="Particle Type", type="string", value="Electron")

sub_list_1 = ET.SubElement(parameters, "ParameterList", name="Spatial Distribution")
ET.SubElement(sub_list_1, "Parameter", name="Position", type="Array(double)", value="{-20.0,0.0,0.0}")

ET.SubElement(parameters, "Parameter", name="Energy Distribution", type="Delta Distribution", value="{" + str(energy) + "}")

sub_list_2 = ET.SubElement(parameters, "ParameterList", name="Directional Distribution")
ET.SubElement(sub_list_2, "Parameter", name="Direction", type="Array(double)", value="{1.0,0.0,0.0}")

prettify(root,"source.xml")
