# 

I adapted my script based on the instruction on [hla-mapper GitHub](https://github.com/erickcastelli/hla-mapper).

This note includes the installation and test using the test_sequences provided.

## Steps of installation

I will clone the `hla-mapper` repository from GitHub repo to my working directory (`/work/clwu/`).

Create the conda env `hla-mapper-v4-env` and install the packages.

(blast can be specify to version 2.15. It's the laster version tasted with [[hla-mapper]])

```bash
conda create -n hla-mapper-v4-env gcc=11.4.0 conda-forge::gxx=11.4.0 bioconda::bwa=0.7.17 bioconda::freebayes=1.3.6 bioconda::samtools=1.19 bioconda::bcftools=1.19 bioconda::star=2.7.10b bioconda::whatshap=2.2 conda-forge::py-bgzip bioconda::tabix conda-forge::parallel conda-forge::boost=1.74.0=py310h7c3ba0c_5 conda-forge::boost-cpp=1.74.0=h75c5d50_8 cmake=3.29.2 conda-forge::zlib conda-forge::htop wget conda-forge::openjdk=17 bioconda::blast
```

At my working directory:

```bash
git clone https://github.com/erickcastelli/hla-mapper.git
```


Enter the hla-mapper repository.

```bash
cd hla-mapper
```


Download the **last version** of the **hla-mapper database** in `/work/clwu/hla-mapper`.

```bash
wget --no-check-certificate https://www.castelli-lab.net/support/hla-mapper_4_db_latest.zip
```

Unzip the database.

```bash
unzip hla-mapper_4_db_latest.zip
```

Create a new folder named `build` and enter it.

```bash
mkdir build && cd build
```

Activate the hla-mapper-env environment.

```bash
conda activate hla-mapper-env
```

Compile hla-mapper **from the /build folder**. (My env name is `hla-mapper-env`)

```bash
BOOST_ROOT=/home/USER/miniconda3/envs/hla-mapper-env ZLIB_ROOT=/home/USER/miniconda3/envs/hla-mapper-env cmake ../src/
```

```bash
make
```

Copy the hla-mapper binary to `(hla-mapper env)/bin`

```bash
cp hla-mapper ../../miniconda3/envs/hla-mapper-env/bin/
```

Run hla-mapper.

```bash
hla-mapper
```

Set up `hla-mapper`.

Output:

```
**** Configuration list ***
Database: hla-mapper_4_db_latest
Samtools: /work/clwu/miniconda3/envs/hla-mapper-env/bin/samtools
BWA:      /work/clwu/miniconda3/envs/hla-mapper-env/bin/bwa
WhatsHap: /work/clwu/miniconda3/envs/hla-mapper-env/bin/whatshap
Freebayes: /work/clwu/miniconda3/envs/hla-mapper-env/bin/freebayes
BLAST:    /work/clwu/miniconda3/envs/hla-mapper-env/bin/blastn
```


## Test installation using the test_sequences

The main working directory `work/clwu/hla-mapper`.

I create a `output` repository in the main working directory. This step can be skipped. Just specify `sample=(sample ID)` `output=output/(sample ID)` in the command, and `hla-mapper` will create a repository.

### Re-aligning the BAM file

```bash
hla-mapper dna bam=test_sequences/HG01890_HLA-A.bam sample=HG01890 output=output/HG01890_BAM
```

It takes only 40s.

### Aligning FASTQ

```bash
hla-mapper dna r1=test_sequences/HG01890_HLA-A_R1.fastq r2=test_sequences/HG01890_HLA-A_R2.fastq sample=HG01890 output=output/HG01890_FASTQ
```
