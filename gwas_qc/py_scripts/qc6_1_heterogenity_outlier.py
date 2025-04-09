"""
"""

import pandas as pd
import sys
from pathlib import Path
import matplotlib.pyplot as plt


def read_het_file(f_path:str) -> pd.DataFrame:
    """
    f_path: str. The path to the heterogeneity file (.het).
    """
    df = pd.read_table(f_path, header=0, sep=r"\s+")

    return df

def extract_het_outliers(df:pd.DataFrame, conditions:str) -> pd.DataFrame:
    """
    df: DataFrame. The dataframe of the heterogeneity file.
    conditions: str. The conditions to filter the outliers.
        e.g. "3sd" or None
        3sd: those HET_RATE out of 3 standard deviations
        None: No outliers

    Return the df with outliers.
    """
    df["HET_RATE"] = (df["N(NM)"] - df["O(HOM)"]) / df["N(NM)"]

    if conditions == "3sd":
        mean = df["HET_RATE"].mean()
        std = df["HET_RATE"].std()
        df_outliers = df[(df["HET_RATE"] > mean + 3 * std) | (df["HET_RATE"] < mean - 3 * std)]
    elif conditions == None:
        df_outliers = df[(df["HET_RATE"] > df["HET_RATE"].max()) | (df["HET_RATE"] < df["HET_RATE"].min())]

    return df_outliers

def save_het_outliers(df:pd.DataFrame, save_path:str) -> None:
    """
    df: DataFrame. The dataframe of the heterogeneity outliers.
    save_path: str. The repository to save the heterogeneity outliers.
        Without "/" in the end.
    """
    # TODO: Do we need to remove the header?
    df.to_csv(f"{save_path}/qc6_heterozygosity_outliers.txt", sep="\t", index=False)

if __name__ == "__main__":
    
    print("=== Heterogenity Check ===")
    print()
    
    # file_path = "task/T20250405_develop_gwas_qc_py_scripts/input/qc5_homozygous_check.het"
    # conditions = None # "3sd"
    file_path = sys.argv[1] 
    conditions = None if sys.argv[2] == "None" else sys.argv[2]
    print(f"file_path: {file_path}")
    print(f"conditions: {conditions}")
    print()

    file_path = Path(file_path)
    folder = file_path.parent
    f_name = file_path.stem

    print(f"folder: {folder}")
    print(f"file name: {f_name}")
    print()

    df_het = read_het_file(file_path)
    print(f"df_het shape: {df_het.shape}")
    print(df_het.head())
    print()

    # Extract the heterogeneity outliers
    df_het_outliers = extract_het_outliers(df_het, conditions)
    print(f"df_het_outliers shape: {df_het_outliers.shape}")
    print(df_het_outliers.head())
    print()

    # Save the heterogeneity outliers
    save_het_outliers(df_het_outliers, folder)
    print(f"heterozygosity_outliers.txt is saved in {folder}")
    print()