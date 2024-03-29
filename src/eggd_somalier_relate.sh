#!/bin/bash

set -exo pipefail

main() {

    # Install packages
    export PATH=$PATH:/home/dnanexus/.local/bin  # pip installs some packages here, add to path
    sudo -H python3 -m pip install --no-index --no-deps packages/*

    # Load data
    dx-download-all-inputs
    # Move all files in subdirectories of /in directory to the current project
    find ~/in -type f -name "*" -print0 | xargs -0 -I {} mv {} ./

    # Download docker image from 001 folder
    dx download "$somalier_docker" -o somalier.tar.gz

    # clean file_prefix input
    # Removed the 002 or 003 part of the run folder
    file_prefix=$(echo $file_prefix | sed s'/^00[23][-_]//' )
    echo "'${file_prefix}'"

    # Create ped file
    echo "--------------Creating ped file-------------------"
    python3 make_ped.py -a *.somalier

    # Run relate somalier
    echo "--------------Run Somalier docker -----------------"
    service docker start
    docker load -i somalier.tar.gz

    # Get image id from docker image loaded
    SOM_IMAGE_ID=$(sudo docker images --format="{{.Repository}} {{.ID}}" | grep "^brentp" | cut -d' ' -f2)

    if [[ ! -z ${file_prefix} ]]; then
        echo "Prefix " "${file_prefix}" " will be used for output files"
        docker run  -v /home/dnanexus/:/data ${SOM_IMAGE_ID} /bin/bash -c "cd /data ; somalier relate -o ${file_prefix}.somalier --ped /data/Samples.ped /data/*.somalier"
    else
        echo "No prefix provided for output files - default somalier will be used"
        docker run  -v /home/dnanexus/:/data ${SOM_IMAGE_ID} /bin/bash -c "cd /data ; somalier relate --ped /data/Samples.ped /data/*.somalier"
    fi

    chmod 777 *

    echo "--------------Outputting files -----------------"
    mkdir -p /home/dnanexus/out/html/
    mkdir -p /home/dnanexus/out/pairs_tsv/
    mkdir -p /home/dnanexus/out/samples_tsv/
    mkdir -p /home/dnanexus/out/ped_output

    mv *somalier.html /home/dnanexus/out/html/
    mv *somalier.pairs.tsv /home/dnanexus/out/pairs_tsv/
    mv *somalier.samples.tsv /home/dnanexus/out/samples_tsv/
    mv Samples.ped /home/dnanexus/out/ped_output

    # If a single somalier file is inputted, groups.tsv file is not generated
    if [ -f *somalier.groups.tsv ]; then
        echo "somalier.groups.tsv exists."
        mkdir -p /home/dnanexus/out/groups_tsv/
        mv *somalier.groups.tsv /home/dnanexus/out/groups_tsv/
    else
        echo "somalier.groups.tsv does not exist as a single sample was used"
    fi

    dx-upload-all-outputs

}
