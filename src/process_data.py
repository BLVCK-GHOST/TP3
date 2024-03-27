# process_data.py

import pandas as pd
from typing import List
import os
import glob
from pathlib import Path
import json

col_date: str = "date_time"  # Update the column name if necessary
col_donnees: str = "consommation"
cols: List[str] = [col_date, col_donnees]
fic_export_data: str = "data/interim/data.csv"


def load_data():
    list_fic: list[str] = [Path(e) for e in glob.glob("data/raw/*json")]
    list_df: list[pd.DataFrame] = []
    for p in list_fic:
        with open(p, "r") as f:
            dict_data: dict = json.load(f)
            df: pd.DataFrame = pd.DataFrame.from_dict(dict_data.get("results"))
            list_df.append(df)

    df: pd.DataFrame = pd.concat(list_df, ignore_index=True)
    return df


def format_data(df: pd.DataFrame):
    # Print out column names to verify
    print("Column names:", df.columns)
    
    # typage
    df[col_date] = pd.to_datetime(df[col_date])
    # ordre
    df = df.sort_values(col_date)
    # filtrage colonnes
    df = df[cols]
    # dédoublonnage
    df = df.drop_duplicates()
    return df


def export_data(df: pd.DataFrame):
    os.makedirs("data/interim/", exist_ok=True)
    df.to_csv(fic_export_data, index=False)


def calculate_average_consumption_per_hour(df: pd.DataFrame):
    # Extract hour from the date column
    df['Hour'] = df[col_date].dt.hour
    
    # Group by hour and calculate the mean consumption for each hour
    average_consumption_per_hour = df.groupby('Hour')[col_donnees].mean()
    
    return average_consumption_per_hour


def main_process():
    df: pd.DataFrame = load_data()
    df = format_data(df)
    export_data(df)


if __name__ == "__main__":
    main_process()
