#!/bin/sh

# === User-defined inputs ===
DATASET=""   # no .bed/.bim/.fam extension
PYDIR="py_script" # path to the directory where the python scripts are located
INVERSIONTXT="1_QC_GWAS/inversion.txt"
OUTDIR=""

GENO=0.02
MIND=0.05
MAF=0.01
HWE=1e-10
R2=0.5


# Create output directory
mkdir $OUTDIR

# QC1 Missingness 

# QC1-1 Variants
plink --bfile $DATASET --geno $GENO --make-bed --out $OUTDIR/qc1_1_geno

# QC1-2 Individuals
plink --bfile $OUTDIR/qc1_1_geno --mind $MIND --make-bed --out $OUTDIR/qc1_2_mind


# QC2 Sex

# QC2-1
plink --bfile $OUTDIR/qc1_2_mind --check-sex --out $OUTDIR/qc2_check_sex

python $PYDIR/qc2_1_sexcheck.py $OUTDIR/qc2_check_sex.sexcheck

# QC2-2 Remove sex discripency
plink --bfile $OUTDIR/qc1_2_mind --remove $OUTDIR/qc2_sex_discrepancy.txt --make-bed --out $OUTDIR/qc2_sex





# QC3 MAF
# Autosomal SNPs only (Chr 1-22)

# QC3-1 
plink --bfile $OUTDIR/qc2_sex --chr 1-22 --freq --out $OUTDIR/qc3_chr1_22_freq

python $PYDIR/qc3_2_mafcheck.py $OUTDIR/qc3_chr1_22_freq.frq

# QC3-3 Remove low MAF
plink --bfile $OUTDIR/qc2_sex --chr 1-22 --maf $MAF --make-bed --out $OUTDIR/qc3_maf


# QC4 WHE

# QC4-1 Calculate HWE
plink --bfile $OUTDIR/qc3_maf --hardy --out $OUTDIR/qc4_hardy

python $PYDIR/qc4_1_hwe.py $OUTDIR/qc4_hardy.hwe

# QC4-2 Filter HWE **on all individuals** using 1e-10 as the threshold. (Add `--hwe-all` to filter HWE on all individuals rather than only control ones.)
plink --bfile $OUTDIR/qc3_maf --hwe $HWE --hwe-all --make-bed --out $OUTDIR/qc4_hweall

# --out qc4_clean






# QC5 LD pruning

# Generate indepSNP tags
# We need the inversion.txt from 1_QC_GWAS of the GWA_tutorial
plink --bfile $OUTDIR/qc4_hweall --exclude $INVERSIONTXT --range --indep-pairwise 50 5 $R2 --out $OUTDIR/qc5_indepSNP

# prun data
plink --bfile $OUTDIR/qc4_hweall --extract $OUTDIR/qc5_indepSNP.prune.in --make-bed --out $OUTDIR/qc5_pruned



# QC6 Heterogeneity (on pruned data)

# Calculate heterozygosity on pruned data 
plink --bfile $OUTDIR/qc5_pruned --het --out $OUTDIR/qc6_het

# View Heterozygosity
python $PYDIR/qc6_view_het.py $OUTDIR/qc6_het.het

# Identify heterozygosity outliers ("3sd" or None)
python $PYDIR/qc6_1_heterogenity_outlier.py $OUTDIR/qc6_het.het None



# QC7 IBD (on pruned data) (Keep family members, so only remove duplicates)

# QC7-1 Calculate IBD
plink --bfile $OUTDIR/qc5_pruned --genome --out $OUTDIR/qc7_pihat

# QC7-2 Extract 
awk '$10 > 0.98' $OUTDIR/qc7_pihat.genome > $OUTDIR/qc7_2_duplicates_to_check.txt

# QC7-3 Check duplicates
awk '($1!=$3) {print $3, $4}' $OUTDIR/qc7_2_duplicates_to_check.txt > $OUTDIR/qc7_3_duplicates_to_remove.txt


# QC8 PCA (on pruned data)

# Run PCA
plink --bfile $OUTDIR/qc5_pruned --pca --out $OUTDIR/qc8_pca

# plot pca
python $PYDIR/qc8_1_plot_pca.py $OUTDIR/qc8_pca.eigenvec $OUTDIR/qc5_pruned

# pca to remove
python $PYDIR/qc8_2_pca_to_remove.py $OUTDIR/qc8_pca.eigenvec 0.05 -0.05 0.1 -0.1






# QC9 Prepare for imputation

# Combine Col1 and Col2 of qc6_heterozygosity_outliers.txt, qc7_3_duplicates_to_remove.txt, qc8_pca_to_remove.txt
awk 'NR>1 {print $1, $2}' $OUTDIR/qc6_heterozygosity_outliers.txt > $OUTDIR/qc9_remove.txt
awk 'NR>1 {print $1, $2}' $OUTDIR/qc7_3_duplicates_to_remove.txt >> $OUTDIR/qc9_remove.txt
awk 'NR>1 {print $1, $2}' $OUTDIR/qc8_pca_to_remove.txt >> $OUTDIR/qc9_remove.txt

# Remove qc9_remove.txt from qc4_hweall, do not use pruned data
plink --bfile $OUTDIR/qc4_hweall --remove $OUTDIR/qc9_remove.txt --make-bed --out $OUTDIR/qc9_outliers_removed

# Extract chr6
plink --bfile $OUTDIR/qc9_outliers_removed --chr 6 --make-bed --out $OUTDIR/qc9_outliers_removed_chr6