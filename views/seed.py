import streamlit as st
from views.side_seed import render_sidebar
from config.seed_data import Data

def seed():
    # Page Configuration
    st.title("Seed Requirement Calculator")
    # Set the favicon
    st.markdown("""
        <link rel="icon" href="assets/logo2.png">
    """, unsafe_allow_html=True)

    # Main Title
    st.markdown('<div class="centered-title">Seed Requirement Calculator</div>', unsafe_allow_html=True)

    # Initialize Data
    data = Data()

    # Render Sidebar and Get Inputs
    seed_rate, selected_counties, default_opv_2023, default_opv_2028, biotech_2023, biotech_2028, update_button = render_sidebar(data.df)

    # Display Updated Metrics
    # Ensure projections are calculated
    data.calculate_projections(seed_rate)
    summary_df = data.calculate_summary_metrics(selected_counties)

    # Display Summary Table
    st.markdown(
        """
        <div class="cost-breakdown-title">Summary</div>
        """,
        unsafe_allow_html=True,
    )
    st.write(summary_df)

    st.markdown(
        """
        <div class="cost-breakdown-title">Calculator</div>
        """,
        unsafe_allow_html=True
    )

    if update_button:
        # Update Percentages and Recalculate Metrics
        for county in selected_counties:
            # Filter the dataframe by county and update columns
            data.df.loc[data.df["County"] == county, ["2023 % of Biotech", "2028 % of Biotech"]] = [biotech_2023, biotech_2028]
            
            # Optionally update default OPV values if needed
            data.df.loc[data.df["County"] == county, ["2023 % of OPV", "2028 % of OPV"]] = [default_opv_2023, default_opv_2028]
        data.calculate_projections(seed_rate)

    # Display Metrics
    st.dataframe(data.df)

