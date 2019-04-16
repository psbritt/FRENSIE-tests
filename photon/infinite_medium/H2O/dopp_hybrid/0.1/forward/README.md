1. run `mcnp6 i=infinite_medium_mcnp.i o=infinite_medium_mcnp.o tasks 8`
2. run `export DATABASE_PATH=path-to-db`
3. run `./infinite_medium.py --db_path=$DATABASE_PATH --sim_name="infinite_medium" --num_particles=1e8 --threads=8`
4. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous.xml" --estimator_id=1 --entity_id=1 --mcnp_file=infinite_medium_mcnp.o --mcnp_file_start=280 --mcnp_file_end=1278 --flux --forward`
5. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous.xml" --estimator_id=1 --entity_id=3 --mcnp_file=infinite_medium_mcnp.o --mcnp_file_start=1284 --mcnp_file_end=2282 --flux --forward`
6. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous.xml" --estimator_id=1 --entity_id=6 --mcnp_file=infinite_medium_mcnp.o --mcnp_file_start=2288 --mcnp_file_end=3286 --flux --forward`
7. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous.xml" --estimator_id=1 --entity_id=9 --mcnp_file=infinite_medium_mcnp.o --mcnp_file_start=3292 --mcnp_file_end=4290 --flux --forward`
8. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous.xml" --estimator_id=1 --entity_id=12 --mcnp_file=infinite_medium_mcnp.o --mcnp_file_start=4296 --mcnp_file_end=5294 --flux --forward`
[H Infinite Medium](h_infinite_medium_current.png "H Infinite Medium")