"""
"""

import pandas as pd
import sys
from pathlib import Path
import matplotlib.pyplot as plt


def read_genome_file(f_path:str) -> pd.DataFrame:
    """
    f_path: str. The path to the genome file (.genome).
    """
    df = pd.read_table(f_path, header=0, sep=r"\s+")

    return df

def extract_ibd_outliers(df:pd.DataFrame, threshold:float=0.2) -> pd.DataFrame:
    """
    df: DataFrame. The dataframe of the genome file.
    threshold: float. The threshold to filter the outliers.
        Default: 0.2
        The IBD values below this threshold are considered as outliers.

    Outliers are those with PI_HAT < threshold.
    Return the df with outliers.
    """
    df_outliers = df[df["PI_HAT"] < threshold]

    return df_outliers

def save_ibd_outliers(df:pd.DataFrame, save_path:str) -> None:
    """
    df: DataFrame. The dataframe of the genome outliers.
    save_path: str. The repository to save the genome outliers.
        Without "/" in the end.
    """
    df.to_csv(f"{save_path}/ibd_outliers.txt", sep="\t", index=False) # TODO: add "qc6_" in the file name.


if __name__ == "__main__":

    print("=== IBD Check ===")
    print()
    
    file_path = "task/T20250405_develop_gwas_qc_py_scripts/input/qc6_pihat_min0.2.genome"
    threshold = 0.2
    # file_path = sys.argv[1] 
    # threshold = float(sys.argv[2])
    print(f"file_path: {file_path}")
    print(f"threshold: {threshold}")
    print()

    df_ibd = read_genome_file(file_path)
    print(f"df_ibd shape: {df_ibd.shape}")
    print(df_ibd.head())
    print()

    # Extract the IBD outliers
    df_ibd_outliers = extract_ibd_outliers(df_ibd, threshold)
    print(f"df_ibd_outliers shape: {df_ibd_outliers.shape}")
    print(df_ibd_outliers)
    print()