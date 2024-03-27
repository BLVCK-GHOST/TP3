import streamlit as st
import pandas as pd
import plotly.express as px
from src.process_data import col_date, col_donnees, main_process, fic_export_data, calculate_average_daily_consumption
import logging
import os
import glob

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
    main_process()
    data = pd.read_csv(fic_export_data, parse_dates=[col_date])
    return data

df = load_data(LAG_N_DAYS)

st.subheader("Line Chart of Numerical Data Over Time")
numerical_column = col_donnees
fig = px.line(df, x=col_date, y=col_donnees, title="Consommation en fonction du temps")
st.plotly_chart(fig)

df['Hour'] = df[col_date].dt.hour
hourly_avg_consumption = df.groupby('Hour')[col_donnees].mean().reset_index()

st.subheader("Moyenne de la consommation par heure de la journée")
fig_hourly_avg = px.bar(hourly_avg_consumption, x='Hour', y=col_donnees, title="Moyenne de la consommation par heure de la journée")
st.plotly_chart(fig_hourly_avg)

average_daily_consumption = calculate_average_daily_consumption(df)
st.write(f"Average Daily Consumption: {average_daily_consumption}")
