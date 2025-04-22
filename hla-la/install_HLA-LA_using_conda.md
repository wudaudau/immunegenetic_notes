# 


https://github.com/DiltheyLab/HLA-LA?tab=readme-ov-file

It takes hours to index the graph and testing installation, respectively.



## Steps of installation

### Create the env with required packages

Run the following code to create an env named `hla-la-env` with `hla-la` (channel bioconda). `libgcc-ng` (channel conda-forge) is required to installing hla-la.

```bash
conda create -n hla-la-env bioconda::hla-la conda-forge::libgcc-ng
```

The Platform should be linux-64. It does not work on MAC OS.

Of note, I saw it uses older versions of Py and pandas among the packages. In order to not disrupt the env, do not add Python to the env.

**Be careful with the messages from conda to download the data packages and index the graph.**

### Download the data package

It's about 5GB.

```bash
mkdir /work/clwu/miniconda3/envs/hla-la-env/opt/hla-la/graphs
cd /work/clwu/miniconda3/envs/hla-la-env/opt/hla-la/graphs
wget http://www.well.ox.ac.uk/downloads/PRG_MHC_GRCh38_withIMGT.tar.gz
tar -xvzf PRG_MHC_GRCh38_withIMGT.tar.gz
```

### Download the reference

It's about 852.68MB.

```bash
(in envs/hla-la-env/opt/hla-la/src)
wget https://www.dropbox.com/s/mnkig0fhaym43m0/reference_HLA_ASM.tar.gz
tar -xvzf reference_HLA_ASM.tar.gz
```

### Modifying paths.ini

Skip it. We don't need to specify a working directory. We specify it at each run.

(GitHub)
> If you want to create a central installation of HLA-LA, you will probably want to delete the `workingDir` entry from the `paths.ini` file -- this forces users to specify a working directory via the command line and avoids shared access to the same working directory.

### Index the graph

```bash
../miniconda3/envs/hla-la-env/opt/hla-la/bin/HLA-LA --action prepareGraph --PRG_graph_dir /work/clwu/miniconda3/envs/h
la-la-env/opt/hla-la/graphs/PRG_MHC_GRCh38_withIMGT
```

## Testing installation

We can create a repository name `HLA-LA` to run it. It would be the `--workingDir` to run `HLA-LA.pl`.

Download the "BA121878 mini" test CRAM file from Dropbox using `wget`.

```bash
wget https://www.dropbox.com/s/xr99u3vqaimk4vo/NA12878.mini.cram?dl=0
```

Rename the file to remove "?dl=0" use `mv`.

```bash
mv NA12878.mini.cram?dl=0 NA12878.mini.cram
```

Activate the env and run. We can adjust `--maxThreads`.

```bash
HLA-LA.pl --BAM NA12878.mini.cram --graph PRG_MHC_GRCh38_withIMGT --sampleID NA12878 --maxThreads 7 --workingDir /work/clwu/HLA-LA/
```
