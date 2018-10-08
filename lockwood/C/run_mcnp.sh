#!/bin/bash
##---------------------------------------------------------------------------##
## MCNP6 test runner
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.1
EXTRA_ARGS=$@
MCNP6_1=/home/software/mcnp6.1.1/bin/mcnp611_linux_x86_64_omp
MCNP6_2=/home/software/mcnp6.2/MCNP_CODE/bin/mcnp6
MCNP=$MCNP6_2
TODAY=$(date +%Y-%m-%d)
OUTPUT_DIR="./results/mcnp/${TODAY}/"

THREADS="8"
if [ "$#" -eq 1 ]; then
    # Set the number of threads used
    THREADS="$1"
fi

# Set the energy ( 1 MeV )
energy=1
# Set the test number (0 to N where N_1=9)
test_number="0"

if [ ${energy} == 1 ]; then
    # ranges for 1.0 MeV source (g/cm2)
    ranges=( 0.007805 0.060883 0.112662 0.164441 0.215082 0.268568 0.323192 0.382937 0.444389 0.502427 )
    # Front plate z_0 for 0.314 MeV source (cm)
    z_locations=( 4.9 4.87051222222222 4.84174611111111 4.81298 4.78484611111111 4.75513166666667 4.724785 4.69159333333333 4.65745333333333 4.62521 )
else
    echo "Error: Energy (${energy} MeV) is currently not supported!"
fi

# The z_0 location of the front foil
z_0=z_locations[test_number]

# Set the input file name
if [ ${test_number} == 0 ]; then
    NAME="mcnp_no_foil.in"
else
    NAME="mcnp.in"

    # Change the front foil thickness
    front_lower_z=${z_locations[${test_number}]}
    # pattern="200 RPP -4.445 4.445 -4.445 4.445 ${front_lower_z} 4.9"
    pattern="204 PZ  ${front_lower_z}"
    sed -i 's,204 PZ.*,'"$pattern"',' "$NAME"
fi

OUTPUT="mcnp_${energy}_${test_number}."

mkdir -p $OUTPUT_DIR

# Change the energy
pattern="ERG=${energy} POS=0 0 0 DIR=1 VEC=0 0 1 PAR=e"
sed -i 's,ERG=.*,'"$pattern"',' "$NAME"

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
calorimeter_thickness=1.561E-02
python ../../../../mcnp_data_processor.py -f ${OUTPUT}o -r ${ranges[${test_number}]} -t ${calorimeter_thickness}
echo "The processed data is located at: ${OUTPUT_DIR}"
