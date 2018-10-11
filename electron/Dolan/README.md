## Dolan photo-emission experiment ##

# Experimental
50 keV photon spectrum on tantalum for a reflected energy spectrum of electron
escape.

# Setup
For the photon spectrum, use:
   1.0000E+00
   1.0000E+00  9.9991E-01  9.9955E-01  9.9297E-01  9.7635E-01
   9.5163E-01  9.2031E-01  8.8227E-01  8.3924E-01  7.9210E-01
   7.4036E-01  6.8591E-01  6.2916E-01  5.7102E-01  5.1217E-01
   4.5302E-01  3.9497E-01  3.3892E-01  2.8548E-01  2.3594E-01
   1.9070E-01  1.5057E-01  1.1554E-01  8.6612E-02  6.3193E-02
   4.5178E-02  3.1867E-02  2.2629E-02  1.6123E-02  1.1790E-02
   8.6272E-03  6.2952E-03  4.3536E-03  2.6622E-03  1.2510E-03
   0.0000E+00

   5.0000E-02
   4.8000E-02  4.7000E-02  4.6000E-02  4.5000E-02  4.4000E-02
   4.3000E-02  4.2000E-02  4.1000E-02  4.0000E-02  3.9000E-02
   3.8000E-02  3.7000E-02  3.6000E-02  3.5000E-02  3.4000E-02
   3.3000E-02  3.2000E-02  3.1000E-02  3.0000E-02  2.9000E-02
   2.8000E-02  2.7000E-02  2.6000E-02  2.5000E-02  2.4000E-02
   2.3000E-02  2.2000E-02  2.1000E-02  2.0000E-02  1.9000E-02
   1.8000E-02  1.7000E-02  1.6000E-02  1.5000E-02  1.4000E-02
   1.3000E-02

The first portion is a complementary cumulative distribution function, with the
corresponding energy points (in MeV) in the second portion.
The CDF is in terms of number of photons.
(The first bin from 50 keV down to 48 keV has CDF points of 1.0 and 1.0,
indicating that there is no source in this energy range, but it helped trick ITS
into thinking the energy goes up to 50 keV to get energy binning up to that
energy for comparison with the experimental results.)

Tally the escaping electrons in 50 equal energy bins from 50 keV down to 0 keV.

# Running the simulation if FRENSIE

# Running the simulation if MCNP6.2

# Plotting results