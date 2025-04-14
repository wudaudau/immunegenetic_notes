#!/bin/sh

SNP2HLAPROG="/media/toufikNFS3/toufikNFS/MIS/SNP2HLA.csh"

DATASET="/work/clwu/GWA_tutorial/output/LEAP_FreezeV3_1563_May2020_PSC2/qc9_outliers_removed_chr6"   # no .bed/.bim/.fam extension
REFFILE="/work/clwu/SNP2HLA/SNP2HLA_package_v1.0.3/SNP2HLA/HM_CEU_REF"
#REFFILE="/work/clwu/SNP2HLA/SNP2HLA_package_v1.0.3/SNP2HLA/T1DGC_REF"
OUTDIR="/work/clwu/SNP2HLA/SNP2HLA_package_v1.0.3/SNP2HLA/output/LEAP_FreezeV3_1563_May2020_PSC2_HM_CEU_REF"
PLINK="plink"
max_memory=80000 # [mb] (default java mamory = 2Gb, marker window size = 1000)
window_size=1000 # [bp] (default java mamory = 2Gb, marker window size = 1000)



mkdir -p OUTDIR

${SNP2HLAPROG} \
    $DATASET \
    ${REFFILE}  \
    $OUTDIR \
    ${PLINK} \
    $max_memory $window_size






