#!/bin/bash
# eggd_somalier_relate 0.0.1
# Generated by dx-app-wizard.

set -exo pipefail

main() {

    echo "Value of input_file: '${input_file[@]}'"

    echo "Value of female: '${f}'"

    echo "Value of male: '${m}'"
    # The following line(s) use the dx command-line tool to download your file
    # inputs to the local file system using variable names for the filenames. To
    # recover the original filenames, you can use the output of "dx describe
    # "$variable" --name".

    # install python packages from included wheels
    # pip install --upgrade pip
    pip install packages/pandas-0.24.2-cp35-cp35m-manylinux1_x86_64.whl

    dx-download-all-inputs

    find ~/in -type f -name "*" -print0 | xargs -0 -I {} mv {} ./

    ls -a
    echo "--------------Creating ped file-------------------"
    if [[ ! -z ${ReportedSex_file} ]]; then
        echo "Reported sex file provided"
        python3 make_ped.py -a *.somalier -s ${ReportedSex_file}
    else
        echo "Reported sex file not provided so will assume unknown for all"
        python3 make_ped.py -a *.somalier
    fi
    
    dx pwd
    
    # Now run static binary in resources/usr/bin
    echo "--------------Run Somalier docker -----------------"

    ls -a
    pwd

    service docker start

    docker load -i somalier_v0_2_12.tar.gz

    docker run  -v /home/dnanexus/:/data brentp/somalier:v0.2.12 /bin/bash -c "cd /data ; somalier relate --ped /data/Samples.ped /data/*.somalier"
  
    echo "-------------- Predicting sex based on threshold -----------------"
    # Add threshold to file
    # if statement -z assumes the parameter is null
    if [[ ! -z ${f} ]] && [[ ! -z ${m} ]]; then
        echo "Inputted thresholds will be used: Female =<" "${f} and" "male =>" "${m}"
        python3 het.py -F ${f} -M ${m}
    elif [[ ! -z ${f} ]] && [[ -z ${m} ]]; then
        echo "Female threshold set to" "${f}." "Default threshold for male =< 1 het calls will be used."
        python3 het.py -F ${f} -M 1
    elif [[  -z ${f} ]] && [[ ! -z ${m} ]]; then
        echo "Male threshold set to" "${m}." "Default threshold for female => 45 het calls will be used."
        python3 het.py -F 45 -M ${m}
    else
        echo "No inputs provided. Default het call thresholds of female => 45 and male =< 1 are used."
        python3 het.py -F 45 -M 1
    fi

    echo "--------------Outputting files -----------------"
    ls -a

    mkdir -p /home/dnanexus/out/html/
    mkdir -p /home/dnanexus/out/pairs_tsv/
    mkdir -p /home/dnanexus/out/samples_tsv/
    mkdir -p /home/dnanexus/out/groups_tsv/

    mv somalier.html /home/dnanexus/out/html/
    mv somalier.pairs.tsv /home/dnanexus/out/pairs_tsv/
    mv somalier.samples.tsv /home/dnanexus/out/samples_tsv/
    mv somalier.groups.tsv /home/dnanexus/out/groups_tsv/

    ls -a /home/dnanexus/out/html
    ls -a /home/dnanexus/out/pairs_tsv
    ls -a /home/dnanexus/out/samples_tsv
    ls -a /home/dnanexus/out/groups_tsv
    ls -a /home/dnanexus/out/

    dx-upload-all-outputs

}
