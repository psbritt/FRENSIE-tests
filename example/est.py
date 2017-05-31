#! /usr/bin/env python
import argparse as ap
import xml.etree.ElementTree as ET
from ElementTree_pretty import prettify

# Set up the argument parser
description = "This script allows one to write the est.xml file for FACEMC."\
              "The input parameter is the geometry type."

parser = ap.ArgumentParser(description=description)

energy_msg = "The source energy (in MeV)"
parser.add_argument('-e', help=energy_msg, required=True)

geom_type_msg = "the geometry type (DagMC, ROOT)"
parser.add_argument('-t', help=geom_type_msg, required=False)

# Parse the user's arguments
user_args = parser.parse_args()
energy = user_args.e

geom_type = "DagMC"
if user_args.t:
    geom_type = user_args.t

# Set xml file name
name = "est_"+str(energy)

# assume energy is 0.01 MeV
bins = "{ 1e-5,5e-5, 198i, 1e-2}"
if energy == ".001" or energy == "0.001":
    bins = "{ 1e-5, 197i, 1e-3}"
if energy == ".1" or energy == "0.1":
    bins = "{ 1e-5, 1e-4, 5e-4, 198i, 1e-1}"

root = ET.Element("ParameterList", name="Estimators")

if geom_type == "DagMC":

    # Flux on sphere surfaces
    tally = "Surface Flux"

    parameter_1 = ET.SubElement(root, "ParameterList", name="Flux on sphere surfaces")

    ET.SubElement(parameter_1, "Parameter", name="Id", type="unsigned int", value="2")
    ET.SubElement(parameter_1, "Parameter", name="Type", type="string", value=tally)
    ET.SubElement(parameter_1, "Parameter", name="Particle Type", type="string", value="Electron")

    sub_list_1 = ET.SubElement(parameter_1, "ParameterList", name="Bins")
    ET.SubElement(sub_list_1, "Parameter", name="Energy Bins", type="Array", value=bins)

    tally = "Surface Current"

    parameter_2 = ET.SubElement(root, "ParameterList", name="Current on sphere surfaces")

    ET.SubElement(parameter_2, "Parameter", name="Id", type="unsigned int", value="3")
    ET.SubElement(parameter_2, "Parameter", name="Type", type="string", value=tally)
    ET.SubElement(parameter_2, "Parameter", name="Particle Type", type="string", value="Electron")
    #ET.SubElement(parameter_2, "Parameter", name=tally_type, type="Array", value=tally_vols)

    sub_list_2 = ET.SubElement(parameter_2, "ParameterList", name="Bins")
    ET.SubElement(sub_list_2, "Parameter", name="Energy Bins", type="Array", value=bins)

    # Track Length Flux in Sphere
    tally = "Cell Track-Length Flux"

    parameter_3 = ET.SubElement(root, "ParameterList", name="Track Length Flux in Sphere")

    ET.SubElement(parameter_3, "Parameter", name="Id", type="unsigned int", value="1")
    ET.SubElement(parameter_3, "Parameter", name="Type", type="string", value=tally)
    ET.SubElement(parameter_3, "Parameter", name="Particle Type", type="string", value="Electron")
    sub_list_3 = ET.SubElement(parameter_3, "ParameterList", name="Bins")
    ET.SubElement(sub_list_3, "Parameter", name="Energy Bins", type="Array", value=bins)

    # Pulse Height in Sphere
    tally = "Cell Pulse Height"

else:
    # Track Length Flux in Sphere
    tally = "Cell Track-Length Flux"
    name += "_root"

    parameter_3 = ET.SubElement(root, "ParameterList", name="Track Length Flux in Sphere")

    ET.SubElement(parameter_3, "Parameter", name="Id", type="unsigned int", value="1")
    ET.SubElement(parameter_3, "Parameter", name="Type", type="string", value=tally)
    ET.SubElement(parameter_3, "Parameter", name="Particle Type", type="string", value="Electron")
    ET.SubElement(parameter_3, "Parameter", name="Cells", type="Array", value="{1}")

    sub_list_3 = ET.SubElement(parameter_3, "ParameterList", name="Bins")
    ET.SubElement(sub_list_3, "Parameter", name="Energy Bins", type="Array", value=bins)

name +=".xml"
prettify(root,name)

