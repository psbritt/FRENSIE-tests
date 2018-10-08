1. run `mcnp6 i=sphere_mcnp.inp o=sphere_mcnp.out tasks 8`
2. run `./sphere.py --db_path=/home/alexr/Software/mcnpdata/database.xml --sim_name="sphere" --num_particles=1e6 --threads=8`
3. run `./sphere-plot.py --rendezvous_file="sphere_rendezvous_10.xml" --estimator_id=1 --entity_id=1 --mcnp_file=sphere_mcnp.out --mcnp_file_start=242 --mcnp_file_end=342 --current`
![H1 Sphere @ 293.6K](h1_sphere_current.png)
run `./sphere-plot.py --rendezvous_file="sphere_rendezvous_10.xml" --estimator_id=2 --entity_id=1 --mcnp_file=sphere_mcnp.out --mcnp_file_start=408 --mcnp_file_end=508 --flux`
![H1 Sphere @ 293.6K](h1_sphere_flux.png)