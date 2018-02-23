#! /usr/bin/env python
import argparse as ap
import h5py

# Set up the argument parser
description = "This script allows one to pull information from the "\
              "simulation.h5 file generated after running facemc. The output "\
              "is dumped to the screen."

parser = ap.ArgumentParser(description=description)

simulation_file_msg = "the simulation.h5 file (with path)."
parser.add_argument('-f', help=simulation_file_msg, required=True)

history_msg = "the desired history number."
parser.add_argument('-n', help=history_msg, required=True)

particle_msg = "the desired particle type."
parser.add_argument('-p', help=particle_msg, required=True)

generation_msg = "the desired generation number."
parser.add_argument('-g', help=generation_msg, required=True)

location_msg = "the desired generation location."
parser.add_argument('-l', help=location_msg, required=True)

location_msg = "the desired track attribute (collision_number, energy, weight, position, direction or all)."
parser.add_argument('-a', help=location_msg, required=True)

# Parse the user's arguments
user_args = parser.parse_args()

# Open the simulation.h5 file
hdf5_file = h5py.File(user_args.f,'r')

particle_type_id = "0"
if user_args.p == "Photon" or user_args.p == "PHOTON" or user_args.p == "photon":
  particle_type_id = "0"
elif user_args.p == "Neutron" or user_args.p == "NEUTRON" or user_args.p == "neutron":
  particle_type_id = "1"
elif user_args.p == "Electron" or user_args.p == "ELECTRON" or user_args.p == "electron":
  particle_type_id = "2"
elif user_args.p == "Adjoint Photon" or user_args.p == "ADJOINT PHOTON" or user_args.p == "adjoint photon":
  particle_type_id = "3"
elif user_args.p == "Adjoint Neutron" or user_args.p == "ADJOINT NEUTRON" or user_args.p == "adjoint neutron":
  particle_type_id = "5"
elif user_args.p == "Adjoint Electron" or user_args.p == "ADJOINT ELECTRON" or user_args.p == "adjoint electron":
  particle_type_id = "7"
else:
  print "Error: The particle type ", str(user_args.p), " is invalid!"

attribute_base = "Particle_Tracker/"+str(user_args.n)+"/"+particle_type_id+"/"+str(user_args.g)+"/"+str(user_args.l)+"/"


attributes = ["collision_number", "x_position", "y_position", "z_position", "x_direction", "y_direction", "z_direction", "energy", "weight"]

if attributes.count(str(user_args.a)) == 0 and str(user_args.a) != "all":
  print "Error: The requested attribute", str(user_args.a) ,"is invalid!"
else:
  attribute_group = attribute_base+str(user_args.a)

  if str(user_args.a) == "position" or str(user_args.a) == "direction":
    print "# ", attribute_group, ":"
    print "Collision Number\tx",str(user_args.a),"\t\ty",str(user_args.a),"\t\tz",str(user_args.a)

    # Print the dataset if it exists
    if attribute_base in hdf5_file:
        col_num_group = attribute_base+"collision_number"
        x_group = attribute_base+"x_"+str(user_args.a)
        y_group = attribute_base+"y_"+str(user_args.a)
        z_group = attribute_base+"z_"+str(user_args.a)
        col_num_set = hdf5_file[col_num_group]
        x_set = hdf5_file[x_group]
        y_set = hdf5_file[y_group]
        z_set = hdf5_file[z_group]

        for i in range(0, len(x_set) ):
          print int(col_num_set[i]),"\t\t\t",'%.11e' % x_set[i],"\t",'%.11e' %y_set[i],"\t",'%.11e' %z_set[i]

    else:
        print "Error: the requested particle track id does not exist"

  elif str(user_args.a) == "all":
    print "# ", attribute_group, ":"
    print "Col. Number\tx position\ty position\tz position\tx direction\ty direction\tz direction\tenergy\t\tweight"

    # Print the dataset if it exists
    if attribute_base in hdf5_file:
      col_num_group = attribute_base+"collision_number"
      x_pos_group = attribute_base+"x_position"
      y_pos_group = attribute_base+"y_position"
      z_pos_group = attribute_base+"z_position"
      x_dir_group = attribute_base+"x_direction"
      y_dir_group = attribute_base+"y_direction"
      z_dir_group = attribute_base+"z_direction"
      energy_group = attribute_base+"energy"
      weight_group = attribute_base+"weight"
      col_num_set = hdf5_file[col_num_group]
      x_pos_set = hdf5_file[x_pos_group]
      y_pos_set = hdf5_file[y_pos_group]
      z_pos_set = hdf5_file[z_pos_group]
      x_dir_set = hdf5_file[x_dir_group]
      y_dir_set = hdf5_file[y_dir_group]
      z_dir_set = hdf5_file[z_dir_group]
      energy_set = hdf5_file[energy_group]
      weight_set = hdf5_file[weight_group] 

      for i in range(0, len(col_num_set) ):
        print int(col_num_set[i]),"\t\t",'%.6e' % x_pos_set[i],"\t",'%.6e' %y_pos_set[i],"\t",'%.6e' %z_pos_set[i],"\t",'%.6e' %x_dir_set[i],"\t",'%.6e' %y_dir_set[i],"\t",'%.6e' %z_dir_set[i],"\t",'%.6e' %energy_set[i],"\t",'%.6e' %weight_set[i]

    else:
        print "Error: the requested particle track id does not exist"

  else:

    print "# ", attribute_group, ":"

    # Print the dataset if it exists
    if attribute_group in hdf5_file:
        dset = hdf5_file[attribute_group]
        array = dset[:]

        for i in array:
          print i

    else:
        print "Error: the requested particle track id does not exist"

hdf5_file.close()

