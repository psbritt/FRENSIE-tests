#! /usr/bin/env python
import argparse as ap
import xml.etree.ElementTree as ET
from ElementTree_pretty import prettify

# Set up the argument parser
description = "This script allows one to write the source.xml file for FACEMC."

root = ET.Element("ParameterList", name="Source")

parameters = ET.SubElement(root, "ParameterList", name="Basic Distributed Source")

ET.SubElement(parameters, "Parameter", name="Id", type="int", value="1")

ET.SubElement(parameters, "Parameter", name="Particle Type", type="string", value="Electron")

sub_list_1 = ET.SubElement(parameters, "ParameterList", name="Spatial Distribution")
ET.SubElement(sub_list_1, "Parameter", name="Position", type="Array(double)", value="{-0.5,0.0,0.0}")

ET.SubElement(parameters, "Parameter", name="Energy Distribution", type="Delta Distribution", value="{15.7}")

sub_list_2 = ET.SubElement(parameters, "ParameterList", name="Directional Distribution")
ET.SubElement(sub_list_2, "Parameter", name="Direction", type="Array(double)", value="{1.0,0.0,0.0}")

prettify(root,"source.xml")
