# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, fic_export_data, calculate_average_consumption_per_hour
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
    load_data_from_lag_to_today(lag_days)
    main_process()
    data = pd.read_csv(fic_export_data, parse_dates=[col_date])
    return data

df = load_data(LAG_N_DAYS)

st.subheader("Line Chart of Numerical Data Over Time")

numerical_column = col_donnees

fig = px.line(df, x=col_date, y=col_donnees, title="Consommation en fonction du temps")
st.plotly_chart(fig)

# Calculate average consumption per hour
average_consumption_per_hour = calculate_average_consumption_per_hour(df)

# Display the calculated average consumption per hour
st.subheader("Average Consumption Per Hour of the Day")
fig_avg_consumption_per_hour = px.bar(average_consumption_per_hour, x=average_consumption_per_hour.index, y=average_consumption_per_hour.values, labels={'x':'Hour', 'y':'Average Consumption'})
st.plotly_chart(fig_avg_consumption_per_hour)
