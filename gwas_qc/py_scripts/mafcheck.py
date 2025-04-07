"""
I can create my own script to plot it or to sort the table by MAF or to aggregate the count by MAF. We need to determine the threshold to contraol on MAF.
"""

import pandas as pd
import sys
from pathlib import Path
import matplotlib.pyplot as plt


def read_frq_file(f_path:str) -> pd.DataFrame:
    """
    f_path: str. The file path of the ".frq" file including the file extention
        ".frq" file is the output of plink --freq
        There are 6 columns: "CHR", "SNP", "A1", "A2", "MAF", and "NCHROBS".

    Read frq file and return the dataframe.
    """
    df = pd.read_table(f_path, header=0, sep=r"\s+")

    return df

def plot_maf_distribution(df:pd.DataFrame, save_path:str) -> None:
    """
    df: DataFrame. The table in the ".frq" file.
    save_path: str. The repository to save the sex_discrepancy.txt file.
        Without "/" in the end.

    Plot the MAF distribution.
    """
    
    # Plot the MAF distribution
    plt.hist(df["MAF"], bins=50, edgecolor='black')
    plt.xlabel('Minor Allele Frequency (MAF)')
    plt.ylabel('Frequency')
    plt.title('MAF Distribution')
    plt.grid(axis='y', alpha=0.75)

    # Plot vertical line at MAF = 0.01
    plt.axvline(x=0.01, color='r', linestyle='--', label='MAF = 0.01')
    # Plot vertical line at MAF = 0.05
    plt.axvline(x=0.05, color='orange', linestyle='--', label='MAF = 0.05')
    plt.legend()

    # Save the plot
    plt.savefig(f"{save_path}/qc3_maf_distribution.png")


if __name__ == "__main__":

    print("=== MAF check script ===")
    print()
    
    # file_path = "task/T20250405_develop_gwas_qc_py_scripts/input/qc3_1_chr1_22_MAF_check.frq"
    file_path = sys.argv[1] 
    print(f"file_path: {file_path}")
    print()

    file_path = Path(file_path)
    folder = file_path.parent
    f_name = file_path.stem

    print(f"folder: {folder}")
    print(f"file name: {f_name}")
    print()

    df_frq = read_frq_file(file_path)
    print(f"df_frq shape: {df_frq.shape}")
    print(df_frq.head())
    print()

    # Check the MAF distribution
    plot_maf_distribution(df_frq, folder)
    print("=== MAF check script end ===")
    print()