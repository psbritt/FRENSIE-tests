1. run `export DATABASE_PATH=path-to-db`
2. run `./dyson_sphere.py --db_path=$DATABASE_PATH --sim_name="dyson_sphere" --num_particles=1e9 --thread=8`

# Phi = 0.15
3. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=1 --entity_id=1 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=1770 --mcnp_file_end=2768 --emin=0.0995 --emax=0.1 --top_ymax=3e-8 --bottom_ymin=0.60 --bottom_ymax=1.40 --legend_xpos=1.01 --legend_ypos=1.05`

4. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=2 --entity_id=1 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=40050 --mcnp_file_end=50030 --emin=0.09955 --emax=0.1 --top_ymax=4e-8 --bottom_ymin=0.60 --bottom_ymax=1.40 --legend_xpos=1.01 --legend_ypos=1.05`

# Phi = Pi/12
5. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=1 --entity_id=2 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=4785 --mcnp_file_end=5783 --emin=0.0988 --emax=0.1 --top_ymax=2e-8 --bottom_ymin=0.9 --bottom_ymax=1.1 --legend_xpos=1.01 --legend_ypos=1.05`

6. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=2 --entity_id=2 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=50036 --mcnp_file_end=60016 --emin=0.0988 --emax=0.1 --top_ymax=2.5e-8 --bottom_ymin=0.6 --bottom_ymax=1.4 --legend_xpos=1.01 --legend_ypos=1.05`

# Phi = Pi/6
7. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=1 --entity_id=3 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=7800 --mcnp_file_end=8798 --emin=0.096 --emax=0.099 --top_ymax=1e-8 --bottom_ymin=0.6 --bottom_ymax=1.4 --legend_xpos=1.01 --legend_ypos=1.05`

8. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=2 --entity_id=3 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=60022 --mcnp_file_end=70002 --emin=0.096 --emax=0.099 --top_ymax=1e-8 --bottom_ymin=0.6 --bottom_ymax=1.4 --legend_xpos=1.01 --legend_ypos=1.05`

# Phi = Pi/4
9. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=1 --entity_id=4 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=10815 --mcnp_file_end=11813 --emin=0.093 --emax=0.096 --top_ymax=6e-9 --bottom_ymin=0.6 --bottom_ymax=1.4 --legend_xpos=1.01 --legend_ypos=1.05`

10. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=2 --entity_id=4 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=70008 --mcnp_file_end=79988 --emin=0.093 --emax=0.096 --top_ymax=6e-9 --bottom_ymin=0.6 --bottom_ymax=1.4 --legend_xpos=1.01 --legend_ypos=1.05`

# Phi = Pi/3
11. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=1 --entity_id=5 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=12825 --mcnp_file_end=13823 --emin=0.0895 --emax=0.0925 --top_ymax=4e-9 --bottom_ymin=0.6 --bottom_ymax=1.4 --legend_xpos=1.01 --legend_ypos=1.05`

12. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=2 --entity_id=5 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=79994 --mcnp_file_end=89974 --emin=0.0895 --emax=0.0925 --top_ymax=4e-9 --bottom_ymin=0.6 --bottom_ymax=1.4 --legend_xpos=1.01 --legend_ypos=1.05`

# Phi = 5Pi/12
13. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=1 --entity_id=6 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=13830 --mcnp_file_end=14828 --emin=0.0855 --emax=0.089 --top_ymax=2.5e-9 --bottom_ymin=0.6 --bottom_ymax=1.4 --legend_xpos=1.01 --legend_ypos=1.05`

14. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=2 --entity_id=6 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=89980 --mcnp_file_end=99960 --emin=0.0855 --emax=0.089 --top_ymax=2.5e-9 --bottom_ymin=0.6 --bottom_ymax=1.4 --legend_xpos=1.01 --legend_ypos=1.05`

# Phi = Pi/2
15. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=1 --entity_id=7 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=16845 --mcnp_file_end=17843 --emin=0.0855 --emax=0.089 --top_ymax=2.5e-9 --bottom_ymin=0.6 --bottom_ymax=1.4 --legend_xpos=1.01 --legend_ypos=1.05`

16. run `../dyson_sphere-plot.py --rendezvous_file="dyson_sphere_rendezvous_10.xml" --estimator_id=2 --entity_id=7 --mcnp_file=../dyson_sphere_mcnp.o --mcnp_file_start=99966 --mcnp_file_end=109946 --emin=0.0855 --emax=0.089 x--top_ymax=2.5e-9 --bottom_ymin=0.6 --bottom_ymax=1.4 --legend_xpos=1.01 --legend_ypos=1.05`

# Phi = 7Pi/12

# Phi = 2Pi/3

# Phi = 3Pi/4

# Phi = 5Pi/6

# Phi = 11Pi/12

# Phi = Pi - 0.15

# ../dyson_sphere_restart.py --db_path=$DATABASE_PATH --rendezvous_file="dyson_sphere_rendezvous_10.xml" --num_particles=1e9 --threads=8