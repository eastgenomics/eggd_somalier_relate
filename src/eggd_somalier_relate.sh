#!/bin/bash

set -exo pipefail

main() {

    # Install packages
    pip install packages/pandas-0.24.2-cp35-cp35m-manylinux1_x86_64.whl

    # Load data
    dx-download-all-inputs
    # Move all files in subdirectories of /in directory to the current project
    find ~/in -type f -name "*" -print0 | xargs -0 -I {} mv {} ./

    # Create ped file 
    echo "--------------Creating ped file-------------------"
    python3 make_ped.py -a *.somalier
      
    # Run relate somalier
    echo "--------------Run Somalier docker -----------------"
    service docker start
    docker load -i somalier_v0_2_12.tar.gz

    echo "No prefix provided for output files - default somalier will be used"
    docker run  -v /home/dnanexus/:/data brentp/somalier:v0.2.12 /bin/bash -c "cd /data ; somalier relate --ped /data/Samples.ped /data/*.somalier"

    chmod 777 *

    echo "--------------Outputting files -----------------"
    mkdir -p /home/dnanexus/out/html/
    mkdir -p /home/dnanexus/out/pairs_tsv/
    mkdir -p /home/dnanexus/out/samples_tsv/
    mkdir -p /home/dnanexus/out/groups_tsv/
    mkdir -p /home/dnanexus/out/ped_output

    mv *somalier.html /home/dnanexus/out/html/
    mv *somalier.pairs.tsv /home/dnanexus/out/pairs_tsv/
    mv *somalier.samples.tsv /home/dnanexus/out/samples_tsv/
    mv *somalier.groups.tsv /home/dnanexus/out/groups_tsv/
    mv Samples.ped /home/dnanexus/out/ped_output

    dx-upload-all-outputs

}
