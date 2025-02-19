import streamlit as st
import pandas as pd
from utils.data_imports import df, df2, cost
from utils.calculations import adjust_percentages

def sidebar_seed():
    with st.popover("⚙️ Global Parameters"):
        st.header("Global Parameters")

        # Load country selection
        df['Country'] = df['Country'].dropna().str.strip()
        country = df['Country'].unique()
        selected_country = st.selectbox("Country:", country)

        # Filter the DataFrame based on the selected country
        filtered_c_df = df[df['Country'] == selected_country]

        # Seed rate input
        seed_rate = st.number_input("Seed Rate (kg/h):", value=25.0, step=1.0)

        # OPV Selection
        with st.expander("Select OPV %", expanded=False):
            default_opv_2023 = st.number_input("2023 OPV %", min_value=0, max_value=100, value=30, step=1)
            default_opv_2028 = st.number_input("2028 OPV %", min_value=0, max_value=100, value=30, step=1)

        # Biotech percentage sliders
        biotech_2023 = st.slider("2023 Biotech %", 0, 100, 0)
        biotech_2028 = st.slider("2028 Biotech %", 0, 100, 0)

        # Adjust hybrid and OPV percentages
        opv_2023, hybrid_2023 = adjust_percentages(biotech_2023, default_opv_2023, selected_country)
        opv_2028, hybrid_2028 = adjust_percentages(biotech_2028, default_opv_2028, selected_country)

        # Apply calculated percentages
        filtered_c_df["2023 % of OPV"] = [opv_2023] * len(filtered_c_df)
        filtered_c_df["2023 % of Hybrid"] = [hybrid_2023] * len(filtered_c_df)
        filtered_c_df["2023 % of Biotech"] = [biotech_2023] * len(filtered_c_df)
        filtered_c_df["2028 % of OPV"] = [opv_2028] * len(filtered_c_df)
        filtered_c_df["2028 % of Hybrid"] = [hybrid_2028] * len(filtered_c_df)
        filtered_c_df["2028 % of Biotech"] = [biotech_2028] * len(filtered_c_df)

        # Scenario testing section
        st.header("Scenario Testing")

        # Get unique counties or states
        county_options = filtered_c_df['County/State'].unique()

        # Multi-select counties
        selected_counties = st.multiselect("County/State:", options=county_options, placeholder="Choose a County/State")

        # Biotech percentage update
        new_biotech_percentage = st.number_input("2028 Biotech %:", min_value=0, max_value=100, value=0)

        # Update button
        update_button = st.button("Update")
        st.markdown(f""" <div class="update-county">
            <b>Updated {', '.join(selected_counties)} , the 2028 Biotech  for the selected county/ies is now: {new_biotech_percentage} %</b>
        </div> """, unsafe_allow_html=True)

    return filtered_c_df, seed_rate, selected_counties, new_biotech_percentage, update_button

#______________________________________________________________Gross Margin Galculator_______________________________________________________________________________________

def sidebar_gross(df2, cost):
    with st.popover("⚙️ Global Parameters"):
        st.header("Global Parameters")

        country =sorted(set(df2['Country']).union(set(cost['Country'])))
        selected_country = st.selectbox("Country:", country)
        cost['Country'] = cost['Country'].astype(str).str.strip()

        # Filter the DataFrame based on the selected country
        filtered_c_df = df2[df2['Country'] == selected_country]
        f_cost=  cost[cost['Country'] == selected_country]


        counties = ["All"] + sorted(filtered_c_df["County"].unique().tolist())
        selected_county = st.selectbox("County:", counties)


        # Collapsible section for all cost-related parameters
        with st.expander("Production Variables", expanded=False):

            # Value Chain
            value_chains = ["Maize", "Irish Potatoes", "Coffee"]
            selected_value_chain = st.selectbox("Value Chain:", value_chains)

            # Scale of Production
            # scale_options = f_cost["Scale of Production"].unique()
            # selected_scale = st.selectbox("Scale of Production:", scale_options)
            scale_options = sorted(f_cost["Scale of Production"].unique())  # Sort to ensure ordering

            # Ensure "Small-scale" is selected by default
            default_index = list(scale_options).index("Small-scale") if "Small-scale" in scale_options else 0

            selected_scale = st.selectbox("Scale of Production:", scale_options, index=default_index)

            # Fertilizer Subsidy
            subsidy_options = f_cost["Fertilizer Subsidy"].unique()
            selected_subsidy = st.selectbox("Fertilizer Subsidy:", subsidy_options)

            # Fluctuation Levels
            fluctuation_levels = {"Low": 1, "Moderate": 2, "High": 3}
            selected_fluctuation = st.selectbox("Fluctuation Level:", list(fluctuation_levels.keys()))

            bag_weight = st.number_input("Weight Per Bag (Kg):", value=90.0, step=1.0)


        with st.expander("Currency", expanded=False):
            if selected_country == "Nigeria":
                currency = st.selectbox("Currency:", ["NGN", "USD"])  
                if currency == "NGN":
                    exchange_rate = 11.6
                elif currency == "USD":
                    exchange_rate = 11.6 * 0.3  
            else:
                currency = st.selectbox("Currency:", ["KES", "USD", "Euro"])  
                exchange_rate = st.number_input(
                    "Exchange Rate:",
                    value=1.0 if currency == "KES" else (0.008 if currency == "USD" else 0.007),
                    step=0.001,
                    format="%.3f"
                )


        # Set Farmgate Price dynamically
        default_farmgate_price = 39.1853448276 if selected_country == "Nigeria" else 38.89

        farmgate_price = st.number_input(
            f"Farmgate Price ({currency}):", value=default_farmgate_price*exchange_rate, step=1.0
        )
        loss_percentage = st.slider("Post-Harvest Loss %:", 0, 50, 5)
        own_consumption_percentage = st.slider("Own Consumption %:", 0, 50, 10)

        selling_price_per_unit = farmgate_price

        # Filter Data

        filtered_df = filtered_c_df.copy()
        if selected_county != "All":
            filtered_df = filtered_df[filtered_df["County"] == selected_county]
        if selected_value_chain != "All":
            filtered_df = filtered_df[filtered_df["Crop Type"] == selected_value_chain]


        # Sidebar Area Selector
        area_unit = st.selectbox("Area Unit:", ["Hectares", "Acres"], index=0)
        # Acre conversion
        acre_to_hectare = 2.47105  

        # Aggregate Metrics
        total_production = filtered_c_df["Production (Tonnes)"].sum()
        total_area = filtered_df["Area (Ha)"].sum()
        yield_kg = (total_production * 1000) / total_area 

        # Adjust Area Based on Selected Area Unit
        if area_unit == "Acres":
            total_area = total_area * acre_to_hectare  
            yield_kg = (total_production * 1000) / total_area 
        else:
            total_area = total_area  
            yield_kg = (total_production * 1000) / total_area 


        # Create a DataFrame for the Indicators
        metrics_data = {
            "Indicator": ["Production (Tonnes)", f"Area({area_unit})", "Yield (MT/Ha)"],
            "Value": [f"{total_production:,.2f}", f"{total_area:,.2f}", f"{yield_kg:,.2f}"],
        }


        metrics_df = pd.DataFrame(metrics_data)

        # Convert DataFrame to HTML, exclude index
        html_metrics = metrics_df.to_html(index=False)

        # Display in Streamlit's sidebar without the index
        st.markdown(html_metrics, unsafe_allow_html=True)
    return bag_weight, selected_fluctuation, loss_percentage, f_cost, yield_kg, own_consumption_percentage, selling_price_per_unit, selected_scale, selected_subsidy, fluctuation_levels, area_unit, exchange_rate, acre_to_hectare, currency, farmgate_price
