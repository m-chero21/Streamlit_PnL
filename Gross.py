import streamlit as st
st.set_page_config(
    page_title="Gross Margin Calculator",  
    page_icon="logo2.png",  
    layout="wide"
)

LOGO_PATH = "logo.png"
st.image(LOGO_PATH, width = 300) 


# Displaying the title for Global Parameters
st.markdown("<h2 style='color:#007278; font-weight:bold;'>Global Parameters</h2>", unsafe_allow_html=True)
st.markdown("---")
# Adding Production (Tonnes) and Area under cultivation with units
production_unit = st.selectbox("Production Unit:", options=["Tonnes", "Kilograms"])
production_value = st.number_input("Production Value:", value=84000.0, step=1000.0)
area_unit = st.selectbox("Area Unit:", options=["Hectares (Ha)", "Acres"])
area_value = st.number_input("Area under cultivation:", value=47000.0, step=100.0)

# Bag weight and farmgate price
bag_weight = st.number_input("Weight per Bag (Kg):", value=90.0, step=1.0)
farmgate_price = st.number_input("Farmgate Price (KES):", value=65.0, step=1.0)

# Adding a dropdown to choose between USD and Euros for exchange rate
currency = st.selectbox("Currency:", options=["USD", "Euro"])
exchange_rate = st.number_input("Exchange Rate (KES):", value=0.008, step=0.001)

# Loss percentage and own consumption percentage
loss_percentage = st.slider("Loss %:", min_value=0.0, max_value=0.5, value=0.03, step=0.01)
own_consumption_percentage = st.slider("Consumption %:", min_value=0.0, max_value=0.5, value=0.1, step=0.05)

# Function to calculate yield dynamically
def calculate_yield():
    # Get production value in kilograms
    production_conversion = 1000 if production_unit == "Tonnes" else 1
    production_in_kg = production_value * production_conversion

    # Get area value in hectares
    area_conversion = 0.404686 if area_unit == "Acres" else 1
    area_in_ha = area_value * area_conversion

    # Calculate yield only if area > 0
    if area_in_ha > 0:
        yield_kg = round(production_in_kg / area_in_ha, 0)
    else:
        yield_kg = 0
    return yield_kg

# Calculate yield dynamically
yield_kg = calculate_yield()

# Display Yield (Kg/Ha)
st.text_input("Yield (Kg/Ha):", value=f"{yield_kg}", disabled=True)

# Button to trigger update (not strictly necessary in Streamlit since recalculations happen dynamically)
if st.button("Update Values"):
    st.write("Values updated successfully!")

# Display calculated yield for user confirmation
st.markdown(
    f"""
    <div style="display:flex; justify-content:center; align-items:center; height:50px; background-color:#007278; color:white; border-radius:5px; font-size:20px; font-weight:bold;">
        Calculated Yield: {yield_kg} Kg/Ha
    </div>
    """,
    unsafe_allow_html=True
)