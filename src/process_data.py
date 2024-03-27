import pandas as pd
from typing import List
import os
import glob
from pathlib import Path
import json

col_date: str = "date_heure"
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
    df[col_date] = pd.to_datetime(df[col_date])
    df = df.sort_values(col_date)
    df = df[cols]
    df = df.drop_duplicates()
    return df


def export_data(df: pd.DataFrame):
    os.makedirs("data/interim/", exist_ok=True)
    df.to_csv(fic_export_data, index=False)


def main_process():
    df: pd.DataFrame = load_data()
    df = format_data(df)
    export_data(df)


def calculate_average_daily_consumption(df: pd.DataFrame):
    daily_consumption = df.groupby(df[col_date].dt.date)[col_donnees].sum()
    average_daily_consumption = daily_consumption.mean()
    return average_daily_consumption


if __name__ == "__main__":
    main_process()
    df = pd.read_csv(fic_export_data, parse_dates=[col_date])
    average_daily_consumption = calculate_average_daily_consumption(df)
    print("Average Daily Consumption:", average_daily_consumption)
