# 


We need PLINK, R, and Python (I develop my Python scripts to optimize the GWAS QC working flow).


Create and instal:

`seaborn` does not need `conda-forge`. `numpy`, `scipy`, `pandas`, and `matplotlib` will be included. 

- [ ] Do I need to include JupyterNotebook?

```bash
conda create -n gwas-qc-env conda-forge::r-base bioconda::plink python seaborn
```

Of note: osx-arm64 platform ok.

Acitvate

```bash
conda activate gwas-qc-env
```

## Obtain py_scripts by cloning this repository

We also need the `py_scripts` in this section. Clone ... to ...
TODO: Find a better way to manage it for people want to follow these notes. 

Clone to `work/xxx`.

At `work/xxx`

```bash
git clone https://github.com/wudaudau/immunegenetic_notes.git
```

Move 

```bash
cp -r immunegenetic_notes/gwas_qc/py_scripts /your/target/folder/
```

Remove ... To obtain the updated repository, we need to remove the entire repo first and clone again.

```bash
rm -rf immunegenetic_notes/
```