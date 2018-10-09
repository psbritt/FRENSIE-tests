#!/bin/bash
##---------------------------------------------------------------------------##
## Create ROOT geometries for the Al lockwood energy deposition tests.
##---------------------------------------------------------------------------##

# Set cross_section.xml directory path.
# EXTRA_ARGS=$@

# Set the energy (0.314 0.521 1.033)
energy=1.033

# Get the range (g/cm2)
if [ ${energy} == 0.314 ]; then
    # ranges for 0.314 MeV source (g/cm2)
    ranges=( 0.0025 0.0094 0.0181 0.0255 0.0336 0.0403 0.0477 0.0566 0.0654 0.0721 0.0810 0.0993 )
elif [ ${energy} == 0.521 ]; then
    # ranges for 0.521 MeV source (g/cm2)
    ranges=( 0.0025 0.0094 0.0180 0.0255 0.0335 0.0405 0.0475 0.0566 0.0653 0.0721 0.0807 0.0992 0.1111 0.1259 0.1439 0.1596 0.1825 0.2125 )
elif [ ${energy} == 1.033 ]; then
    # ranges for 1.033 MeV source (g/cm2)
    ranges=( 0.0025 0.0094 0.0180 0.0255 0.0336 0.0402 0.0476 0.0562 0.0654 0.0723 0.0808 0.0990 0.1110 0.1257 0.1440 0.1593 0.1821 0.2122 0.2225 0.2452 0.2521 0.2908 0.3141 0.3533 0.4188 0.4814 )
fi

# Get the output directory
OUTPUT_DIR="./Al_${energy}/root/"
mkdir -p ${OUTPUT_DIR}

# loop through ranges and create the ROOT geometry
for i in `seq 0 $((${#ranges[@]}-1))`;
do
    printf "\n\n---------------------------------------------------------------\n"
    printf "Creating the geometry for Al test #${i} at an energy of ${energy} MeV!\n"

    # Change the range
    pattern="range = ${ranges[${i}]};"
    sed -i 's,range =.*,'"$pattern"',' "geom_Al.c"
    printf "Range has been set to ${ranges[${i}]} g/cm2!\n"

    # Create the geometry
    root geom_Al.c

    # Set the output file name
    NAME="geom_${i}.root"
    OUTPUT="${OUTPUT_DIR}${NAME}"

    # Move the geometry
    echo "Geometry is located at ${OUTPUT}!"
    mv geom_Al.root ${OUTPUT}

done