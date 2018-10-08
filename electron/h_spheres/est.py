#! /usr/bin/env python
import argparse as ap
import xml.etree.ElementTree as ET
import sys; sys.path.append("../")
from ElementTree_pretty import prettify

# Set up the argument parser
description = "This script allows one to write the est.xml file for FACEMC."\
              "The input parameter is the geometry type."

parser = ap.ArgumentParser(description=description)

energy_msg = "The source energy (in MeV)"
parser.add_argument('-e', help=energy_msg, required=True)

geom_type_msg = "the geometry type (DagMC, ROOT)"
parser.add_argument('-t', help=geom_type_msg, required=False)

tracker_msg = "turn on the particle tracker (true = on, false = off)"
parser.add_argument('-p', help=tracker_msg, required=False)

# Parse the user's arguments
user_args = parser.parse_args()
energy = user_args.e

geom_type = "DagMC"
if user_args.t:
    geom_type = user_args.t

# Set xml file name
name = "est_"+str(energy)

# assume energy is 0.001 MeV
bins = "{ 1e-5, 197i, 1e-3}"
if float(energy) == 0.01:
    bins = "{ 1e-5, 5e-5, 198i, 1e-2}"
if float(energy) == 0.1:
    bins = "{ 1e-5, 1e-4, 5e-4, 198i, 1e-1}"

root = ET.Element("ParameterList", name="Observers")

tally_number = 1
if geom_type == "DagMC" or geom_type == "DAGMC" or geom_type == "dagmc":

    # Flux on sphere surfaces
    tally = "Surface Flux"

    parameter_1 = ET.SubElement(root, "ParameterList", name="Flux on sphere surfaces")

    ET.SubElement(parameter_1, "Parameter", name="Id", type="unsigned int", value=str(tally_number) )
    ET.SubElement(parameter_1, "Parameter", name="Type", type="string", value=tally)
    ET.SubElement(parameter_1, "Parameter", name="Particle Type", type="string", value="Electron")

    sub_list_1 = ET.SubElement(parameter_1, "ParameterList", name="Bins")
    ET.SubElement(sub_list_1, "Parameter", name="Energy Bins", type="Array", value=bins)

    # Current on sphere surfaces
    tally_number = tally_number +1
    tally = "Surface Current"

    parameter_2 = ET.SubElement(root, "ParameterList", name="Current on sphere surfaces")

    ET.SubElement(parameter_2, "Parameter", name="Id", type="unsigned int", value=str(tally_number) )
    ET.SubElement(parameter_2, "Parameter", name="Type", type="string", value=tally)
    ET.SubElement(parameter_2, "Parameter", name="Particle Type", type="string", value="Electron")

    sub_list_2 = ET.SubElement(parameter_2, "ParameterList", name="Bins")
    ET.SubElement(sub_list_2, "Parameter", name="Energy Bins", type="Array", value=bins)

    # Track Length Flux in Sphere
    tally_number = tally_number +1
    tally = "Cell Track-Length Flux"

    parameter_3 = ET.SubElement(root, "ParameterList", name="Track Length Flux in Sphere")

    ET.SubElement(parameter_3, "Parameter", name="Id", type="unsigned int", value=str(tally_number) )
    ET.SubElement(parameter_3, "Parameter", name="Type", type="string", value=tally)
    ET.SubElement(parameter_3, "Parameter", name="Particle Type", type="string", value="Electron")
    sub_list_3 = ET.SubElement(parameter_3, "ParameterList", name="Bins")
    ET.SubElement(sub_list_3, "Parameter", name="Energy Bins", type="Array", value=bins)

else:
    # Track Length Flux in Sphere
    tally = "Cell Track-Length Flux"
    name += "_root"

    parameter_3 = ET.SubElement(root, "ParameterList", name="Track Length Flux in Sphere")

    ET.SubElement(parameter_3, "Parameter", name="Id", type="unsigned int", value=str(tally_number) )
    ET.SubElement(parameter_3, "Parameter", name="Type", type="string", value=tally)
    ET.SubElement(parameter_3, "Parameter", name="Particle Type", type="string", value="Electron")
    ET.SubElement(parameter_3, "Parameter", name="Cells", type="Array", value="{1,2,3,4,5}")

    sub_list_3 = ET.SubElement(parameter_3, "ParameterList", name="Bins")
    ET.SubElement(sub_list_3, "Parameter", name="Energy Bins", type="Array", value=bins)

# Particle Tracker (if asked for)
if user_args.p == "true":
    tally_number = tally_number +1
    tally = "Particle Tracker"

    parameter_4 = ET.SubElement(root, "ParameterList", name="Particle Tracker 1")

    ET.SubElement(parameter_4, "Parameter", name="Id", type="unsigned int", value=str(tally_number) )
    ET.SubElement(parameter_4, "Parameter", name="Type", type="string", value=tally)

name +=".xml"
prettify(root,name)
print name