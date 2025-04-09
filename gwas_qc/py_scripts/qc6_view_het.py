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

def plot_het_distribution(df:pd.DataFrame, save_path:str) -> None:
    """
    df: DataFrame. The dataframe of the heterogeneity file.
    save_path: str. The repository to save the heterogeneity distribution plot.
        Without "/" in the end.

    Plot the heterogeneity distribution.
    Save the plot as a PNG file.
    """

    df["HET_RATE"] = (df["N(NM)"] - df["O(HOM)"]) / df["N(NM)"]

    # Plot the distribution of heterogeneity
    plt.figure(figsize=(10, 6))
    plt.hist(df["HET_RATE"], bins=50, color='blue', alpha=0.7)
    plt.xlabel("Heterogeneity")
    plt.ylabel("Frequency")
    plt.title(f"Heterogeneity Rate")
    plt.grid()

    # Indicate the mean and standard deviation
    mean = df["HET_RATE"].mean()
    std = df["HET_RATE"].std()
    plt.axvline(mean, color='red', linestyle='dashed', linewidth=1)
    plt.axvline(mean + std, color='green', linestyle='dashed', linewidth=1)
    plt.axvline(mean - std, color='green', linestyle='dashed', linewidth=1)
    plt.axvline(mean + 2 * std, color='orange', linestyle='dashed', linewidth=1)
    plt.axvline(mean - 2 * std, color='orange', linestyle='dashed', linewidth=1)
    plt.axvline(mean + 3 * std, color='purple', linestyle='dashed', linewidth=1)
    plt.axvline(mean - 3 * std, color='purple', linestyle='dashed', linewidth=1)
    plt.legend(['Mean', 'Mean ± 1 Std', 'Mean ± 2 Std', 'Mean ± 3 Std'])
    # Save the plot

    plt.savefig(f"{save_path}/qc6_1_heterozygosity.png")
    # plt.show()
    plt.close()

if __name__ == "__main__":
    
    print("=== Heterogenity Check ===")
    print()
    
    # file_path = "task/T20250405_develop_gwas_qc_py_scripts/input/qc5_homozygous_check.het"
    file_path = sys.argv[1] 
    print(f"file_path: {file_path}")
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

    # Check the heterogeneity distribution
    plot_het_distribution(df_het, folder)
    print(f"Heterogeneity distribution plot is saved in {folder}.")
    print()