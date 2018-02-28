#!/bin/bash
##---------------------------------------------------------------------------##
## MCNP6 test runner
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
EXTRA_ARGS=$@
MCNP6_1=/home/software/mcnp6.1.1/bin/mcnp611_linux_x86_64_omp
MCNP6_2=/home/software/mcnp6.2/bin/mcnp6
MCNP=$MCNP6_2
TODAY=$(date +%Y-%m-%d)
OUTPUT_DIR="./results/mcnp/${TODAY}/"

THREADS="8"
if [ "$#" -eq 1 ]; then
    # Set the number of threads used
    THREADS="$1"
fi

# Set the energy (0.314 0.521 1.033)
energy=0.314

# Set the range (the min range 0.0009 is left off because there is no front foil)

# ranges for 0.314 MeV source
# ( 0.0035 0.0067 0.0095 0.0124 0.0149 0.0177 0.0210 0.0242 0.0267 0.0300 0.0368 )

# ranges for 0.521 MeV source
# ( 0.0035 0.0067 0.0094 0.0124 0.0150 0.0176 0.0210 0.0242 0.0267 0.0299 0.0367 0.0412 0.0466 0.0533 0.0591 0.0676 0.0787 )

# ranges for 1.033 MeV source
# ( 0.0035 0.0067 0.0094 0.0125 0.0149 0.0176 0.0208 0.0242 0.0268 0.0299 0.0367 0.0411 0.0466 0.0533 0.0590 0.0674 0.0786 0.0824 0.0908 0.0934 0.1077 0.1163 0.1309 0.1551 0.1783 )

range=0.0035

# Set the input file name
NAME="mcnp.in"
OUTPUT="mcnp_${energy}_${range}."

mkdir -p $OUTPUT_DIR

# Change the energy
pattern="ERG=${energy} POS=0 0 0 DIR=1 VEC=0 0 1 PAR=e"
sed -i 's,ERG=.*,'"$pattern"',' "mcnp.in"

# Change the front foil thickness
half_cal=0.000935185
front_thickness=$(echo "${range} - ${half_cal}" | bc)
front_lower_z=$(echo "4.9 - ${front_thickness}" | bc)


pattern="204 PZ  ${front_lower_z}"
echo ${range}
echo ${front_thickness}
echo ${pattern}
sed -i 's,204 PZ.*,'"$pattern"',' "mcnp.in"

echo "Running MCNP6.2 with ${THREADS} threads:"
echo "${MCNP} i=${NAME} n=${OUTPUT} tasks ${THREADS}"
${MCNP} i=${NAME} n=${OUTPUT} tasks ${THREADS}

NEW_NAME=${OUTPUT_DIR}${OUTPUT}

# Move output files to test directory
mv ${OUTPUT}o ${NEW_NAME}o
mv ${OUTPUT}r ${NEW_NAME}r
mv ${OUTPUT}m ${NEW_NAME}m

# # Move to output directory
# cd ${OUTPUT_DIR}

# echo "Processing the results:"
# python ../../../mcnp_data_processor.py -d ./
# python ../../../convert_to_square_degrees.py -f ./mcnp_101.txt -o mcnp_spectrum.txt
# echo "The processed data is located at: ${OUTPUT_DIR}"
