# eggd_somalier_relate

## What does this app do?
This app runs Somalier (v0.2.12) to predict relatness and sex of samples. 

This app is based on https://github.com/brentp/somalier

![Image of workflow](https://github.com/eastgenomics/eggd_somalier_extract/blob/dev/somalier_relate_workflow.png)

## What are the inputs?
Inputs are the somalier files. These can be inputed as an array.

## What are the outputs?
* Somalier.html
  Interactive visualization of results.

* Somalier.pairs.tsv
  The relatedness between pairs of samples.
  
* Somalier.samples.tsv
  Contains depth, het and homo of X chromosomes along with other QC metrics.

* Somalier.groups.tsv

## Where is this app applicable?
This app can be used after sites required are extracted, usually after running somalier_extract. This app can be used in a multi workflow as the app can take multiple inputs in.

## How does this app calculate relatedness and sex of sample?
To run sex check and relatedness - the app somalier_related needs to be run. This will output a tsv and html of all samples sex and relatedness.

### This app was made by EMEE GLH
