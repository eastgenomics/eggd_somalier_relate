#!/bin/bash
# eggd_somalier_relate 0.0.1
# Generated by dx-app-wizard.

set -exo pipefail

main() {

    echo "Value of female: '${f}'"

    echo "Value of male: '${m}'"

    # Install packages
    pip install packages/pandas-0.24.2-cp35-cp35m-manylinux1_x86_64.whl

    # Load data
    dx-download-all-inputs
    find ~/in -type f -name "*" -print0 | xargs -0 -I {} mv {} ./

    # If file_prefix.txt is provided, use that to name files
    # else the $file_prefix will be blank
    if [[ ! -z "$file_prefix" ]]; then
        dx download "$file_prefix" -o file_prefix
        file_prefix=$(cat file_prefix)
        echo "'${file_prefix}'"
        file_prefix=$(echo $file_prefix | sed 's/.$//'| sed 's/.$//' | cut -d "_" -f2- )
        echo "'${file_prefix}'"
    fi

    # Create ped file 
    echo "--------------Creating ped file-------------------"
    python3 make_ped.py -a *.somalier
      
    # Run relate somalier
    echo "--------------Run Somalier docker -----------------"
    service docker start

    docker load -i somalier_v0_2_12.tar.gz

    if [[ ! -z ${file_prefix} ]]; then
        echo "Prefix " "${file_prefix}" " will be used for output files"
        docker run  -v /home/dnanexus/:/data brentp/somalier:v0.2.12 /bin/bash -c "cd /data ; somalier relate -o ${file_prefix}.somalier --ped /data/Samples.ped /data/*.somalier"
    else
        echo "No prefix provided for output files - default somalier will be used"
        docker run  -v /home/dnanexus/:/data brentp/somalier:v0.2.12 /bin/bash -c "cd /data ; somalier relate --ped /data/Samples.ped /data/*.somalier"
    fi
    
    # Add predicted sex to file
    echo "-------------- Predicting sex based on threshold -----------------"
    chmod 777 *
    # Add threshold to file
    # if statement -z assumes the parameter is null
    if [[ ! -z ${f} ]] && [[ ! -z ${m} ]]; then
        echo "Inputted thresholds will be used: Female =<" "${f} and" "male =>" "${m}"
        python3 het.py -F ${f} -M ${m} -i *somalier.samples.tsv
    elif [[ ! -z ${f} ]] && [[ -z ${m} ]]; then
        echo "Female threshold set to" "${f}." "Default threshold for male =< 1 het calls will be used."
        python3 het.py -F ${f} -M 1 -i *somalier.samples.tsv
    elif [[  -z ${f} ]] && [[ ! -z ${m} ]]; then
        echo "Male threshold set to" "${m}." "Default threshold for female => 45 het calls will be used."
        python3 het.py -F 45 -M ${m} -i *somalier.samples.tsv
    else
        echo "No inputs provided. Default het call thresholds of female => 45 and male =< 1 are used."
        python3 het.py -F 45 -M 1 -i *somalier.samples.tsv
    fi

    echo "--------------Outputting files -----------------"
    mkdir -p /home/dnanexus/out/html/
    mkdir -p /home/dnanexus/out/pairs_tsv/
    mkdir -p /home/dnanexus/out/samples_tsv/
    mkdir -p /home/dnanexus/out/groups_tsv/

    mv *somalier.html /home/dnanexus/out/html/
    mv *somalier.pairs.tsv /home/dnanexus/out/pairs_tsv/
    mv *somalier.samples.tsv /home/dnanexus/out/samples_tsv/
    mv *somalier.groups.tsv /home/dnanexus/out/groups_tsv/

    dx-upload-all-outputs

}
