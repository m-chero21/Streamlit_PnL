
import streamlit as st
from utils.file_operations import load_css
from utils.calculations import update_combined_summary_metrics
from utils.data_imports import df
from components.sidebar import sidebar_seed
import pandas as pd
load_css()
def seed():
    LOGO_PATH = "assets/images/logos/SAFIC - Light.png"
    st.sidebar.image(LOGO_PATH, use_container_width=True)
    st.markdown('<div class="centered-title">Seed Requirement Calculator</div>', unsafe_allow_html=True)
    filtered_c_df, seed_rate, selected_counties, new_biotech_percentage, update_button = sidebar_seed()

    # Add calculated columns
    filtered_c_df["Hectares 2028"] = (filtered_c_df["Hectares 2023"] * (1 + filtered_c_df["G% Hectares (2023-2028)"] / 100)).round(1)
    filtered_c_df["2023 kg seed OPV"] = (filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of OPV"] / 100 * seed_rate).round(1)
    filtered_c_df["2023 kg seed Hybrid"] =(filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of Hybrid"] / 100 * seed_rate).round(1)
    filtered_c_df["2023 kg seed Biotech"] = (filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of Biotech"] / 100 * seed_rate).round(1)
    filtered_c_df["2028 kg seed OPV"] = (filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of OPV"] / 100 * seed_rate).round(1)
    filtered_c_df["2028 kg seed Hybrid"] = (filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of Hybrid"] / 100 * seed_rate).round(1)
    filtered_c_df["2028 kg seed Biotech"] = (filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of Biotech"] / 100 * seed_rate).round(1)

    filtered_c_df["Production Volume 2023"] = (
        filtered_c_df["Avg Yield OPV"] * filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of OPV"] / 100 +
        filtered_c_df["Avg Yield Hybrid"] * filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of Hybrid"] / 100 +
        (filtered_c_df["Avg Yield Biotech"] * filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of Biotech"] / 100).fillna(0)
    ).round(1)

    filtered_c_df["Production Volume 2028"] = (
        filtered_c_df["Avg Yield OPV"] * filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of OPV"] / 100 +
        filtered_c_df["Avg Yield Hybrid"] * filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of Hybrid"] / 100 +
        filtered_c_df["Avg Yield Biotech"] * filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of Biotech"] / 100
    ).round(1)

    # The logic to handle updates
    if update_button:
        for county in selected_counties:
            
            filtered_c_df.loc[df["County/State"] == county, "2028 % of Biotech"] = new_biotech_percentage
            
            remaining_percentage = 100 - new_biotech_percentage
            
    
            filtered_c_df.loc[df["County/State"] == county, "2028 % of OPV"] = round(30 / (30 + 70) * remaining_percentage)
            filtered_c_df.loc[df["County/State"] == county, "2028 % of Hybrid"] = (
                100 - new_biotech_percentage - filtered_c_df.loc[df["County/State"] == county, "2028 % of OPV"]
            )
            
            
            filtered_c_df.loc[df["County/State"] == county, "2028 kg seed Biotech"] = (
                filtered_c_df.loc[df["County/State"] == county, "Hectares 2028"] *
                filtered_c_df.loc[df["County/State"] == county, "2028 % of Biotech"] / 100 * seed_rate
            )
            
            filtered_c_df.loc[df["County/State"] == county, "Production Volume 2028"] = (
                filtered_c_df.loc[df["County/State"] == county, "Avg Yield OPV"] *
                filtered_c_df.loc[df["County/State"] == county, "Hectares 2028"] *
                filtered_c_df.loc[df["County/State"] == county, "2028 % of OPV"] / 100 +
                filtered_c_df.loc[df["County/State"] == county, "Avg Yield Hybrid"] *
                filtered_c_df.loc[df["County/State"] == county, "Hectares 2028"] *
                filtered_c_df.loc[df["County/State"] == county, "2028 % of Hybrid"] / 100 +
                filtered_c_df.loc[df["County/State"] == county, "Avg Yield Biotech"] *
                filtered_c_df.loc[df["County/State"] == county, "Hectares 2028"] *
                filtered_c_df.loc[df["County/State"] == county, "2028 % of Biotech"] / 100
            )
        
    formatted_df = filtered_c_df.copy()

    columns_to_round = ["Avg Yield OPV", "Avg Yield Hybrid", "Avg Yield Biotech"]
    for col in columns_to_round:
        if col in formatted_df.columns:
            formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.1f}" if pd.notnull(x) else x)


    for col in formatted_df.columns:
        if col not in columns_to_round and pd.api.types.is_numeric_dtype(formatted_df[col]):
            formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else x)

    # Render table without showing the "Country" column
    columns_to_display = [col for col in formatted_df.columns if col != "Country"]

    table_style = """
    <div class="custom-table-container">
        {table_html}
    </div>
    """
    update_combined_summary_metrics(filtered_c_df, selected_counties, new_biotech_percentage, pd, st)

    st.markdown(
        """
        <div class="cost-breakdown-title">Calculator</div>
        """,
        unsafe_allow_html=True
    )

    # Render the table
    st.markdown(
        table_style.format(
            table_html=formatted_df[columns_to_display].to_html(index=False, escape=False)
        ),
        unsafe_allow_html=True
    )
