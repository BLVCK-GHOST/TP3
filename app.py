import streamlit as st
import pandas as pd
import plotly.express as px
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, fic_export_data
import logging
import os
import glob

def remove_data(df: pd.DataFrame, last_n_samples: int = 4*24):
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
