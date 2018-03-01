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

# Set the range (the min range 0.0025 is left off because there is no front foil)

# ranges for 0.314 MeV source (g/cm2)
# ( 0.0094 0.0181 0.0255 0.0336 0.0403 0.0477 0.0566 0.0654 0.0721 0.0810 0.0993 )

# ranges for 0.521 MeV source (g/cm2)
# ( 0.0094 0.0180 0.0255 0.0335 0.0405 0.0475 0.0566 0.0653 0.0721 0.0807 0.0992 0.1111 0.1259 0.1439 0.1596 0.1825 0.2125 )

# ranges for 1.033 MeV source (g/cm2)
# ( 0.0094 0.0180 0.0255 0.0336 0.0402 0.0476 0.0562 0.0654 0.0723 0.0808 0.0990 0.1110 0.1257 0.1440 0.1593 0.1821 0.2122 0.2225 0.2452 0.2521 0.2908 0.3141 0.3533 0.4188 0.4814 )

# range in g/cm^2
range=0.0094
# density in g/cm^3
density=2.7
range_cm=$(echo "${range}/${density}" | bc)

# Set the input file name
NAME="mcnp.in"
OUTPUT="mcnp_${energy}_${range}."

mkdir -p $OUTPUT_DIR

# Change the energy
pattern="ERG=${energy} POS=0 0 0 DIR=1 VEC=0 0 1 PAR=e"
sed -i 's,ERG=.*,'"$pattern"',' "mcnp.in"

# Change the front foil thickness
half_cal=0.000935185
front_thickness=$(echo "${range_cm} - ${half_cal}" | bc)
front_lower_z=$(echo "4.9 - ${front_thickness}" | bc)


pattern="204 PZ  ${front_lower_z}"
sed -i 's,204 PZ.*,'"$pattern"',' "mcnp.in"

echo "Running MCNP6.2 with ${THREADS} threads:"
echo "${MCNP} i=${NAME} n=${OUTPUT} tasks ${THREADS}"
${MCNP} i=${NAME} n=${OUTPUT} tasks ${THREADS}

NEW_NAME=${OUTPUT_DIR}${OUTPUT}

# Move output files to test directory
mv ${OUTPUT}o ${NEW_NAME}o
mv ${OUTPUT}r ${NEW_NAME}r
mv ${OUTPUT}m ${NEW_NAME}m

# Move to output directory=
cd ${OUTPUT_DIR}

echo "Processing the results:"
python ../../../mcnp_data_processor.py -f ${OUTPUT}o -r ${range}
echo "The processed data is located at: ${OUTPUT_DIR}"
