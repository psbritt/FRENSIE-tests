#!/bin/bash
# This file is update_adjoint_test_files.sh
#SBATCH --partition=pre
#SBATCH --time=1-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=4000

##---------------------------------------------------------------------------##
## Adjoint test adjoint data updater
##---------------------------------------------------------------------------##

# Get the date for the table notes
today=`date`
notes="This table was generated on $today. It is for the adjoint electron test problem only!"

# Set the data directory path.
while getopts d: option
do case "${option}"
   in
       d) cross_section_directory=${OPTARG};;
   esac
done

aepr="../../bin/aepr_generator"
if [ -d "$cross_section_directory" ]; then

    if [ -d "$cross_section_directory/native" ]; then
        # Update Hydrogen LogLogLog data
        printf "Updating the H LogLogLog native test data...\n"
        $aepr --cross_sec_dir=$cross_section_directory --cross_sec_alias=H-Native --min_photon_energy=1e-3 --max_photon_energy=20.0 --min_electron_energy=1e-5 --max_electron_energy=20 --data_generated=electron --cutoff_angle_cosine=0.9 --number_of_moment_preserving_angles=2 --electron_tabular_evaluation_tol=1e-6 --electron_correlated_sampling --electron_unit_based_interp --adjoint_electron_grid_convergence_tol=1e-3 --adjoint_electron_grid_absolute_diff_tol=1e-16 --adjoint_electron_dist_tol=1e-9 --adjoint_bremsstrahlung_max_e_nudge_val=0.2 --adjoint_bremsstrahlung_e_to_outgoing_e_nudge_val=2e-7 --adjoint_bremsstrahlung_eval_tol=1e-4 --adjoint_bremsstrahlung_grid_convergence_tol=1e-2 --adjoint_bremsstrahlung_grid_absolute_diff_tol=1e-16 --adjoint_bremsstrahlung_dist_tol=1e-9 --adjoint_electroionization_eval_tol=1e-4 --adjoint_electroionization_grid_convergence_tol=1e-2 --adjoint_electroionization_grid_absolute_diff_tol=1e-16 --adjoint_electroionization_dist_tol=1e-9 --grid_convergence_tol=1e-3 --grid_absolute_diff_tol=1e-42 --grid_absolute_dist_tol=1e-16 --modify_cs_xml_file --subdir="native" --notes="$notes"
        if [ $? -eq 0 ]
        then
            printf "H adjoint log-log-log data updated successfully!\n\n"
        else
            printf "H adjoint log-log-log data FAILED to update!\n"
            exit 1
        fi
    else
        printf "\nERROR: Subdirectory $cross_section_directory/native/ does not exist!\n"
        printf "create the subdirectory before updating file!\n"
    fi
    # if [ -d "$cross_section_directory/native/linlinlin" ]; then
    # # Update Hydrogen LinLinLin data
    #     printf "Updating the H LinLinLin native test data...\n"
    #     $aepr --cross_sec_dir=$cross_section_directory --cross_sec_alias=H-LinLinLin --min_photon_energy=1e-3 --max_photon_energy=20.0 --min_electron_energy=1e-5 --max_electron_energy=20 --adjoint_pp_edist_eval_tol=1e-1 --adjoint_pp_edist_nudge_val=1e-6 --adjoint_tp_edist_eval_tol=1e-1 --adjoint_tp_edist_nudge_val=1e-6 --adjoint_incoherent_max_e_nudge_val=0.2 --adjoint_incoherent_e_to_max_e_nudge_val=1e-5 --adjoint_incoherent_eval_tol=1e-1 --adjoint_incoherent_grid_convergence_tol=0.9 --adjoint_incoherent_grid_absolute_diff_tol=1e-42 --adjoint_incoherent_grid_dist_tol=1e-16 --cutoff_angle_cosine=0.9 --number_of_moment_preserving_angles=2 --electron_tabular_evaluation_tol=1e-5 --electron_correlated_sampling --electron_unit_based_interp --adjoint_electron_grid_convergence_tol=1e-3 --adjoint_electron_grid_absolute_diff_tol=1e-16 --adjoint_electron_dist_tol=1e-9 --adjoint_bremsstrahlung_max_e_nudge_val=0.2 --adjoint_bremsstrahlung_e_to_outgoing_e_nudge_val=2e-7 --adjoint_bremsstrahlung_eval_tol=1e-6 --adjoint_bremsstrahlung_grid_convergence_tol=1e-2 --adjoint_bremsstrahlung_grid_absolute_diff_tol=1e-16 --adjoint_bremsstrahlung_dist_tol=1e-9 --adjoint_electroionization_eval_tol=1e-6 --adjoint_electroionization_grid_convergence_tol=1e-2 --adjoint_electroionization_grid_absolute_diff_tol=1e-16 --adjoint_electroionization_dist_tol=1e-9 --grid_convergence_tol=1e-5 --grid_absolute_diff_tol=1e-42 --grid_absolute_dist_tol=1e-16 --modify_cs_xml_file --subdir="native/linlinlin" --output_alias="LinLinLin" --notes="$notes"
    #     if [ $? -eq 0 ]
    #     then
    #         printf "H adjoint lin-lin-lin data updated successfully!\n\n"
    #     else
    #         printf "H adjoint lin-lin-lin data FAILED to update!\n"
    #         exit 1
    #     fi
    # else
    #     printf "\nERROR: Subdirectory $cross_section_directory/native/linlinlin does not exist!\n"
    #     printf "create the subdirectory before updating file!\n"
    # fi
    # if [ -d "$cross_section_directory/native/linlinlog" ]; then
    #     # Update Hydrogen LinLinLog data
    #     printf "Updating the H LinLinLog native test data...\n"
    #     $aepr --cross_sec_dir=$cross_section_directory --cross_sec_alias=H-LinLinLog --min_photon_energy=1e-3 --max_photon_energy=20.0 --min_electron_energy=1e-5 --max_electron_energy=20 --adjoint_pp_edist_eval_tol=1e-1 --adjoint_pp_edist_nudge_val=1e-6 --adjoint_tp_edist_eval_tol=1e-1 --adjoint_tp_edist_nudge_val=1e-6 --adjoint_incoherent_max_e_nudge_val=0.2 --adjoint_incoherent_e_to_max_e_nudge_val=1e-5 --adjoint_incoherent_eval_tol=1e-1 --adjoint_incoherent_grid_convergence_tol=0.9 --adjoint_incoherent_grid_absolute_diff_tol=1e-42 --adjoint_incoherent_grid_dist_tol=1e-16 --cutoff_angle_cosine=0.9 --number_of_moment_preserving_angles=2 --electron_tabular_evaluation_tol=1e-5 --electron_correlated_sampling --electron_unit_based_interp --adjoint_electron_grid_convergence_tol=1e-3 --adjoint_electron_grid_absolute_diff_tol=1e-16 --adjoint_electron_dist_tol=1e-9 --adjoint_bremsstrahlung_max_e_nudge_val=0.2 --adjoint_bremsstrahlung_e_to_outgoing_e_nudge_val=2e-7 --adjoint_bremsstrahlung_eval_tol=1e-6 --adjoint_bremsstrahlung_grid_convergence_tol=1e-2 --adjoint_bremsstrahlung_grid_absolute_diff_tol=1e-16 --adjoint_bremsstrahlung_dist_tol=1e-9 --adjoint_electroionization_eval_tol=1e-6 --adjoint_electroionization_grid_convergence_tol=1e-2 --adjoint_electroionization_grid_absolute_diff_tol=1e-16 --adjoint_electroionization_dist_tol=1e-9 --grid_convergence_tol=1e-5 --grid_absolute_diff_tol=1e-42 --grid_absolute_dist_tol=1e-16 --modify_cs_xml_file --subdir="native/linlinlog" --output_alias="LinLinLog" --notes="$notes"
    #     if [ $? -eq 0 ]
    #     then
    #         printf "H adjoint lin-lin-log data updated successfully!\n\n"
    #     else
    #         printf "H adjoint lin-lin-log data FAILED to update!\n"
    #         exit 1
    #     fi
    # else
    #     printf "\nERROR: Subdirectory $cross_section_directory/native/linlinlog does not exist!\n"
    #     printf "create the subdirectory before updating file!\n"
    # fi
else
    printf "\nERROR: Directory $cross_section_directory does not exist!\n"
    printf "  update_test_files.sh -d cross_sectin_directory\n\n"
fi

