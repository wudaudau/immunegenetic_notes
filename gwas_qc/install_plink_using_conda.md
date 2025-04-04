# 


We need PLINK, R, and Python (I develop my Python scripts to optimize the GWAS QC working flow).


Create and instal:

`seaborn` does not need `conda-forge`. `numpy`, `scipy`, `pandas`, and `matplotlib` will be included. 

- [ ] Do I need to include JupyterNotebook?

```bash
conda create -n gwas-qc-env conda-forge::r-base bioconda::plink python seaborn
```

Acitvate

```bash
conda activate gwas-qc-env
```


We also need the `py_scripts` in this section. Clone ... to ...
TODO: Find a better way to manage it for people want to follow these notes. 