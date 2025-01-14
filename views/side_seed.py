import streamlit as st

def render_sidebar(df):
    # Global Inputs
    st.sidebar.header("Global Inputs")
    seed_rate = st.sidebar.number_input(
        "Seed Rate (kg/h):",
        value=25.0,
        step=1.0,
        help="Specify the seed rate in kilograms per hectare."
    )

    # Scenario Testing Controls
    st.sidebar.header("Scenario Testing")
    selected_counties = st.sidebar.multiselect(
        "Counties:",
        options=df["County"].unique(),
        placeholder="Choose one or more counties",
        help="Select counties for which to test scenarios."
    )

    new_biotech_percentage = st.sidebar.number_input(
        "2028 Biotech %:",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        help="Specify the biotech percentage for 2028."
    )

    update_button = st.sidebar.button(
        "Update",
        help="Click to update metrics based on the selected counties and biotech percentage."
    )

    # Return values for use in the main app
    return seed_rate, selected_counties, new_biotech_percentage, update_button

