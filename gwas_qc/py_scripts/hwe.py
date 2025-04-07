"""
"""


import pandas as pd
import sys
from pathlib import Path
import matplotlib.pyplot as plt


def read_hwe_file(f_path:str) -> pd.DataFrame:
    """
    f_path: str. The path to the hwe file.
    """
    df = pd.read_table(f_path, header=0, sep=r"\s+")

    return df

def plot_hwe_distribution(df:pd.DataFrame, save_path:str) -> None:
    """
    df: DataFrame. The dataframe of the hwe file.
    save_path: str. The repository to save the sex_discrepancy.txt file.
        Without "/" in the end.

    Plot the HWE distribution.
    Save the plot as a PNG file.
    """

    # Plot the distribution of HWE p-value
    plt.figure(figsize=(10, 6))
    plt.hist(df["P"], bins=50, color='blue', alpha=0.7)
    plt.xlabel("HWE p-value")
    plt.ylabel("Frequency")
    plt.title(f"HWE Distribution")
    plt.grid()
    plt.savefig(f"{save_path}/hwe_distribution.png") # TODO: add "qc3_2_" in the file name.
    # plt.show()
    plt.close()

def plot_zoomhwe_distribution(df_hwe:pd.DataFrame, save_path:str, threshold:float=0.00001):
    """
    df_hwe: DataFrame. The dataframe of the hwe file.
    save_path: str. The repository to save the sex_discrepancy.txt file.
        Without "/" in the end.
    threshold: float. The threshold to zoom in the HWE p-value.

    Plot the zoomed-in HWE distribution.
    Save the plot as a PNG file.
    """
    df_zoomed = df_hwe[df_hwe["P"] < threshold]

    # Plot the zoomed-in distribution of HWE p-value
    plt.figure(figsize=(10, 6))
    plt.hist(df_zoomed["P"], bins=50, color='red', alpha=0.7)
    plt.xlabel("HWE p-value")
    plt.ylabel("Frequency")
    plt.title(f"Zoomed-in HWE Distribution (P < {threshold})") # Histogram HWE: strongly deviating SNPs only
    plt.grid()

    # Add a vertical line at 1e-6, 1e-7, 1e-8, 1e-9, 1e-10
    plt.axvline(x=1e-6, color='green', linestyle='--', label='1e-6')
    plt.axvline(x=1e-7, color='orange', linestyle='--', label='1e-7')
    plt.axvline(x=1e-8, color='purple', linestyle='--', label='1e-8')
    plt.axvline(x=1e-9, color='brown', linestyle='--', label='1e-9')
    plt.axvline(x=1e-10, color='pink', linestyle='--', label='1e-10')
    plt.legend()

    # x-axis in log scale
    plt.xscale('log')

    plt.savefig(f"{save_path}/hwe_distribution_below_threshold.png") # TODO: add "qc3_2_" in the file name.
    # plt.show()
    plt.close()


if __name__ == "__main__":

    print("=== HWE check script ===")
    print()
    
    # file_path = "task/T20250405_develop_gwas_qc_py_scripts/input/qc3_2_maf001_hardy.hwe"
    file_path = sys.argv[1] 
    print(f"file_path: {file_path}")
    print()

    file_path = Path(file_path)
    folder = file_path.parent
    f_name = file_path.stem

    print(f"folder: {folder}")
    print(f"file name: {f_name}")
    print()

    df_hwe = read_hwe_file(file_path)
    print(f"df_hwe shape: {df_hwe.shape}")
    print(df_hwe.head())
    print()

    # Check the HWE distribution
    print("Plotting HWE distribution...")
    plot_hwe_distribution(df_hwe, folder)
    print("HWE distribution plotted.")
    print()

    # Plot the zoomed-in HWE distribution
    print("Plotting zoomed-in HWE distribution...")
    threshold = 0.00001
    print(f"Threshold: {threshold}")
    plot_zoomhwe_distribution(df_hwe, folder, threshold)
    print("Zoomed-in HWE distribution plotted.")
    print()