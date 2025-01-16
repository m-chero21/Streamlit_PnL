import streamlit as st

def setup_sidebar(df):
    """Configure the sidebar and capture user inputs."""
    st.sidebar.header("Filters")
    counties = ["All"] + sorted(df["County"].unique())
    selected_county = st.sidebar.selectbox("Select County:", counties)

    value_chains = ["All"] + sorted(df["Crop Type"].unique())
    selected_value_chain = st.sidebar.selectbox("Select Value Chain:", value_chains)

    area_unit = st.sidebar.selectbox("Area Unit:", ["Hectares", "Acres"])
    fluctuation_level = st.sidebar.selectbox("Fluctuation Level:", ["Low", "Moderate", "High"])
    exchange_rate = st.sidebar.number_input("Exchange Rate:", value=1.0, step=0.01)

    return selected_county, selected_value_chain, area_unit, fluctuation_level, exchange_rate