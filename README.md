# eggd_somalier_relate

## What does this app do?
This app runs Somalier (v0.2.12) to predict sex of samples. Can also predict relatedness between samples and ancestry.

This app is based on https://github.com/brentp/somalier

![Image of workflow](https://github.com/eastgenomics/eggd_somalier_relate/blob/dev/somalier_relate_workflow.jpg)

## What are the inputs?
* Array of {sample}.somalier files
* Female and male X heterozygous call thresholds, defaults are 45 and 1 respectively. (Optional)
* Reported sex in xlsx file, defaults are labelled as unknown (Optional):
  * Column 1 : Lab numbers
  * Column 2 : Exome Numbers
  * Column 3 : Reported Sex (Categorised as F and M) 
* Text File which contains prefix for outputs, can be run folder here ideally, default is somalier prefix. (Optional) 

## What are the outputs?

* Somalier.samples.tsv - contains depth, het and homo of X chromosomes along with predicted sex and other QC metrics.

* Somalier.html - interactive visualization of results.

* Somalier.pairs.tsv - the relatedness between pairs of samples.
  
* Somalier.groups.tsv

## Where is this app applicable?
This app can be used after sites required are extracted, usually after running somalier_extract. This app can be used in a multi workflow as the app can take multiple inputs in.

## How does this app calculate sex of sample?

The {samples}.somalier file is a binary file with selected sites from vcf. The sites on the X and Y chromosome are specific to each chromosome and not in PARs. The heterozygous(het) calls on the X chromosome are used to predict whether a sample is female or male as females have more het calls due to have two X chromsomes. Males typically have 0 or 1 het calls whereas female have a wider range, typically starting at 45.

### This app was made by EMEE GLH
