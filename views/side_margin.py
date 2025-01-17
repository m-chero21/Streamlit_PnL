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

    with st.sidebar.expander("Currency Metrics: ", expanded=False):
        currency = st.selectbox("Currency:", ["KES", "USD", "Euro"])
        exchange_rate = st.number_input("Exchange Rate:", value=1.0, step=0.01)

    # Gross Margin Calculation
    with st.sidebar.expander("Data Metrics: ", expanded=False):
        bag_weight = st.number_input("Weight Per Bag (Kg):", value=90.0, step=1.0)
        farmgate_price = st.number_input("Farmgate Price (KES):", value=38.89, step=1.0)
        loss_percentage = st.slider("Post-Harvest Loss %:", 0, 50, 5)
        own_consumption_percentage = st.slider("Own Consumption %:", 0, 50, 10)
        

    return selected_county, selected_value_chain, area_unit, fluctuation_level, currency, bag_weight, farmgate_price, exchange_rate, loss_percentage, own_consumption_percentage