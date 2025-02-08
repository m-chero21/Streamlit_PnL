import pandas as pd
import streamlit as st

@st.cache_data
def load_csv_data():
    return pd.read_csv("data\country - county - seed - data.csv")

@st.cache_data
def load_excel_data():
    return pd.read_excel("data\country - county - crop - yield.xlsx")

@st.cache_data
def load_cost_data():
    return pd.read_excel("data\country - farmer - costs.xlsx")


# Load datasets
df = load_csv_data()
df2 = load_excel_data()
cost = load_cost_data()