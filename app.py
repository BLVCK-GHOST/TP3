import streamlit as st
import pandas as pd
import plotly.express as px
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, fic_export_data
import logging
import os
import glob

def remove_data(df: pd.DataFrame, last_n_samples: int = 4*3):
    return df.iloc[:-last_n_samples]

logging.basicConfig(level=logging.INFO)

LAG_N_DAYS: int = 7

os.makedirs("data/raw/", exist_ok=True)
os.makedirs("data/interim/", exist_ok=True)

for file_path in glob.glob("data/raw/*json"):
    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        logging.warning(e)

st.title("Data Visualization App")

@st.cache_data(ttl=15 * 60)
def load_data(lag_days: int):
    load_data_from_lag_to_today(lag_days)
    main_process()
    data = pd.read_csv(
        fic_export_data, parse_dates=[col_date]
    )
    return data

df = load_data(LAG_N_DAYS)
df = remove_data(df, last_n_samples=4*24)

st.subheader("Line Chart of Numerical Data Over Time")
numerical_column = col_donnees

fig = px.line(df, x=col_date, y=col_donnees, title="Consommation en fonction du temps")
st.plotly_chart(fig)

df['Hour'] = df[col_date].dt.hour
hourly_avg_consumption = df.groupby('Hour')[col_donnees].mean().reset_index()

st.subheader("Moyenne de la consommation par heure de la journée")
fig_hourly_avg = px.bar(hourly_avg_consumption, x='Hour', y=col_donnees, title="Moyenne de la consommation par heure de la journée")
st.plotly_chart(fig_hourly_avg)

df['DayOfWeek'] = df[col_date].dt.dayofweek
day_mapping = {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 4: 'Vendredi', 5: 'Samedi', 6: 'Dimanche'}
df['DayOfWeek'] = df['DayOfWeek'].map(day_mapping)

daily_avg_consumption = round(df.groupby(df[col_date].dt.date)[col_donnees].sum().mean())

st.subheader("Consommation moyenne par jour")
st.write("La consommation moyenne par jour est de:", daily_avg_consumption)

# Adding table for number of lines lost between March 26th and March 27th
start_date = "2024-03-26"
end_date = "2024-03-27"
filtered_df = df[(df[col_date] >= start_date) & (df[col_date] <= end_date)]
num_lines_lost = len(df) - len(filtered_df)

st.subheader("Number of Lines Lost between March 26th and March 27th")
st.write(f"The number of lines lost between {start_date} and {end_date} is: {num_lines_lost}")

# Displaying the latest date
latest_date = df.iloc[-1][col_date]  # Getting the latest date from the DataFrame
st.subheader("Latest Date in the Dataset")
st.write(f"The latest date in the dataset is: {latest_date}")
