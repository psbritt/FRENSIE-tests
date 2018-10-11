## Hanson 15.7 MeV electron multiple scattering spectrum in Au ##

# Experimental
Hanson et al. measured the fractional scattering of 15.7 MeV electron per square degree from a thin gold foil of 9.658 micrometers thickness.
Ref: ``Measurement of Multiple Scattering of 15.7-MeV Electrons'' Hanson et al. Physical Review, Volume 84, Number 4 November 15, 1951

# Setup
15.7 MeV delta source of electrons are normally incident on a 9.658 micrometers film of Au. The surface current of the exiting surface is measured at several cosine bins. The current is then converted to units of fractional scattering per square degree.
Cosine bins (degrees): 0.0 0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0 5.5 6.0 8.0 10.0 15.0 20.0 90.0 180.0

# Running the simulation if FRENSIE

Set the desired physics option at the top of hanson.py.
Set the run parameters ( for FRENSIE and SBATCH ) on hanson.sh.
run `sbatch hanson.sh` on the UW-Cluster.
Use scp to copy the rendezvous and spectrum files from the results directory on the UW-Cluster to a local computer.

# Running the simulation if MCNP6.2

Set the path to mcnp6.2 in the run_mcnp.sh script.
run `run_mcnp.sh N` where N is the desired number of cores.

# Plotting results
run `hist_plot_results_all_in_one.py -e -o hanson_results.pdf path-to-frensie-spectrum1.txt path-to-frensie-spectrum2.txt`
run `hist_plot_results_all_in_one.py -m -o hanson_results.pdf path-to-mcnp6.2-spectrum.txt path-to-frensie-spectrum1.txt path-to-frensie-spectrum2.txt`
The `-e` flag will plots the designated frensie results against experimental results.
The `-m` flag will plots the designated frensie results against mcnp results.
The `-o` flag can be use to designate the name of the output file.
Multiple frensie spectrums can be designated when plotting.