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

    # OPV Percentage Inputs
    with st.sidebar.expander("Select OPV %", expanded=False):
        default_opv_2023 = st.number_input(
            "2023 OPV %",
            min_value=0,
            max_value=100,
            value=30,
            step=1,
            help="Set the OPV percentage for 2023."
        )
        default_opv_2028 = st.number_input(
            "2028 OPV %",
            min_value=0,
            max_value=100,
            value=30,
            step=1,
            help="Set the OPV percentage for 2028."
        )

    # Biotech Percentage Inputs
    with st.sidebar.expander("Select Biotech %", expanded=False):
        biotech_2023 = st.number_input(
            "2023 Biotech %",
            min_value=0,
            max_value=100,
            value=0,
            step=1,
            help="Specify the biotech percentage for 2023."
        )
        biotech_2028 = st.number_input(
            "2028 Biotech %",
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
    return seed_rate, selected_counties, default_opv_2023, default_opv_2028, biotech_2023, biotech_2028, update_button

