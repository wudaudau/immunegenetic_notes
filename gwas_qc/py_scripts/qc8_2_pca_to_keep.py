"""
"""

import pandas as pd
import sys
from pathlib import Path


def read_pca_file(f_path:str) -> pd.DataFrame:
    """
    f_path: str. The path to the PCA file (.eigenvec).

    Read the PCA file and return a DataFrame.
    The first two columns are FID and IID.
    """
    df = pd.read_table(f_path, header=None, sep=r"\s+") # No header
    # Rename the columns
    df.columns = ["FID", "IID"] + [f"PC{i}" for i in range(1, df.shape[1] - 1)]
    
    return df

def keep_pca_by_range(df_pca:pd.DataFrame, pc1_p:float, pc1_n:float, pc2_p:float, pc2_n:float) -> pd.DataFrame:
    """
    df_pca: DataFrame. The dataframe of the PCA file.
    pc1_p: float. The positive range for PC1.
    pc1_n: float. The negative range for PC1.
    pc2_p: float. The positive range for PC2.
    pc2_n: float. The negative range for PC2.

    Return the df with the PCA data in the specified range.
    """
    df_pca = df_pca[(df_pca["PC1"] > pc1_n) & (df_pca["PC1"] < pc1_p) & (df_pca["PC2"] > pc2_n) & (df_pca["PC2"] < pc2_p)]

    return df_pca

def save_pca_to_keep(df:pd.DataFrame, save_path:str) -> None:
    """
    df: DataFrame. The dataframe of the PCA to keep.
    save_path: str. The repository to save the PCA data to keep.
        Without "/" in the end.
    """
    df.to_csv(f"{save_path}/qc8_2_pca_to_keep.txt", sep="\t", index=False)


if __name__ == "__main__":

    print("=== Plot PCA ===")
    print()

    # file_path = "task/T20250405_develop_gwas_qc_py_scripts/output/qc8_pca.eigenvec"
    file_path = sys.argv[1]
    print(f"file_path: {file_path}")
    print()

    file_path = Path(file_path)
    folder = file_path.parent
    f_name = file_path.stem

    print(f"folder: {folder}")
    print(f"file name: {f_name}")
    print()

    df_pca = read_pca_file(file_path)
    print("=== PCA Data ===")
    print(df_pca.shape)
    print(df_pca.head())
    print()

    # Keep the PCA data in the specified range
    pc1_p = float(sys.argv[2])
    pc1_n = float(sys.argv[3])
    pc2_p = float(sys.argv[4])
    pc2_n = float(sys.argv[5])
    print("Range for PCA data to keep:")
    print(f"pc1_p: {pc1_p}")
    print(f"pc1_n: {pc1_n}")
    print(f"pc2_p: {pc2_p}")
    print(f"pc2_n: {pc2_n}")
    print()

    df_pca_to_keep = keep_pca_by_range(df_pca, pc1_p, pc1_n, pc2_p, pc2_n)
    print("=== PCA Data to Keep ===")
    print(df_pca_to_keep.shape)
    print(df_pca_to_keep.head())
    print()

    # Save the PCA data to keep
    save_pca_to_keep(df_pca_to_keep, folder)
    print(f"qc8_2_pca_to_keep.txt is saved in {folder}")
    print()