## Self Adjoint H Sphere Test ##

# Forward Setup
H sphere of radius 0.02 cm surrounded by a void.
0.01 MeV isotropic delta source at the center of the sphere.
Measure flux and current on the surface of the sphere and the track flux in the sphere. Set energy bins for all estimators

# Adjoint Setup
H sphere of radius 0.02 cm surrounded by a void.
cutoff energy to 0.01 MeV isotropic uniform source at the center of the sphere.
Measure adjoint flux and current on the surface of the sphere and the adjoint track flux in the sphere. Set source energy bins for all estimators. Set a delta distribution at the forward source energy as a response function.

# Trelis geometry commands
sphere r 0.02
brick x 0.1 y 0.1 z 0.1
brick x 0.2 y 0.2 z 0.2
subtract volume 2 from volume 3

imprint body all
merge tol 5e-7
merge all
group "termination.cell" add vol 4
group "material_1_density_0.005" add vol 1
group "estimator_1.cell.tl.flux.e" add vol 1
group "estimator_2.surface.flux.e" add surface 1
group "estimator_3.surface.current.e" add surface 1
group "estimator_4.cell.tl.flux.e*" add vol 1
group "estimator_5.surface.flux.e*" add surface 1
group "estimator_6.surface.current.e*" add surface 1
export dagmc "path-to-frensie-tests/self_adjoint/geom.h5m" faceting_tolerance 1.e-5 make_watertight

# Running the simulation if FRENSIE

# Running the simulation if MCNP6.2

# Plotting results