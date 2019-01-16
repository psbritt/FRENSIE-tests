1. run `export DATABASE_PATH=path-to-db`
2. run `./infinite_medium.py --db_path=$DATABASE_PATH --sim_name="infinite_medium" --num_particles=1e8 --threads=8`

3. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous_10.xml" --estimator_id=1 --entity_id=1 --col_bin=1 --mcnp_file=../infinite_medium_mcnp.o --mcnp_file_start=1284 --mcnp_file_end=2282 --flux --adjoint`
4. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous_10.xml" --estimator_id=1 --entity_id=1 --col_bin=2 --mcnp_file=../infinite_medium_mcnp.o --mcnp_file_start=2289 --mcnp_file_end=3287 --flux --adjoint`
5. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous_10.xml" --estimator_id=1 --entity_id=1 --col_bin=3 --mcnp_file=../infinite_medium_mcnp.o --mcnp_file_start=3294 --mcnp_file_end=4292 --flux --adjoint`
6. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous_10.xml" --estimator_id=1 --entity_id=1 --col_bin=4 --mcnp_file=../infinite_medium_mcnp.o --mcnp_file_start=4299 --mcnp_file_end=5297 --flux --adjoint`
7. run `./infinite_medium-plot.py --rendezvous_file="infinite_medium_rendezvous_10.xml" --estimator_id=1 --entity_id=1 --col_bin=5 --mcnp_file=../infinite_medium_mcnp.o --mcnp_file_start=5304 --mcnp_file_end=6302 --flux --adjoint`

