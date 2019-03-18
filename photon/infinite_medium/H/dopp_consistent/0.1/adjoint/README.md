1. run `export DATABASE_PATH=path-to-db`
2. run `./infinite_medium.py --db_path=$DATABASE_PATH --sim_name="infinite_medium" --num_particles=1e8 --threads=8`
3. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous_10.xml" --estimator_id=1 --entity_id=1 --mcnp_file=../infinite_medium_mcnp.o --mcnp_file_start=281 --mcnp_file_end=1279 --flux --adjoint`
4. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous_10.xml" --estimator_id=1 --entity_id=3 --mcnp_file=../infinite_medium_mcnp.o --mcnp_file_start=1285 --mcnp_file_end=2283 --flux --adjoint`
5. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous_10.xml" --estimator_id=1 --entity_id=6 --mcnp_file=../infinite_medium_mcnp.o --mcnp_file_start=2289 --mcnp_file_end=3287 --flux --adjoint`
6. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous_10.xml" --estimator_id=1 --entity_id=9 --mcnp_file=../infinite_medium_mcnp.o --mcnp_file_start=3293 --mcnp_file_end=4291 --flux --adjoint`
7. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous_10.xml" --estimator_id=1 --entity_id=12 --mcnp_file=../infinite_medium_mcnp.o --mcnp_file_start=4297 --mcnp_file_end=5295 --flux --adjoint`
8. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous_10.xml" --estimator_id=1 --entity_id=15 --mcnp_file=../infinite_medium_mcnp.o --mcnp_file_start=5301 --mcnp_file_end=6299 --flux --adjoint`
