# Efficiency Data Generation
1. run `./evaluate_efficiency.py --db_path=$DATABASE_PATH --atomic_number=1 --model_type=kn --samples_per_point=100000 --num_energies=1000 --max_energy=0.1`
2. run `./evaluate_efficiency.py --db_path=$DATABASE_PATH --atomic_number=1 --model_type=wh --samples_per_point=100000 --num_energies=1000 --max_energy=0.1`
3. run `./evaluate_efficiency.py --db_path=$DATABASE_PATH --atomic_number=1 --model_type=kn --samples_per_point=100000 --num_energies=1000 --max_energy=1.0`
4. run `./evaluate_efficiency.py --db_path=$DATABASE_PATH --atomic_number=1 --model_type=wh --samples_per_point=100000 --num_energies=1000 --max_energy=1.0`
5. run `./evaluate_efficiency.py --db_path=$DATABASE_PATH --atomic_number=1 --model_type=kn --samples_per_point=100000 --num_energies=1000 --max_energy=10.0`
6. run `./evaluate_efficiency.py --db_path=$DATABASE_PATH --atomic_number=1 --model_type=wh --samples_per_point=100000 --num_energies=1000 --max_energy=10.0`

# Efficiency Plots
1. run `./plot_efficiency.py --file=1-kn-0.1.txt --eff_min=0.5 --rate_min=300000 --rate_max=600000 --legend_x=1.06 --legend_y=-0.05`
2. run `./plot_efficiency.py --file=1-wh-0.1.txt --eff_min=0.3 --rate_min=120000 --rate_max=200000 --legend_x=1.06 --legend_y=-0.05`
3. run `./plot_efficiency.py --file=1-kn-1.0.txt --eff_min=0.2 --rate_min=300000 --rate_max=500000 --legend_x=1.06 --legend_y=-0.05`
4. run `./plot_efficiency.py --file=1-wh-1.0.txt --eff_min=0.2 --rate_min=120000 --rate_max=200000 --legend_x=1.06 --legend_y=-0.05`
5. run `./plot_efficiency.py --file=1-kn-10.0.txt --eff_min=0.0 --rate_min=200000 --rate_max=600000 --legend_x=1.06 --legend_y=-0.05`
6. run `./plot_efficiency.py --file=1-wh-10.0.txt --eff_min=0.0 --rate_min=120000 --rate_max=200000 --legend_x=1.06 --legend_y=-0.05`