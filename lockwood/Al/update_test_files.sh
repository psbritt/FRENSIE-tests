#!/bin/bash
##---------------------------------------------------------------------------##
## Hanson test data updater
##---------------------------------------------------------------------------##

# Get the date for the table notes
today=`date`
notes="This table was generated on $today. It is for the Hanson electron test problem only!"

# Set the data directory path.
while getopts d: option
do case "${option}"
   in
       d) cross_section_directory=${OPTARG};;
   esac
done

epr="../../bin/epr_generator"
if [ -d "$cross_section_directory" ]; then

    if [ -d "$cross_section_directory/native" ]; then
        # Update Al LogLogLog data
        printf "Updating the Al LogLogLog native test data...\n"
        $epr --cross_sec_dir=$cross_section_directory --cross_sec_alias=Al --min_photon_energy=1e-3 --max_photon_energy=20.0 --min_electron_energy=1e-5 --max_electron_energy=1e5 --occupation_num_tol=1e-3 --subshell_incoherent_tol=1e-3 --grid_convergence_tol=1e-3 --grid_absolute_diff_tol=1e-80 --grid_absolute_dist_tol=1e-18 --tabular_evaluation_tol=1e-15 --cutoff_angle_cosine=0.9 --number_of_moment_preserving_angles=2.0 --electron_interp_policy="Log-Log-Log" --modify_cs_xml_file --subdir="native" --output_alias="Native" --notes="$notes"
        if [ $? -eq 0 ]; then
            printf "Al native log-log-log data updated successfully!\n\n"
        else
            printf "Al native log-log-log data FAILED to update!\n"
            exit 1
        fi
    else
        printf "\nERROR: Subdirectory $cross_section_directory/native/ does not exist!\n"
        printf "create the subdirectory before updating file!\n"
    fi
    if [ -d "$cross_section_directory/native/linlinlin" ]; then
    # Update Al LinLinLin data
        printf "Updating the Al LinLinLin native test data...\n"
        $epr --cross_sec_dir=$cross_section_directory --cross_sec_alias=Al --min_photon_energy=1e-3 --max_photon_energy=20.0 --min_electron_energy=1e-5 --max_electron_energy=1e5 --occupation_num_tol=1e-3 --subshell_incoherent_tol=1e-3 --grid_convergence_tol=1e-3 --grid_absolute_diff_tol=1e-80 --grid_absolute_dist_tol=1e-18 --tabular_evaluation_tol=1e-15 --cutoff_angle_cosine=0.9 --number_of_moment_preserving_angles=2.0 --electron_interp_policy="Lin-Lin-Lin" --modify_cs_xml_file --subdir="native/linlinlin" --output_alias="LinLinLin" --notes="$notes"
        if [ $? -eq 0 ]; then
            printf "Al native lin-lin-lin data updated successfully!\n\n"
        else
            printf "Al native lin-lin-lin data FAILED to update!\n"
            exit 1
        fi
    else
        printf "\nERROR: Subdirectory $cross_section_directory/native/linlinlin does not exist!\n"
        printf "create the subdirectory before updating file!\n"
    fi
    if [ -d "$cross_section_directory/native/linlinlog" ]; then
        # Update Al LinLinLog data
        printf "Updating the Al LinLinLog native test data...\n"
        $epr --cross_sec_dir=$cross_section_directory --cross_sec_alias=Al --min_photon_energy=1e-3 --max_photon_energy=20.0 --min_electron_energy=1e-5 --max_electron_energy=1e5 --occupation_num_tol=1e-3 --subshell_incoherent_tol=1e-3 --grid_convergence_tol=1e-3 --grid_absolute_diff_tol=1e-80 --grid_absolute_dist_tol=1e-18 --tabular_evaluation_tol=1e-15 --cutoff_angle_cosine=0.9 --number_of_moment_preserving_angles=2.0 --electron_interp_policy="Lin-Lin-Log" --modify_cs_xml_file --subdir="native/linlinlog" --output_alias="LinLinLog" --notes="$notes"
        if [ $? -eq 0 ]; then
            printf "Al native lin-lin-log data updated successfully!\n\n"
        else
            printf "Al native lin-lin-log data FAILED to update!\n"
            exit 1
        fi
    else
        printf "\nERROR: Subdirectory $cross_section_directory/native/linlinlog does not exist!\n"
        printf "create the subdirectory before updating file!\n"
    fi
else
    printf "\nERROR: Directory $cross_section_directory does not exist!\n"
    printf "  update_test_files.sh -d cross_sectin_directory\n\n"
fi

