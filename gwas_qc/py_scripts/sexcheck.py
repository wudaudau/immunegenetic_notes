"""
TODO: The R script generate 3 figures (Sex check, Female check, and Male check). Do we need to generate the figures?
    - If we make the figures, we can put the thresholds (femail < 0.2; male > 0.8) in the figure.
"""

import sys
from pathlib import Path

import pandas as pd

def read_sexcheck_file(f_path:str) -> pd.DataFrame:
    """
    f_path: str. The file path of the ".sexcheck" file including the file extention 

    ".sexcheck" file is the output of plink --check-sex
    There are 6 columns: "FID", "IID", "PEDSEX", "SNPSEX", "STATUS", and "F"

    Read the dataframe and return it as a DataFrame.
    """
    df = pd.read_table(f_path, header=0, sep=r"\s+")

    return df

def filter_status_not_ok(df:pd.DataFrame) -> pd.DataFrame:
    """
    df: DataFrame. The table in the ".sexcheck" file.

    Keep only where "STATUS" is NOT "OK".
    Return the df.
    """
    return df[df["STATUS"] != "OK"]

def keep_female_below_threshold(df:pd.DataFrame, threshold:float=0.25) -> pd.DataFrame:
    """
    df: DataFrame. Normally, it's the df return from filter_status_not_ok()
    threshold: float. Default: 0.25
        The Female ("PEDSEX") F should be below 0.2. 
        We could adjust the threshold to adapt our need, e.g use 0.25 to keep more females. 

    What we want are those to eliminate in the QC step.
    We need to keep the females("PEDSEX" == 2) with "F" > threshold. TODO: Use > or >= ???
    Of cause, we keep all the males from the previous step.

    Return df
    """
    # TODO: To include the message in this function.
    # TODO: 
    #   Print threshold.
    #   Pring those can be kept. With reason.
    #   Print those to be checked in the next step (male check).
    return df[((df["PEDSEX"] == 2) &  (df["F"] > threshold)) | (df["PEDSEX"] == 1)]

def keep_male_about_threshold(df:pd.DataFrame, threshold:float=0.8) -> pd.DataFrame:
    """
    df: DataFrame. Normally, it's the df return from filter_status_not_ok()
    threshold: float. Default: 0.8 TODO: What's the default threshold?

    What we want are those to eliminate in the QC step.
    We need to keep the males("PEDSEX" == 1) with "F" < threshold. TODO: Use < or <= ???
    Of cause, we keep all the females from the previous step.

    Return df
    """
    # TODO: To include the message in this function.
    # TODO: 
    #   Print threshold.
    #   Pring those can be kept. With reason.
    #   Pring ...
    return df[((df["PEDSEX"] == 1) &  (df["F"] < threshold)) | (df["PEDSEX"] == 2)]

def save_sex_discrepancy_txt(df:pd.DataFrame, save_path:str) -> None:
    """
    df: DataFrame. The data to save in the sex_discrepancy.txt
    save_path: str. The repository to save the sex_discrepancy.txt file.
        Without "/" in the end.

    Save to sex_discrepancy.txt in the save_path.
    It will be the file to use in the next QC2
    """
    file = f"{save_path}/sex_discrepancy.txt"
    df.to_csv(file, index=False, sep=' ')
    print(f"{file} is saved.")




if __name__ == "__main__":

    file_path = sys.argv[1] 
    print(f"file_path: {file_path}")

    file_path = Path(file_path)
    folder = file_path.parent
    f_name = file_path.stem

    print(f"folder: {folder}")
    print(f"file name: {f_name}")
    print()


    df_sexcheck = read_sexcheck_file(file_path)
    print(f"df_sexcheck shape: {df_sexcheck.shape}")
    print()

    print("Filter status not OK:")
    df_status_not_ok = filter_status_not_ok(df_sexcheck)
    print(f"df_status_not_ok shape: {df_status_not_ok.shape}")
    print(df_status_not_ok)
    print()

    print("Female check:")
    df_female_check = keep_female_below_threshold(df_status_not_ok)
    print(df_female_check)
    print()

    print("Male check:")
    df_male_check = keep_male_about_threshold(df_female_check)
    print(df_male_check)
    print()

    save_sex_discrepancy_txt(df_male_check, folder)
    