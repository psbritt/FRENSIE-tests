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
energy=0.521
# Set the test number (1 to N where N_0.314 = 11, N_0.521 = 17, N_1.033 = 25)
test_number="11"

if [ ${energy} == 0.314 ]; then
    # ranges for 0.314 MeV source (g/cm2)
    ranges=( 0.0025 0.0094 0.0181 0.0255 0.0336 0.0403 0.0477 0.0566 0.0654 0.0721 0.0810 0.0993 )
    # Front plate z_0 for 0.314 MeV source (cm)
    z_locations=( 4.9 4.89745370370370 4.89423148148148 4.89149074074074 4.88849074074074 4.88600925925926 4.88326851851852 4.87997222222222 4.87671296296296 4.87423148148148 4.87093518518519 4.86415740740741 )
elif [ ${energy} == 0.521 ]; then
    # ranges for 0.521 MeV source (g/cm2)
    ranges=( 0.0025 0.0094 0.0180 0.0255 0.0335 0.0405 0.0475 0.0566 0.0653 0.0721 0.0807 0.0992 0.1111 0.1259 0.1439 0.1596 0.1825 0.2125 )
    # Front plate z_0 for 0.521 MeV source (cm)
    z_locations=( 4.9 4.89745370370370 4.89426851851852 4.89149074074074 4.88852777777778 4.88593518518519 4.88334259259259 4.87997222222222 4.87675000000000 4.87423148148148 4.87104629629630 4.86419444444445 4.85978703703704 4.85430555555556 4.84763888888889 4.84182407407408 4.83334259259259 4.82223148148148 )
elif [ ${energy} == 1.033 ]; then
    # ranges for 1.033 MeV source (g/cm2)
    ranges=( 0.0025 0.0094 0.0180 0.0255 0.0336 0.0402 0.0476 0.0562 0.0654 0.0723 0.0808 0.0990 0.1110 0.1257 0.1440 0.1593 0.1821 0.2122 0.2225 0.2452 0.2521 0.2908 0.3141 0.3533 0.4188 0.4814 )
    # Front plate z_0 for 1.033 MeV source (cm)
    z_locations=( 4.9 4.89745370370370 4.89426851851852 4.89149074074074 4.88849074074074 4.88604629629630 4.88330555555556 4.88012037037037 4.87671296296296 4.87415740740741 4.87100925925926 4.86426851851852 4.85982407407408 4.85437962962963 4.84760185185185 4.84193518518519 4.83349074074074 4.82234259259259 4.81852777777778 4.81012037037037 4.80756481481482 4.79323148148148 4.78460185185185 4.77008333333333 4.74582407407408 4.72263888888889 )
else
    echo "Error: Energy (MeV) \"${energy}\" is currently not supported!"
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
    pattern="200 RPP -4.445 4.445 -4.445 4.445 ${front_lower_z} 4.9"
    sed -i 's,200 RPP.*,'"$pattern"',' "$NAME"
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
calorimeter_thickness=5.050E-03
python ../../../../mcnp_data_processor.py -f ${OUTPUT}o -r ${ranges[${test_number}]} -t ${calorimeter_thickness}
echo "The processed data is located at: ${OUTPUT_DIR}"
