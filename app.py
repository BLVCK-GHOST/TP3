import streamlit as st
import pandas as pd
import plotly.express as px
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, calculate_average_consumption_per_hour

LAG_N_DAYS: int = 7

# Title for your app
st.title("Data Visualization App")

# Load data from CSV
@st.cache_data(ttl=15 * 60)
def load_data(lag_days: int):
    load_data_from_lag_to_today(lag_days)
    main_process()
    data = pd.read_csv(fic_export_data, parse_dates=[col_date])
    return data

df = load_data(LAG_N_DAYS)

# Creating a line chart for overall consumption
st.subheader("Line Chart of Numerical Data Over Time")
fig = px.line(df, x=col_date, y=col_donnees, title="Consommation en fonction du temps")
st.plotly_chart(fig)

# Calculate average consumption per hour
average_consumption_per_hour = calculate_average_consumption_per_hour(df)
# Creating a bar chart for average consumption per hour
st.subheader("Average Consumption Per Hour of the Day")
fig_hourly = px.bar(average_consumption_per_hour, x=average_consumption_per_hour.index, y=col_donnees,
                     title="Average Consumption Per Hour of the Day")
st.plotly_chart(fig_hourly)
