#! /usr/bin/env python
import argparse as ap
import xml.etree.ElementTree as ET
from ElementTree_pretty import prettify

# Set up the argument parser
description = "This script allows one to write the source.xml file for FACEMC. "\
              "The input parameter is the source energy."

parser = ap.ArgumentParser(description=description)

geom_type_msg = "the geometry type (DagMC, ROOT)"
parser.add_argument('-t', help=geom_type_msg, required=False)

# Parse the user's arguments
user_args = parser.parse_args()
geom_type = user_args.t

root = ET.Element("ParameterList", name="Geometry")

if geom_type == "DagMC":
    ET.SubElement(root, "Parameter", name="Handler", type="string", value="DagMC")
    ET.SubElement(root, "Parameter", name="CAD File", type="string", value="geom.sat")
    ET.SubElement(root, "Parameter", name="Facet Tolerance", type="double", value="1e-3")
    ET.SubElement(root, "Parameter", name="Use Fast Id Lookup", type="bool", value="True")

elif geom_type == "ROOT":
    ET.SubElement(root, "Parameter", name="Handler", type="string", value="ROOT")
    ET.SubElement(root, "Parameter", name="Root File", type="string", value="geom.root")
    ET.SubElement(root, "Parameter", name="Termination Cell Synonym", type="string", value="graveyard")
    ET.SubElement(root, "Parameter", name="Estimator Synonym", type="string", value="estimator")

else:
    # Just assume DagMC
    ET.SubElement(root, "Parameter", name="Handler", type="string", value="DagMC")
    ET.SubElement(root, "Parameter", name="CAD File", type="string", value="geom.sat")
    ET.SubElement(root, "Parameter", name="Facet Tolerance", type="double", value="1e-3")
    ET.SubElement(root, "Parameter", name="Use Fast Id Lookup", type="bool", value="True")


ET.SubElement(root, "Parameter", name="Material Property", type="string", value="mat")
ET.SubElement(root, "Parameter", name="Density Property", type="string", value="rho")

prettify(root,"geom.xml")
