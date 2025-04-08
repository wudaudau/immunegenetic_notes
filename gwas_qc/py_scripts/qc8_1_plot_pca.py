"""
"""


import pandas as pd
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

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

def read_fam_file(f_path:str) -> pd.DataFrame:
    """
    f_path: str. The path to the fam file (.fam).

    Read the fam file and return a DataFrame.
    The first two columns are FID and IID.
    """
    df = pd.read_table(f_path, header=None, sep=r"\s+") # No header
    # Rename the columns
    df.columns = ["FID", "IID", "PID", "MID", "SEX", "PHENOTYPE"]
    
    return df

def plot_pca(df_pca:pd.DataFrame, df_fam:pd.DataFrame, save_path:str) -> None:
    """
    df_pca: DataFrame. The dataframe of the PCA file.
    df_fam: DataFrame. The dataframe of the fam file.
        The fam file contains the FID, IID, and PHENOTYPE columns.
        We will use the PHENOTYPE column to color the PCA plot.
    save_path: str. The repository to save the PCA plot.
        Without "/" in the end.
    """
    # Merge the PCA and fam dataframes on FID and IID
    df_pca.index = df_pca[["FID", "IID"]].apply(lambda x: '_'.join(x.values.astype(str)), axis=1)
    df_fam.index = df_fam[["FID", "IID"]].apply(lambda x: '_'.join(x.values.astype(str)), axis=1)
    df_pca = df_pca.merge(df_fam[["PHENOTYPE"]], left_index=True, right_index=True, how="left")

    df_pca["PHENOTYPE"] = df_pca["PHENOTYPE"].map({1: "1 Control", 2: "2 Case", -9: "-9 Missing"})

    # Plot the PCA
    plt.figure(figsize=(10, 6)) # TODO: adjust the figure size
    sns.scatterplot(data=df_pca, x="PC1", y="PC2", hue="PHENOTYPE", alpha=0.7)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA Plot")
    plt.grid()

    # plot vline and hline at 0
    plt.axvline(x=0, color='gray', linestyle='dashed', linewidth=1)
    plt.axhline(y=0, color='gray', linestyle='dashed', linewidth=1)

    # Fill between PC1 between -0.05 and 0.05 and PC2 between -0.1 and 0.1 (including the threshold)
    plt.fill_betweenx(y=[-0.1, 0.1], x1=-0.05, x2=0.05, color='gray', alpha=0.2)

    # equal aspect ratio
    plt.gca().set_aspect('equal', adjustable='box')

    
    # Save the plot
    plt.savefig(f"{save_path}/qc8_1_pca.png")
    print(f"PCA plot is saved in {save_path}/qc8_1_pca.png")
    print()
    # plt.show()
    plt.close()


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

    # TODO: We will optimize the code to read the fam file and pca file.
    f_fam = f"{folder}/qc7_4_duplicate_removed.fam"
    df_fam = read_fam_file(f_fam)
    print("=== Fam Data ===")
    print(df_fam.shape)
    print(df_fam.head())
    print()

    df_pca = read_pca_file(file_path)
    print("=== PCA Data ===")
    print(df_pca.shape)
    print(df_pca.head())
    print()

    # Plot the PCA
    plot_pca(df_pca, df_fam, folder)
    


    
