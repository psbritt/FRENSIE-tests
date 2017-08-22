#!/bin/bash
##---------------------------------------------------------------------------##
## Al Albedo test data updater
##---------------------------------------------------------------------------##

# Get the date for the table notes
today=`date`
notes="This table was generated on $today. It is for the Al Albedo electron test problem only!"

# Set the data directory path.
while getopts d: option
do case "${option}"
   in
       d) cross_section_directory=${OPTARG};;
   esac
done

epr="../../../bin/epr_generator"
if [ -d "$cross_section_directory" ]; then
    
    # Update Gold Log data
    printf "Updating the Al LinLog native test data...\n"
    $epr --cross_sec_dir=$cross_section_directory --cross_sec_alias=Al --min_photon_energy=1e-3 --max_photon_energy=20.0 --min_electron_energy=1e-5 --max_electron_energy=1e5 --occupation_num_tol=1e-3 --subshell_incoherent_tol=1e-3 --grid_convergence_tol=1e-3 --grid_absolute_diff_tol=1e-80 --grid_absolute_dist_tol=1e-18 --tabular_evaluation_tol=1e-15 --cutoff_angle_cosine=0.9 --number_of_moment_preserving_angles=2.0 --linlinlog_interp_on --modify_cs_xml_file --subdir="native" --output_alias="Native" --notes="$notes"
    if [ $? -eq 0 ]
    then
        printf "Au native lin-lin-log data updated successfully!\n\n"
    else
        printf "Au native lin-lin-log data FAILED to update!\n"
        exit 1
    fi
    
    # Update Gold Lin data
    printf "Updating the Al LinLin native test data...\n"
    $epr --cross_sec_dir=$cross_section_directory --cross_sec_alias=Al --min_photon_energy=1e-3 --max_photon_energy=20.0 --min_electron_energy=1e-5 --max_electron_energy=1e5 --occupation_num_tol=1e-3 --subshell_incoherent_tol=1e-3 --grid_convergence_tol=1e-3 --grid_absolute_diff_tol=1e-80 --grid_absolute_dist_tol=1e-18 --tabular_evaluation_tol=1e-15 --cutoff_angle_cosine=0.9 --number_of_moment_preserving_angles=2.0 --linlinlin_interp_on --modify_cs_xml_file --subdir="linlin" --output_alias="LinLin" --notes="$notes"
    if [ $? -eq 0 ]
    then
        printf "Au native lin-lin-lin data updated successfully!\n\n"
    else
        printf "Au native lin-lin-lin data FAILED to update!\n"
        exit 1
    fi
else
    printf "\nERROR: Invalid cross section directory!\n"
    printf "  update_test_files.sh -d cross_sectin_directory\n\n"
fi
