# README

Once we have done the QC steps, the data is ready for HLA imputation.

https://software.broadinstitute.org/mpg/snp2hla/

(What is it? What does it do?)

## Requirements

SNP2HLA https://software.broadinstitute.org/mpg/snp2hla/

Download SNP2HLA from: https://software.broadinstitute.org/mpg/snp2hla/data/SNP2HLA_package_v1.0.3.tar.gz 


In `SNP2HLA` folder.

```bash
wget https://software.broadinstitute.org/mpg/snp2hla/data/SNP2HLA_package_v1.0.3.tar.gz
```

```bash
tar -xvzf SNP2HLA_package_v1.0.3.tar.gz
```


We need: 
Plink
Beagle (version 3.0.4) (beagle.jar)
linkage2beagle.jar
beagle2linkage.jar

We don't create a specific conda env. Because I cannot find Beagle 3.0.4 on Conda. 

So we need to add the 3 Beagle jar files to the package. For Plink, use the plink in `gwas-qc-env` which is Plink 1.9 instead of 1.7.



> 1. Download Plink for your platform (http://pngu.mgh.harvard.edu/~purcell/plink/download.shtml). Copy the "plink" run file into the current directory (with SNP2HLA.csh).
> 
> 2. Download Beagle (version 3.0.4) .jar files into the current directory.
> - "beagle.jar" from http://faculty.washington.edu/browning/beagle/beagle.html#download
> We recommend downloading version 3.0.4 for the compatability issue, even if it is not the newest version. Beagle web page described above includes links for all past-version binaries.
> - "linkage2beagle.jar" can be found in the Beagle 3.0.4 package (zip file) in the utility directory. Copy this to the current directory, too.
> - "beagle2linkage.jar" from  http://faculty.washington.edu/browning/beagle_utilities/utilities.html


## Reference file

Use *T1DGC_REF* instead of HM_CEU_REF.

## Script to run SNP2HLA

We need to create a bash script (`.sh`) to run it on the server (cluster). Because it is long to run.


INPUTS: 
# 1. Plink dataset
# 2. Reference dataset (beagle format)
# 
# DEPENDENCIES: (download and place in the same folder as this script)
# 1. PLINK (1.07)
# 2. Beagle (3.0.4)
# 3. merge_tables.pl (Perl script to merge files indexed by a specific column)
# 4. linkage2beagle and beagle2linkage (Beagle utilities for PED <-> Beagle format)
# 5. ParseDosage.csh (Converts Beagle posterior probabilities [.gprobs] to dosages in PLINK format [.dosage])
#
# USAGE: ./SNP2HLA.csh DATA (.bed/.bim/.fam) REFERENCE (.bgl.phased/.markers) OUTPUT plink max_memory[mb] window