# QCs - step-by-step

(still in editing)

It's good to practice step-by-step to learn each QC step.

There are 7 QC steps. (Table 1 to the article https://onlinelibrary.wiley.com/doi/10.1002/mpr.1608).

The QC1 to QC6 are based on the  Part 1 of **GWA_tutorial** (https://github.com/MareesAT/GWA_tutorial). There are instructions in (`1_Main_script_QC_GWAS.txt`).

QC7 PCA will be use **smartpca** tool (link to my note).

- [ ] I need to develop and provide my Py scripts.


## Working directory

`/work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/`

Data in `data`. Make a copy to the working directory to get started.

```bash
plink \
--bfile /data/clwu/demo/LEAP_FreezeV3_1563_May2020_PSC2 \
--make-bed \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc0_source_file 
```

It is also the output directory. All the generated files will be here.

## QC1 View Missing

(in the tuto)

## QC1-1 Missing on Variants

Delete SNPs with missingness > 2% and generate new bfiles.

- [ ] We may need a step to copy the bfiles to the output folder. Because we are generating bfiles steps by steps in the output folder.

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc0_source_file \
--geno 0.02 \
--make-bed \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc1_1_geno002
```

Output:
- `.log`
- new bfiles
- `.hh`  (heterozygous haploid and nonmale Y chromosome call list) (https://www.cog-genomics.org/plink/1.9/formats#hh) (https://www.cog-genomics.org/plink/1.9/output).

The `.hh` file is the list to keep(?) (nonmissing calls).

```
96262   796253871713    rs5939319
86827   696700648122    rs5939319
96262   796253871713    rs1419931
96262   236256460571    rs1419931
...
```


## QC1-2 Missing On Individuals

Use the previous output.
Delete individuals with missingness > 5%.

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc1_1_geno002 \
--mind 0.05 \
--make-bed \
--out  /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc1_2_mind005
```

Output:
- `.log`
- new bfiles
- `.hh`  (heterozygous haploid and nonmale Y chromosome call list) (https://www.cog-genomics.org/plink/1.9/formats#hh)
- `.irem` FID and IID of the removed individuals (https://www.cog-genomics.org/plink/1.9/output).


## QC2 Sex

> Subjects who were a priori determined as females must have a F value of <0.2, and subjects who were a priori determined as males must have a F value >0.8. This F value is based on the X chromosome inbreeding (homozygosity) estimate.

(Overview of this step ...)

Check for sex discrepancy.

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc1_2_mind005 \
--check-sex \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc2_sexcheck
```

(https://www.cog-genomics.org/plink/1.9/basic_stats#check_sex)

Output:
- `.log`
- `.hh`  (heterozygous haploid and nonmale Y chromosome call list) (https://www.cog-genomics.org/plink/1.9/formats#hh)
- `.sexcheck`

Then, we need to generate a file `sex_discrepancy.txt` using the `.sexcheck` file.

```
    FID            IID       PEDSEX       SNPSEX       STATUS            F
  28328   502088905174            2            2           OK     -0.04789
  99407   971064170845            2            2           OK      0.05654
  94811   869570533760            2            2           OK       0.1266
...
```

How to make it? Based on `.sexcheck` file :
1. Filter STATUS are NOT "OK".
2. Check F on females. F of female are < 0.2.
3. Check F on males. F of male are > 0.8.

Generate `sex_discrepancy.txt` using my Py script (there are some details in the scripts):

```bash
python /work/clwu/GWA_tutorial/py_scripts/sexcheck.py /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc2_sexcheck.sexcheck
```

Output:
- `sex_discrepancy.txt`. A list of inidividual to remove.

Remove sex discripency:

- [ ] Do we need to update the file name from `sex_discrepancy.txt` to `qc2_sex_discrepancy.txt`???

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc1_2_mind005 \
--remove /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/sex_discrepancy.txt \
--make-bed \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc2_rmsexdic
```

Output:

- `.log`
- new bfiles

## QC3 MAF

> Generate a bfile with autosomal SNPs only and delete SNPs with a low minor allele frequency (MAF).
> A conventional MAF threshold for a regular GWAS is between 0.01 or 0.05, depending on sample size.

Steps overview:

- Only focus on autosomal SNPs (Chr 1-22).
- Calculate MAF using `--freq`.
- View MAF distribution to determine the low MAF thereshold. (MAF_check).
- Remove low MAF using `--MAF`.

Select autosomal SNPs only (Chr 1-22) using plink.

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc2_rmsexdic \
--chr 1-22 \
--make-bed \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc3_1_chr1_22
```

Output:

- `.log`
- new bfiles

Check MAF on Chr 1-22:


```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc3_1_chr1_22 \
--freq \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc3_1_chr1_22_MAF_check
```

Output:

- `.log`
- `.frq`

PLINK will generate a log and a `.frq` file, which is a table of MAF (https://www.cog-genomics.org/plink/1.9/basic_stats#freq).

```
CHR         SNP   A1   A2          MAF  NCHROBS
   1   rs4477212    0    A            0     2036
   1   rs3131972    T    C        0.192     2036
   1  rs11240777    A    G       0.2463     2038
   1   rs4970383    T    G        0.253     2024
   1   rs4475691    T    C        0.213     2038
   1   rs7537756    G    A       0.2198     2038
...
```


There is a R script to visualize the result in plots (MAF distribution). `MAF_check.R`

- [x] I can create my own script to plot it or to sort the table by MAF or to aggregate the count by MAF. We need to determine the threshold to contraol on MAF. -> `mafcheck.py`

```bash
python /work/clwu/GWA_tutorial/py_scripts/mafcheck.py /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc3_1_chr1_22_MAF_check.frq 
```

Output:

- `qc3_maf_distribution.png`


Once the MAF threshold is determined, we can drop the low MAF from bfile.

Remove low MAF (0.01):

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc3_1_chr1_22 \
--maf 0.01 \
--make-bed \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc3_2_maf001
```

Output:

- `.log`
- new bfiles

## QC4 HWE

> Delete SNPs which are not in Hardy-Weinberg equilibrium (HWE).

Steps overview:

- Use `--hardy` to calculate HWE in a `.hwe` file.
- View the HWE distribution (all and below the threshold, respectively).
- Remove low HWE individual from the bfiles (**on all individuals** with a threshold).

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc3_2_maf001 \
--hardy \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc3_2_maf001_hardy
```

- [ ] I might need to update the output file name to prevent the log been overwitten.

Output:

- `.log`
- `.hwe`

(What does `--hardy` do? https://www.cog-genomics.org/plink/1.9/basic_stats#hardy)

This will generate a `.hwe` file (https://www.cog-genomics.org/plink/1.9/basic_stats#hardy). It is a big file. The columns are: "CHR", "SNP", "TEST", "A1", "A2", "GENO", "O(HET)", "E(HET)", and "P".

```
CHR         SNP     TEST   A1   A2                 GENO   O(HET)   E(HET)            P 
   1   rs3131972      ALL    T    C           34/323/661   0.3173   0.3103       0.5444
   1   rs3131972      AFF    T    C              2/15/20   0.4054   0.3817            1
   1   rs3131972    UNAFF    T    C              4/50/92   0.3425   0.3184       0.4456
   1  rs11240777      ALL    A    G           72/358/589   0.3513   0.3713      0.09131
   ...
```

Run the `hwe.py` to generate the hwe (P) and zoomhwe **(P < 0.00001)** in histograms (Histogram HWE and Histogram HWE: strongly deviating SNPs only) in the output folder.

```bash
python /work/clwu/GWA_tutorial/py_scripts/hwe.py /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc3_2_maf001_hardy
```

Output:

- `hwe_distribution.png`
- `hwe_distribution_below_threshold.png`

Filter HWE **on all individuals** using 1e-10 as the threshold. (Add `--hwe-all` to filter HWE on all individuals rather than only control ones.)

```bash
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc3_2_maf001 \
--hwe 1e-10 \
--hwe-all \
--make-bed \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10
```

## Generate indepSNP tags

When QC1 to QC4 are done, we can generate the indepSNP tags for the following QC steps.

We need a `inversion.txt` file.

`inversion.txt` is already in the **1_QC_GWAS** package.

```
6 25500000 33500000 8 HLA
8 8135000 12000000 Inversion8
17 40900000 45000000 Inversion17
```

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10 \
--exclude inversion.txt \
--range \
--indep-pairwise 50 5 0.5 \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10_indepSNP
```

## QC5 Heterogzygotie

Use `indepSNP.prune.in` to generate pruned the data set.

Use the input to generate the indeSNP tag as the input bfile.

`--het` homozygous genotype counts (https://www.cog-genomics.org/plink/1.9/basic_stats#ibc).

- [x] Do I need to focus on the autosome?? -> We already remove the sex chormosome after the sex check.

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10 \
--extract /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10_indepSNP.prune.in \
--het \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc5_homozygous_check
```

The output `` file is a table similar to `--hardy` but not exactly. The columns are: "FID", "IID", "O(HOM)", "E(HOM)", "N(NM)", "F".


Plot of the heterozygosity rate distribution

```bash
python py_scripts/qc5_heterogenity_check.py /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc5_homozygous_check.het
```

The tutorial says that we use 3 SDs to keep individuals with 3SDs. However, accroding to Sigrid, it's better to adjust the histogram to adapte the filter. We may keep all individulas it no weired values and count presented.

There sould be someting to get a list of individuals to extract or to exclude.

```bash
```

## QC6 IBD

Calculate IBD. The inputfile can contain family members. We will evaluate the IBD values to determine which individuals to exclude.

Calculates **identity by descent (IBD)** using `--genome` and based on the LD-based purning (https://www.cog-genomics.org/plink/1.9/ibd).

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10 \
--extract /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10_indepSNP.prune.in \
--genome \
--min 0.2 \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc6_pihat_min0.2
```

The `.genome` file is a table. The columns are: "FID1", "IID1", "FID2", "IID2", "RT", "EZ", "Z0", "Z1", "Z2", "PI_HAT", "PHE", "DST", "PPC", and "RATIO". **FS means ; PO means parent-offspring; OT means ; UN means unrelated individuals.**

```
```

Select based on **"PI_HAT"**.

For each row of "PI_HAT" < threshole, there are two IID. We need to check the MAF of them to determin which one to be removed from the individuals of study. Normally, we drop the low MAF one.  

For each row of "PI_HAT" < threshole, there are two IID. We need to check the MAF of them to determin which one to be removed from the individuals of study. Normally, we drop the low MAF one.  


### How to get participant list

QC1-1 log:

```
1566 people (846 males, 720 females) loaded from .fam.
700 phenotype values loaded from .fam.
Using 1 thread (no multithreaded calculations invoked).
Before main variant filters, 1028 founders and 538 nonfounders present.
```

**Founders** are those PID and MID is 0. Which means they are the **parents**.

LEAP_FreezeV3_1566_May2020_PSC2.fam:

```
Groupby P Count:
    FID  IID  PID  MID  Sex    6
P                               
-9  866  866  866  866  866  866
 1  287  287  287  287  287  287
 2  413  413  413  413  413  413
```

The "P" in `.fam` file is a better indicator to select the participants.

Since the founders are not accosiated to the phenotypes, **do not use** `--filter-founders --make-bed --out ` to remove ...

I want to get the IDs based on "P". Keep only value is 1 or 2. -> There is a `participant_IDs.csv` in the output repository.

Of note, last time when I did QC, the participant are based on a table from AIMS to indicate participants. Amount the "participant", there are "P" == 9 in the `.fam` file we can see them on the pca plot.

### QC7 PCA with PLINK

We need:

- participant only (`participant_IDs.csv`) (Use `--require-pheno`?)
- indepSNP tag

Keep participant only:

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10 \
--keep /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/participant_IDs.csv \
--make-bed \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc7_1_participant_only
```

PCA on the participant only

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc7_1_participant_only \
--extract /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10_indepSNP.prune.in \
--pca \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc7_2_pca \
--maf 0.05
```

(No PCA results using Plink if without MAF adjustion)
(`smartpca` has no problem without MAF adjustion)

- [ ] Try can we do the pca in one step:

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10 \
--keep /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/participant_IDs.csv \
--extract /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10_indepSNP.prune.in \
--pca \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc7_pca 
```








## Convert to ped/map

Generate `.ped` and `.map` to run **smartpca**.

`--recode` is the call to convert to ped/map (https://www.cog-genomics.org/plink/1.9/data#recode).

Use the same input as the plink pca

```bash
plink \
--bfile /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc7_1_participant_only \
--extract /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc4_hweall1em10_indepSNP.prune.in \
--recode \
--out /work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2_QC/qc7_3_recode_pedmap 
```


