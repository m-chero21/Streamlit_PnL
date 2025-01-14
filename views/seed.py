import streamlit as st
from views.side_seed import render_sidebar
from utils.styling import apply_global_styling, render_navigation_bar
from config.seed_data import Data

class Seed:
    # Streamlit Page Configuration
    st.set_page_config(
        page_title="Seed Requirement Calculator",
        page_icon="assets/logo2.png",
        layout="wide"
    )

    # Apply Global CSS Styling
    apply_global_styling()

    # Navigation Bar
    render_navigation_bar()

    # Main Title
    st.markdown('<div class="centered-title">Seed Requirement Calculator</div>', unsafe_allow_html=True)

    # Initialize Data
    data = Data()

    # Render Sidebar and Get Inputs
    seed_rate, selected_counties, new_biotech_percentage, update_button = render_sidebar(data.df)

    if update_button:
        # Update Percentages and Recalculate Metrics
        for county in selected_counties:
            data.df.loc[data.df["County"] == county, "2028 % of Biotech"] = new_biotech_percentage
        data.calculate_projections(seed_rate)

    # Display Metrics
    st.dataframe(data.df)
