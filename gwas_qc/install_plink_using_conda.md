# 


We need PLINK, R, and Python (I develop my Python scripts to optimize the GWAS QC working flow).


Create and instal:

- [ ] Do I need to include JupyterNotebook?

```bash
conda create -n gwas-qc-env conda-forge::r-base bioconda::plink python seaborn
```

Acitvate

```bash
conda activate gwas-qc-env
```