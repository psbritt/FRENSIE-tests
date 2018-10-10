#!/bin/bash
##---------------------------------------------------------------------------##
## Hanson test data updater
##---------------------------------------------------------------------------##

# Set the database directory path.
while getopts d: option
do case "${option}"
   in
       d) database_directory=${OPTARG};;
   esac
done

epr="../../../bin/generate_native_epr.py"
if [ -d "$database_directory" ]; then

    # Update H Log data
    printf "Updating the Au LogLogLog native test data...\n"
    $epr --db_name="$database_directory/database.xml" --zaid=79000 --version=0
    if [ $? -eq 0 ]; then
        printf "Au native data updated successfully!\n\n"
    else
        printf "AU native data FAILED to update!\n"
        exit 1
    fi
else
    printf "\nERROR: Invalid cross section directory!\n"
    printf "  update_test_files.sh -d cross_sectin_directory\n\n"
fi