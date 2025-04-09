#!/bin/sh

# === User-defined inputs ===
DATASET="input/bfiles/LEAP_FreezeV3_1563_May2020_PSC2"   # no .bed/.bim/.fam extension
PYDIR="py_script" # path to the directory where the python scripts are located
INVERSIONTXT="1_QC_GWAS/inversion.txt"
OUTDIR="output/LEAP_FreezeV3_1563_May2020_PSC2"

GENO=0.02
MIND=0.05
MAF=0.02
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
plink --bfile $OUTDIR/qc1_2_mind --check-sex --out $OUTDIR/qc2_1_sexcheck

python py_script/qc2_1_sexcheck.py $OUTDIR/qc2_1_sexcheck.sexcheck

# QC2-2 Remove sex discripency
plink --bfile $OUTDIR/qc1_2_mind --remove $OUTDIR/qc2_sex_discrepancy.txt --make-bed --out $OUTDIR/qc2_2_rmsexdic





# QC3 MAF

# QC3-1 Autosomal SNPs only (Chr 1-22)
plink --bfile $OUTDIR/qc2_2_rmsexdic --chr 1-22 --make-bed --out $OUTDIR/qc3_1_chr1_22

# QC3-2 Check MAF on Chr 1-22
plink --bfile $OUTDIR/qc3_1_chr1_22 --freq --out $OUTDIR/qc3_2_chr1_22_MAF_check

python py_script/qc3_2_mafcheck.py $OUTDIR/qc3_2_chr1_22_MAF_check.frq

# QC3-3 Remove low MAF
plink --bfile $OUTDIR/qc3_1_chr1_22 --maf $MAF --make-bed --out $OUTDIR/qc3_3_maf


# QC4 WHE

# QC4-1 Calculate HWE
plink --bfile $OUTDIR/qc3_3_maf --hardy --out $OUTDIR/qc4_1_maf_hardy

python py_script/qc4_1_hwe.py $OUTDIR/qc4_1_maf_hardy.hwe

# QC4-2 Filter HWE **on all individuals** using 1e-10 as the threshold. (Add `--hwe-all` to filter HWE on all individuals rather than only control ones.)
plink --bfile $OUTDIR/qc3_3_maf --hwe $HWE --hwe-all --make-bed --out $OUTDIR/qc4_2_hweall

# --out qc4_clean


# QC5 LD pruning

# Generate indepSNP tags
# We need the inversion.txt from 1_QC_GWAS of the GWA_tutorial
plink --bfile $OUTDIR/qc4_2_hweall --exclude 1_QC_GWAS/inversion.txt --range --indep-pairwise 50 5 $R2 --out $OUTDIR/qc5_indepSNP

# prun data
plink --bfile $OUTDIR/qc4_2_hweall --extract $OUTDIR/qc5_indepSNP.prune.in --make-bed --out $OUTDIR/qc5_pruned

# QC6 Heterogeneity (on pruned data)

# QC6-1 Heterozygosity on pruned data 
plink --bfile $OUTDIR/qc5_pruned --het --out $OUTDIR/qc6_1_heterogenity_check

# View Heterozygosity
python py_script/qc6_1_heterogenity_check.py $OUTDIR/qc6_1_heterogenity_check.het

# Identify heterozygosity outliers ("3sd" or None)
python py_script/qc6_1_heterogenity_outlier.py $OUTDIR/qc6_1_heterogenity_check.het None

# QC6-2 Remove heterozygosity outliers
plink --bfile $OUTDIR/qc5_pruned --remove $OUTDIR/qc6_1_heterozygosity_outliers.txt --make-bed --out $OUTDIR/qc6_2_heterozygosity_outliers_removed



# QC7 IBD (Keep family members, so only remove duplicates)

# QC7-1 Calculate IBD
plink --bfile $OUTDIR/qc6_2_heterozygosity_outliers_removed --genome --out $OUTDIR/qc7_1_pihat

# QC7-2 Extract potential duplicates
awk '$10 > 0.98' $OUTDIR/qc7_1_pihat.genome > $OUTDIR/qc7_2_duplicates_to_check.txt

# QC7-3 Check duplicates
awk '($1!=$3) {print $3, $4}' $OUTDIR/qc7_2_duplicates_to_check.txt > $OUTDIR/qc7_3_duplicates_to_remove.txt

# QC7-4 Remove duplicates
plink --bfile $OUTDIR/qc6_2_heterozygosity_outliers_removed --remove $OUTDIR/qc7_3_duplicates_to_remove.txt --make-bed --out $OUTDIR/qc7_4_duplicate_removed

# QC8 PCA

# QC8-1 Run PCA
plink --bfile $OUTDIR/qc7_4_duplicate_removed --pca --out $OUTDIR/qc8_1_pca

# plot pca
python py_script/qc8_1_plot_pca.py $OUTDIR/qc8_1_pca.eigenvec

# pca to keep
python py_script/qc8_2_pca_to_keep.py $OUTDIR/qc8_1_pca.eigenvec 0.05 -0.05 0.1 -0.1

# QC8-2 keep pca
plink --bfile $OUTDIR/qc7_4_duplicate_removed --keep $OUTDIR/qc8_2_pca_to_keep.txt --make-bed --out $OUTDIR/qc8_2_pca_done


