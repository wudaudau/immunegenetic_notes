# QCs - step-by-step

It's good to practice step-by-step to learn each QC step.

The parameters used in this note are for HLA imputation steps, rather than general GWAS.

We keep the family members in the data to impute HLA.

## Step overview

missingness/sex check → MAF → HWE → LD pruning → heterozygosity → IBD → PCA

- QC1: Missingness
- QC2: Sex check
- QC3: MAF
- QC4: HWE
- QC5: LD pruning  
- QC6: Heterogeneity
- QC7: IBD
- QC8: PCA Poplutation

(QC8 PCA will be use **smartpca** tool (link to my note).)

## References

- [Marees AT, de Kluiver H, Stringer S, et al. A tutorial on conducting genome-wide association studies: Quality control and statistical analysis. Int J Methods Psychiatr Res. 2018; 27:e1608. https://doi.org/10.1002/mpr.1608](https://onlinelibrary.wiley.com/doi/10.1002/mpr.1608)
- [GWA_tutorial GitHub Repository](https://github.com/MareesAT/GWA_tutorial): Particularly Part 1 of **GWA_tutorial**.
- [PLINK 1.9 Documentation](https://www.cog-genomics.org/plink/1.9/)

## Before QC

- **DATASET**: Input genotype files in PLINK binary format (.bed, .bim, .fam).
- **PYDIR**: Directory containing Python scripts used during QC.
- **INVERSIONTXT**: A file listing genomic regions with known inversions.
- **OUTDIR**: Output directory where QC results will be stored.

To use the Python scripts, you can clone this whole repositoy and then copy the `(py scripts reposity)` to (`/work/clwu/GWA_tutorial/`).

```bash
git clone https://github.com/wudaudau/immunegenetic_notes.git
```

Copy to

```bash
cp -r immunegenetic_notes/gwas_qc/py_scripts /your/target/folder/
```

Remove the cloned repo.

```bash
rm -rf immunegenetic_notes
```

## QC1 Missingness

(in the tuto)

### QC1-1 Missing on Variants

Delete SNPs with missingness > 2% and generate new bfiles.

- [ ] We may need a step to copy the bfiles to the output folder. Because we are generating bfiles steps by steps in the output folder.

```bash
plink \
  --bfile DATASET \
  --geno 0.02 \
  --make-bed \
  --out OUTDIR/qc1_1_geno002
```

Output:

- `.log`
- new bfiles
- `.hh`  (heterozygous haploid and nonmale Y chromosome call list) (https://www.cog-genomics.org/plink/1.9/formats#hh) (https://www.cog-genomics.org/plink/1.9/output).

The `.hh` file is the list to keep(?) (nonmissing calls).

```text
96262   796253871713    rs5939319
86827   696700648122    rs5939319
96262   796253871713    rs1419931
96262   236256460571    rs1419931
...
```

### QC1-2 Missing On Individuals

Use the previous output.
Delete individuals with missingness > 5%.

```bash
plink \
  --bfile OUTDIR/qc1_1_geno002 \
  --mind 0.05 \
  --make-bed \
  --out  OUTDIR/qc1_2_mind005
```

Output:

- `.log`
- new bfiles
- `.hh`  (heterozygous haploid and nonmale Y chromosome call list) (https://www.cog-genomics.org/plink/1.9/formats#hh)
- `.irem` FID and IID of the removed individuals (https://www.cog-genomics.org/plink/1.9/output).

`.irem` file

```text
73531   230740255025
55618   796985110241
99493   943052269428
59967   980380935550
14944   538947876752
...
```

Do no remove missing with `--geno` and `--mind` in one-setp command. PLINK remove individuals in prior to SNPs. Marees et al. suggest that SNP filtering should be performed before individual filtering (Table 1).

## QC2 Sex

> Subjects who were a priori determined as females must have a F value of <0.2, and subjects who were a priori determined as males must have a F value >0.8. This F value is based on the X chromosome inbreeding (homozygosity) estimate.

Males have only 1 X chromosome, so regarded as homogeneous (F value >0.8). Females have 2 X chromosomes, so there are certain heterogeneous rate (F value < 0.2).

(Overview of this step ...)

### QC 2-1

Check for sex discrepancy.

```bash
plink \
  --bfile OUTDIR/qc1_2_mind005 \
  --check-sex \
  --out OUTDIR/qc2_1_sexcheck
```

(https://www.cog-genomics.org/plink/1.9/basic_stats#check_sex)

Output:

- `.log`
- `.hh`  (heterozygous haploid and nonmale Y chromosome call list) (https://www.cog-genomics.org/plink/1.9/formats#hh)
- `.sexcheck`

Then, we need to generate a file `sex_discrepancy.txt` using the `.sexcheck` file.

```text
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
python PYDIR/qc2_1_sexcheck.py OUTDIR/qc2_1_sexcheck.sexcheck
```

Output:

- `sex_discrepancy.txt`. A list of inidividual to remove.

### QC2-2 Remove sex discripency

```bash
plink \
  --bfile OUTDIR/qc1_2_mind005 \
  --remove OUTDIR/qc2_sex_discrepancy.txt \
  --make-bed \
  --out OUTDIR/qc2_2_rmsexdic
```

Output:

- `.log`
- new bfiles

## QC3 MAF

> Generate a bfile with autosomal SNPs only and delete SNPs with a low minor allele frequency (MAF).
> A conventional MAF threshold for a regular GWAS is between 0.01 or 0.05, depending on sample size.

General cases:

- Sample size big (how big???), use low threshold (e.g. 0.01).
- Sample size small, use high threshold (e.g. 0.05).

We have ~1000 individuals, use 0.02 as the threshold (1000 * 0.02 = 20).

Steps overview:

- Only focus on autosomal SNPs (Chr 1-22).
- Calculate MAF using `--freq`.
- View MAF distribution to determine the low MAF thereshold. (MAF_check).
- Remove low MAF using `--MAF`.

### QC3-1 Autosomal SNPs only (Chr 1-22)

Select autosomal SNPs only (Chr 1-22) using plink.

```bash
plink \
  --bfile OUTDIR/qc2_2_rmsexdic \
  --chr 1-22 \
  --make-bed \
  --out OUTDIR/qc3_1_chr1_22
```

Output:

- `.log`
- new bfiles

### QC3-2 Check MAF on Chr 1-22

Check MAF on Chr 1-22:

```bash
plink \
  --bfile OUTDIR/qc3_1_chr1_22 \
  --freq \
  --out OUTDIR/qc3_2_chr1_22_MAF_check
```

Output:

- `.log`
- `.frq`

PLINK will generate a log and a `.frq` file, which is a table of MAF (https://www.cog-genomics.org/plink/1.9/basic_stats#freq).

```text
CHR         SNP   A1   A2          MAF  NCHROBS
   1   rs4477212    0    A            0     2036
   1   rs3131972    T    C        0.192     2036
   1  rs11240777    A    G       0.2463     2038
   1   rs4970383    T    G        0.253     2024
   1   rs4475691    T    C        0.213     2038
   1   rs7537756    G    A       0.2198     2038
...
```

```bash
python PYDIR/qc3_2_mafcheck.py OUTDIR/qc3_1_chr1_22_MAF_check.frq 
```

Output:

- `qc3_maf_distribution.png`

### QC3-3 Remove low MAF

Once the MAF threshold is determined, we can drop the low MAF from bfile.

Remove low MAF (0.02):

```bash
plink \
  --bfile OUTDIR/qc3_1_chr1_22 \
  --maf 0.02 \
  --make-bed \
  --out OUTDIR/qc3_3_maf002
```

Output:

- `.log`
- new bfiles

## QC4 HWE

> Delete SNPs which are not in Hardy-Weinberg equilibrium (HWE).

HWE is about the genetic evalution. A basic assumption would be the control group should has no suprise, therefore the HWE check is strick; the case group might associated with evolution, therefore we tolerant more with the HWE control.

Steps overview:

- Use `--hardy` to calculate HWE in a `.hwe` file.
- View the HWE distribution (all and below the threshold, respectively).
- Remove SNPs which are not in HWE from the bfiles (**on all individuals** with a threshold).

### QC4-1 Calculate HWE

```bash
plink \
  --bfile OUTDIR/qc3_3_maf002 \
  --hardy \
  --out OUTDIR/qc4_1_maf002_hardy
```

Output:

- `.log`
- `.hwe`

`--hardy` writes a list of genotype counts and Hardy-Weinberg equilibrium exact test statistics to plink.hwe. With the 'midp' modifier, a mid-p adjustment is applied (see --hwe for discussion). 'gz' causes the output file to be gzipped. (https://www.cog-genomics.org/plink/1.9/basic_stats#hardy)

This will generate a `.hwe` file (https://www.cog-genomics.org/plink/1.9/basic_stats#hardy). It is a big file. The columns are: "CHR", "SNP", "TEST", "A1", "A2", "GENO", "O(HET)", "E(HET)", and "P".

```text
CHR         SNP     TEST   A1   A2                 GENO   O(HET)   E(HET)            P 
   1   rs3131972      ALL    T    C           34/323/661   0.3173   0.3103       0.5444
   1   rs3131972      AFF    T    C              2/15/20   0.4054   0.3817            1
   1   rs3131972    UNAFF    T    C              4/50/92   0.3425   0.3184       0.4456
   1  rs11240777      ALL    A    G           72/358/589   0.3513   0.3713      0.09131
   ...
```

Run the `hwe.py` to generate the hwe (P) and zoomhwe **(P < 0.00001)** in histograms (Histogram HWE and Histogram HWE: strongly deviating SNPs only) in the output folder.

```bash
python PYDIR/qc4_1_hwe.py OUTDIR/qc4_1_maf002_hardy.hwe
```

Output:

- `hwe_distribution.png`
- `hwe_distribution_below_threshold.png`

### QC4-2 Filter HWE

Filter HWE **on all individuals** using 1e-10 as the threshold. (Add `--hwe-all` to filter HWE on all individuals rather than only control ones.)

Here, because we filter on all individuals instead of on control only, use a small threshold.

The general steps would be to filtre more strickly (p value below 1e-6) on the control group.

```bash
plink \
  --bfile OUTDIR/qc3_3_maf002 \
  --hwe 1e-10 \
  --hwe-all \
  --make-bed \
  --out OUTDIR/qc4_2_hweall1em10
```

Output:

- `.log`
- new bfiles

## QC5 LD Pruning

When QC1 to QC4 are done, we can generate the indepSNP tags for the following QC steps.

### QC5-1 Generate indepSNP tags

We need a `inversion.txt` file.

`inversion.txt` is already in the **1_QC_GWAS** package.

```text
6 25500000 33500000 8 HLA
8 8135000 12000000 Inversion8
17 40900000 45000000 Inversion17
```

There are complexe gene regions. We skip them to make the indepSNP tags.

```bash
plink \
  --bfile OUTDIR/qc4_2_hweall1em10 \
  --exclude /work/clwu/GWA_tutorial/1_QC_GWAS/inversion.txt \
  --range \
  --indep-pairwise 50 5 0.5 \
  --out OUTDIR/qc5_indepSNP
```

Output:

- `qc5_indepSNP.log`
- `qc5_indepSNP.prune.in` (exclude)
- `qc5_indepSNP.prune.out` (include)

These commands produce a pruned subset of markers that are in approximate linkage equilibrium with each other, writing the IDs to plink.prune.in (and the IDs of all excluded variants to plink.prune.out). We will use theses file in later steps of QCs.

**Linkage disequilibrium (LD)**, association of alleles on the same chromosome.

Use 0.5 instead of 0.2 here.

The 50 5 0.5 are:

- the window size
- the number of SNPs to shift the window at each step
- the multiple correlation coefficient for a SNP being regressed on all other SNPs simultaneously.

### QC5-2 Prun data

```bash
plink \
  --bfile $OUTDIR/qc4_2_hweall1em10 \
  --extract $OUTDIR/qc5_indepSNP.prune.in \
  --make-bed \
  --out $OUTDIR/qc5_pruned
```

Output:

- `.log`
- new bfiles

## QC6 Heterogzygotie

On pruned data.

### QC6-1 Calculate Heterozygosity on pruned data

`--het` homozygous genotype counts (https://www.cog-genomics.org/plink/1.9/basic_stats#ibc).

- [x] Do I need to focus on the autosome?? -> We already remove the sex chormosome after the sex check.

```bash
plink \
  --bfile OUTDIR/qc5_pruned \
  --het \
  --out OUTDIR/qc6_1_heterogenity_check
```

Output:

- `.log`
- `.het`

`--het` is a statistical option computes observed and expected autosomal homozygous genotype counts for each sample, and reports method-of-moments F coefficient estimates (i.e. (<observed hom. count> - <expected count>) / (<total observations> - <expected count>)) to plink.het.

The output `.het` file is a table similar to `--check-sex` or `--hardy` but not exactly. The columns are: "FID", "IID", "O(HOM)", "E(HOM)", "N(NM)", "F". This file contains your pruned data set.

```text
  FID            IID       O(HOM)       E(HOM)        N(NM)            F
  28328   502088905174       176854    1.852e+05       269885     -0.09841
  99407   971064170845       186259    1.849e+05       269471      0.01576
  94811   869570533760       191215    1.853e+05       270041      0.06975
  19967   957070122174       176705    1.796e+05       260443     -0.03527
  ...
```

### View Heterozygosity

Plot of the heterozygosity rate distribution.

```bash
python PYDIR/qc6_1_heterogenity_check.py OUTDIR/qc6_1_heterogenity_check.het
```

Output:

- `heterozygosity.png`

### QC6-2 Identify heterozygosity outliers

The tutorial says that we use 3 SDs to keep individuals with 3SDs. However, accroding to Sigrid, it's better to adjust the histogram to adapte the filter. We may keep all individulas it no weired values and count presented.

There sould be someting to get a list of individuals to extract or to exclude. -> Create a Py script. Based on the rate (`(df["N(NM)"] - df["O(HOM)"]) / df["N(NM)"]`), ...

Use the following script to generate a outlier list with None as the threshold. ("3sd")

```bash
python PYDIR/qc6_1_heterogenity_outlier.py OUTDIR/qc6_1_heterogenity_check.het None
```

Output:

- `heterozygosity_outliers.txt`

### QC6-3 Remove heterozygosity outliers

```bash
plink \
  --bfile OUTDIR/qc5_pruned \
  --remove OUTDIR/qc6_1_heterozygosity_outliers.txt \
  --make-bed \
  --out OUTDIR/qc6_2_heterozygosity_outliers_removed
```

Output:

- `.log`
- new bfiles

## QC7 IBD

### QC7-1 Calculate IBD

The inputfile can contain family members. We will evaluate the IBD values to determine which individuals to exclude.

Calculates **identity by descent (IBD)** using `--genome` and based on the LD-based purning (https://www.cog-genomics.org/plink/1.9/ibd).

```bash
plink \
  --bfile OUTDIR/qc6_2_heterozygosity_outliers_removed \
  --genome \
  --out OUTDIR/qc7_1_pihat
```

Output:

- `.log`
- `.genome`

`--genome` invokes an IBS/IBD computation over autosomal SNPs (so chrX, chrY, and chrM are excluded), and then writes a report with the following fields to a `.genome` file. `--min` removes "PI_HAT" values below the given cutoff. (https://www.cog-genomics.org/plink/1.9/ibd)

The `.genome` file is a table. The columns are: "FID1", "IID1", "FID2", "IID2", "RT", "EZ", "Z0", "Z1", "Z2", "PI_HAT", "PHE", "DST", "PPC", and "RATIO". **FS means ; PO means parent-offspring; OT means ; UN means unrelated individuals.**

```text
 FID1          IID1   FID2          IID2 RT    EZ      Z0      Z1      Z2  PI_HAT PHE       DST     PPC   RATIO
  28328  502088905174  28328  307365682603 PO   0.5  0.0000  1.0000  0.0000  0.5000   0  0.835098  1.0000 2138.0000
  99407  971064170845  99407  971185421160 PO   0.5  0.0012  0.9877  0.0112  0.5050   0  0.844678  1.0000 1029.7500
  94811  869570533760  94811  762689081855 PO   0.5  0.0000  1.0000  0.0000  0.5000   0  0.831812  1.0000 805.2000
  19967  957070122174  19967  686924389939 PO   0.5  0.0006  0.9794  0.0200  0.5097   0  0.846123  1.0000 2060.5000
  55266  665620090147  66647  153562611492 UN    NA  0.5451  0.4549  0.0000  0.2274  -1  0.772260  1.0000  2.9549
  35898  778566416157  35898  219811218558 PO   0.5  0.0007  0.9851  0.0143  0.5068   0  0.845211  1.0000      NA
  ...
```

**PI_HAT** is Proportion IBD, i.e. P(IBD=2) + 0.5*P(IBD=1). It indicates the "family distance" between the two individuals:

- 1: identical or twins (100% identical)
- 0.5: parent or child (50% identical)
- 0.25: cousins
- we use 0.2 to exclue individuals within the family

col RT:

- Relationship type inferred from .fam/.ped file
- **FS means ; PO means parent-offspring; OT means ; UN means unrelated individuals.**

col EZ:

- IBD sharing expected value, based on just .fam/.ped relationship

Select based on **"PI_HAT"**.

For each row of "PI_HAT" < threshold, there are two IID. We need to check the **MAF** of them to determin which one to be removed from the individuals of study. Normally, we drop the low MAF one.  

The data contain family members and we keep them for HLA imputation. Because

- HLA imputation (like SNP2HLA) does not require unrelated samples.
- Relatedness does not harm the imputation.
- Family samples might even help a little in imputation because shared haplotypes are more accurately phased.

### QC7-2 Extract potential duplicates

Extract PI_HET > 0.98 to obtain potential duplicates.

```bash
awk '$10 > 0.98' $OUTDIR/qc7_1_pihat.genome > $OUTDIR/qc7_2_duplicates_to_check.txt
```

Output:

- `qc7_2_duplicates_to_check.txt`

### QC7-3 Check duplicates

If FID1 == FID2 AND PI_HAT ≥ 0.99 → assume true monozygotic twins → KEEP. If FID1 ≠ FID2 with PI_HAT ≈ 1.0 → likely technical duplicate → REMOVE one sample.

Keep only pairs where FID1 ≠ FID2 (i.e., not true twins). Keep PI_HAT ≥ 0.98. Get FID2, IID2 to be the ID to remove.

```bash
awk '($1!=$3) {print $3, $4}' $OUTDIR/qc7_2_duplicates_to_check.txt > $OUTDIR/qc7_3_duplicates_to_remove.txt
```

Output:

- `qc7_3_duplicates_to_remove.txt`

### QC7-4 Remove duplicates

```bash
plink \
  --bfile $OUTDIR/qc6_2_heterozygosity_outliers_removed \
  --remove $OUTDIR/qc7_3_duplicates_to_remove.txt \
  --make-bed \
  --out $OUTDIR/qc7_4_duplicate_removed
```

Output:

- `.log`
- new bfiles

## QC8 PCA

PCA can view population. We need data of one clean population to impute HLA.

Why do we need to control on pupulation?

- HLA reference panels (like T1DGC, Pan-Asian, etc.) are usually population-specific.
- If you impute across mixed ancestries, your imputation accuracy will suffer badly.
- Also, population stratification can confound association results.

### QC8-1 Run PCA

```bash
plink \
  --bfile $OUTDIR/qc7_4_duplicate_removed \
  --pca \
  --out $OUTDIR/qc8_1_pca
```

Output:

- `.log`
- `.eigenval`
- `.eigenvec`

### Plot PCA

```bash
python py_script/qc8_1_plot_pca.py $OUTDIR/qc8_1_pca.eigenvec
```

Output:

- `qc8_1_pca.png` PCA plot with phenotypes.

### pca to keep

How to select individuals based on PCA clusters? Manually or automatically define a selection boundary (e.g., PC1 between -0.05 and 0.05, PC2 between -0.1 and 0.1). If we select automatically, we can determin the threshold to exclude the outliers.

We put the range of PC1 pos, PC1 neg, PC2 pos, and PC2 neg. We take PC1 between -0.05 and 0.5 and PC2 between -0.1 and 0.1 in this example.

```bash
python py_script/qc8_2_pca_to_keep.py $OUTDIR/qc8_1_pca.eigenvec 0.05 -0.05 0.1 -0.1
```

Output:

- `qc8_2_pca_to_keep.txt`

It's a list of individual with PC1 and PC2 in the range.

### QC8-2 keep pca

```bash
plink \
  --bfile $OUTDIR/qc7_4_duplicate_removed \
  --keep $OUTDIR/qc8_2_pca_to_keep.txt \
  --make-bed \
  --out $OUTDIR/qc8_2_pca_done
```

Output:

- `.log`
- new bfiles
