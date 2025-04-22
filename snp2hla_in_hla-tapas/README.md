# README

The SNP2HLA in [HLA-TAPAS](https://github.com/immunogenomics/HLA-TAPAS) is an updated version. 

After a quick test, I found this version of SNP2HLA is

- Faster. 2 hours instead of greater than 7 hours of HLA imputation using the same input file. 
- Higer resolution. Up to 4-field of HLA alleles instead of 2-field.
- Only one output file: `.bgl.phased.vcf.gz`.
- Phased HLA data?


## Insteall using conda

You can install HLA-LA by creating a new environment and specifying all required channels in a single command.

https://github.com/immunogenomics/HLA-TAPAS/issues/29

```bash
conda create -n hla-tapas-env python=3.7 pandas=1.0.3 conda-forge::r-base r::r-argparse conda-forge::r-stringr conda-forge::r-purrr conda-forge::r-dplyr conda-forge::r-multidplyr conda-forge::r-tidyr conda-forge::r-data.table conda-forge::parallel conda-forge::r-rcompanion bioconda::plink bioconda::beagle=4.1
```

Note:

- `argparse` should be specified as `r-argparse` to ensure the R version is installed instead of the Python one.
- `r-multidplyr` requires r-base >= 4.2. Therefore, I didn’t restrict r-base to version 3.6 as mentioned in the README.

