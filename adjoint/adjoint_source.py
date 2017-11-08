#! /usr/bin/env python
import argparse as ap
import PyFrensie.Data.Native as Native
import PyTrilinos.Teuchos as Teuchos
import numpy
import xml.etree.ElementTree as ET
import sys; sys.path.append("../")
from ElementTree_pretty import prettify

# Set up the argument parser
description = "This script allows one to write the adjoint_source.xml file for "\
              "FACEMC. The input parameter is the source energy and "\
              "cross_section.xml directory"

parser = ap.ArgumentParser(description=description)

directory_msg = "The cross_Section.xml directory"
parser.add_argument('-d', help=directory_msg, required=True)

energy_msg = "The max adjoint energy (in MeV)"
parser.add_argument('-e', help=energy_msg, required=True)

# Parse the user's arguments
user_args = parser.parse_args()
max_energy = float(user_args.e)
datadir = user_args.d

# -------------------------------------------------------------------------- ##
# Get Adjoint Source Distribution
# -------------------------------------------------------------------------- ##
source = Teuchos.FileInputSource( datadir + '/cross_sections.xml' )
xml_obj = source.getObject()
cs_list = Teuchos.XMLParameterListReader().toParameterList( xml_obj )

data_list = cs_list.get( 'H-Native' )
native_file_name = datadir + data_list.get( 'electroatomic_file_path' )

native_data = Native.ElectronPhotonRelaxationDataContainer( native_file_name )

energy_grid = native_data.getElectronEnergyGrid()
total_cs = native_data.getTotalElectronCrossSection()

e_bin = 0

energy_print = "{" + str(energy_grid[0])
cross_section_print = "{" + str(total_cs[0])
for i in range(1,len(energy_grid)):
  if energy_grid[i] <= max_energy:
    energy_print = energy_print + "," + str(energy_grid[i])
    cross_section_print = cross_section_print + "," + str(total_cs[i])
    e_bin = i

if energy_grid[e_bin] != max_energy:
  log_slope = numpy.log(max_energy/energy_grid[e_bin])/numpy.log(energy_grid[e_bin+1]/energy_grid[e_bin])
  max_energy_cs = total_cs[e_bin]*pow(total_cs[e_bin+1]/total_cs[e_bin], log_slope)
  energy_print = energy_print + "," + str(max_energy)
  cross_section_print = cross_section_print + "," + str(max_energy_cs)

energy_print = energy_print + "}"
cross_section_print = cross_section_print + "}"
source_distribution = "{" + energy_print + "," + cross_section_print + "}"

name = "adjoint_source_"+str(max_energy)+".xml"

root = ET.Element("ParameterList", name="Source")

parameters = ET.SubElement(root, "ParameterList", name="Adjoint Point Source")

ET.SubElement(parameters, "Parameter", name="Id", type="int", value="1")

ET.SubElement(parameters, "Parameter", name="Particle Type", type="string", value="Adjoint Electron")

sub_list_1 = ET.SubElement(parameters, "ParameterList", name="Spatial Distribution")
ET.SubElement(sub_list_1, "Parameter", name="Position", type="Array(double)", value="{0.0,0.0,0.0}")

ET.SubElement(parameters, "Parameter", name="Energy Distribution", type="Tabular LogLog Distribution", value=source_distribution)

prettify(root,name)
print name