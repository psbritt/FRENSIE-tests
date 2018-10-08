#! /usr/bin/env python
import argparse as ap
import xml.etree.ElementTree as ET
import sys; sys.path.append("../")
from ElementTree_pretty import prettify

# Set up the argument parser
description = "This script allows one to write the source.xml file for FACEMC. "\
              "The input parameter is the source energy."

parser = ap.ArgumentParser(description=description)

energy_msg = "the source energy (in MeV)"
parser.add_argument('-e', help=energy_msg, required=True)

# Parse the user's arguments
user_args = parser.parse_args()
energy = user_args.e
source_energy = "{"+energy+"}"
name = "source_"+energy+".xml"

root = ET.Element("ParameterList", name="Source")

parameters = ET.SubElement(root, "ParameterList", name="Monoenergetic point source")

ET.SubElement(parameters, "Parameter", name="Id", type="int", value="1")

ET.SubElement(parameters, "Parameter", name="Particle Type", type="string", value="Electron")

sub_list_1 = ET.SubElement(parameters, "ParameterList", name="Spatial Distribution")
ET.SubElement(sub_list_1, "Parameter", name="Position", type="Array(double)", value="{0.0,0.0,0.0}")

ET.SubElement(parameters, "Parameter", name="Energy Distribution", type="Delta Distribution", value=source_energy)

prettify(root,name)
print name