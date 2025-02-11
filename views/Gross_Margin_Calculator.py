import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from components.sidebar import sidebar_gross
from utils.calculations import calculate_gross_margin, calculate_confidence_interval, plot_break_even, plot_cost_and_revenue_distribution, calculate_break_even
from utils.data_imports import df2, cost
from utils.file_operations import load_css
load_css()

def margin():
    st.markdown('<div class="centered-title">Gross Margin Calculator</div>', unsafe_allow_html=True)

<<<<<<< HEAD
    bag_weight, selected_fluctuation, loss_percentage, f_cost, yield_kg, own_consumption_percentage, selling_price_per_unit, selected_scale, selected_subsidy, fluctuation_levels, area_unit, exchange_rate, acre_to_hectare, currency, farmgate_price = sidebar_gross(df2, cost)
=======
    bag_weight, selected_fluctuation, loss_percentage, f_cost, yield_kg, own_consumption_percentage, selling_price_per_unit, selected_scale, selected_subsidy, selected_country, selected_county, fluctuation_levels, area_unit, exchange_rate, acre_to_hectare, currency, farmgate_price = sidebar_gross(df2, cost)
>>>>>>> front-and-backend-update

    # Filter Cost Data
    filtered_costs = f_cost[
        (f_cost["Scale of Production"] == selected_scale) &
        (f_cost["Fertilizer Subsidy"] == selected_subsidy) 
    ]

    # Cost Data Preparation
    category_mapping = {
        "Seed Cost (KES)": "Variable Cost",
        "Fertilizer Cost (KES)": "Variable Cost",
        "Pesticides Cost": "Variable Cost",
        "Herbicides Cost (KES)": "Variable Cost",
        "Machinery Cost (KES)": "Fixed Cost",
        "Labour Cost (KES)": "Variable Cost",
        "Landrent Cost (KES)": "Fixed Cost",
        "Other Costs (KES)": "Other Cost"
    }
    cost_parameters = []
    for col, category in category_mapping.items():
        if col in filtered_costs.columns:
        
            raw_value = float(filtered_costs[col].iloc[0]) 
            if area_unit == "Hectares":
                raw_value *= acre_to_hectare
            else:
                raw_value = raw_value

        
            cost_per_unit = round(raw_value * exchange_rate) 
            
            std_dev = cost_per_unit * (0.01 * fluctuation_levels[selected_fluctuation])
            lower_bound = round(cost_per_unit - 1.96 * std_dev)
            upper_bound = round(cost_per_unit + 1.96 * std_dev)  
            quantity = int(filtered_costs["Quantity"].iloc[0]) if "Quantity" in filtered_costs else 1 
            cost_parameters.append({
                "Item": col.replace(" (KES)", ""),
                "Category": category,
                "Quantity": quantity,
                "Cost Per Unit": cost_per_unit,
                "Confidence Interval": f"[{lower_bound}, {upper_bound}]",

            })

    cost_df = pd.DataFrame(cost_parameters)
    if "cost_df" not in st.session_state:
        st.session_state.cost_df = pd.DataFrame(cost_parameters) 

    st.markdown(
        """
        <div class="cost-breakdown-title">Cost Breakdown</div>
        """,
        unsafe_allow_html=True
    )


    if "add_item_expanded" not in st.session_state:
        st.session_state.add_item_expanded = False

    # Button to expand or collapse the Add Item section
    if st.button("Insert New Cost"):
        st.session_state.add_item_expanded = not st.session_state.add_item_expanded

    # Add Item Section
    if st.session_state.add_item_expanded:
        with st.expander("", expanded=True):
            new_item = st.text_input("Cost Name", "Cost Item")
            new_category = st.selectbox("Category", ["Variable Cost", "Fixed Cost", "Other Cost"])
            new_quantity = st.number_input("Quantity", value=1, min_value=1, step=1)
            new_cost_per_unit = st.number_input("Cost Per Unit", value=0.0, step=1.0)
            
            std_dev = new_cost_per_unit * (0.01 * fluctuation_levels[selected_fluctuation])
            new_lower_bound = round(new_cost_per_unit - 1.96 * std_dev)
            new_upper_bound = round(new_cost_per_unit + 1.96 * std_dev)
            new_confidence_interval = f"[{new_lower_bound}, {new_upper_bound}]"

            if st.button("Add Item", key="confirm_add_item"):
                
                new_row = {
                    "Item": new_item,
                    "Category": new_category,
                    "Quantity": new_quantity,
                    "Cost Per Unit": new_cost_per_unit,
                    "Confidence Interval": new_confidence_interval,
                }
                st.session_state.cost_df = pd.concat(
                    [st.session_state.cost_df, pd.DataFrame([new_row])], ignore_index=True
                )
            
                cost_df = st.session_state.cost_df
                st.success(f"Item '{new_item}' added successfully!")
    #_______________________________________________________________________________________________________________________________


    lower_bound, upper_bound = calculate_confidence_interval(cost_per_unit, std_dev, quantity)
    # Create a temporary DataFrame without the "Confidence Interval" column for display
    temp_df = cost_df.drop(columns=["Confidence Interval"])

    # Build grid options for the temporary DataFrame
    grid_options_builder = GridOptionsBuilder.from_dataframe(temp_df)

    # Configure default columns to be editable
    grid_options_builder.configure_default_column(editable=True)

    # Configure "Category" column as a dropdown
    grid_options_builder.configure_column(
        "Category",
        editable=True,
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": ["Fixed Cost", "Variable Cost", "Other Cost"]},
    )

    # Build the grid options
    grid_options = grid_options_builder.build()

    # Render the editable AgGrid table inside an expander
    with st.expander("Edit Costs", expanded=False):
        response = AgGrid(
            temp_df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.MODEL_CHANGED,  # Track changes in the table
            fit_columns_on_grid_load=True,
            theme="balham",
        )
    # Update the dataframe directly with edited values
    if response['data'] is not None:
        # Update cost_df directly with the edited table
        cost_df = pd.DataFrame(response['data'])

        # Recalculate Confidence Interval for updated rows
        fluctuation_level = fluctuation_levels[selected_fluctuation]
        cost_df["Confidence Interval"] = cost_df.apply(
            lambda row: calculate_confidence_interval(
                row["Cost Per Unit"],
                fluctuation_level,
                row["Quantity"]
            ),
            axis=1
        )
        # Update session state with the new table
        st.session_state.cost_df = cost_df

    # Display the updated table in real-time
    st.markdown('<div class="custom-table-container">', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    #_________________________________________________________________________________________________
            
    # Display the Updated Cost Breakdown Table

    table_style = """
    <div class="custom-table-container">
        {table_html}
    </div>
    """

    table_html = cost_df.to_html(index=False, escape=False)
    st.markdown(table_style.format(table_html=table_html), unsafe_allow_html=True)

    # Calculate the total costs
    total_costs_display = cost_df["Cost Per Unit"].sum()

    # Print the total costs
    st.write(f"The total costs are **{currency} {total_costs_display:,.2f}**")

    gross_output, net_output, gross_margin, real_g_margin = calculate_gross_margin(cost_df, yield_kg, farmgate_price, loss_percentage, own_consumption_percentage)

    # Calculate Best and Worst Case Scenarios
    std_dev = gross_margin * (0.01 * fluctuation_levels[selected_fluctuation])
    best_case_gross_margin = gross_margin + 1.96 * std_dev
    worst_case_gross_margin = gross_margin - 1.96 * std_dev
    

    fixed_costs = cost_df[cost_df["Category"] == "Fixed Cost"]["Cost Per Unit"].sum() 
    variable_costs = cost_df[cost_df["Category"] == "Variable Cost"]["Cost Per Unit"].sum() 
    other_costs= cost_df[cost_df["Category"] == "Other Cost"]["Cost Per Unit"].sum() 
    variable_cost_per_unit = (variable_costs / yield_kg) 

    total_costs = fixed_costs + variable_costs +other_costs
    required_price_to_break_even = (fixed_costs + variable_costs + other_costs) / yield_kg 

    break_even_quantity, break_even_revenue, worst_case_quantity, best_case_quantity = calculate_break_even(selling_price_per_unit, total_costs, fluctuation_levels,selected_fluctuation)


    st.markdown(
        """
        <div class="cost-breakdown-title">Results Summary</div>
        """,
        unsafe_allow_html=True
    )

    summary_data = [
        {
            "Indicator": f"Farmgate Price ({currency})",
            "Value": (
                f"{(farmgate_price):,.2f} {currency}"
            
            ),
        },
        {
            "Indicator": "Break-Even Quantity (Bags)",
            "Value": (
                f"{(break_even_quantity / bag_weight):,.2f}"
                if isinstance(break_even_quantity / bag_weight, (int, float, np.number)) and isinstance(bag_weight, (int, float, np.number))
                else "N/A"
            ),
        },
        {
            "Indicator": "Break-Even Quantity (Kg)",
            "Value": (
                f"{break_even_quantity:,.2f}"
                if isinstance(break_even_quantity, (int, float, np.number))
                else "N/A"
            ),
        },
        {
            "Indicator": f"Break-Even Price ({currency})",
            "Value": (
                f"{required_price_to_break_even:,.2f} {currency}"
                if required_price_to_break_even is not None and isinstance(required_price_to_break_even, (int, float, np.number))
                else "N/A"
            ),
        },
        {
            "Indicator": f"Gross Margin ({currency})",
            "Value": (
                f"{gross_margin:,.2f}"
                if isinstance(gross_margin, (int, float, np.number))
                else "N/A"
            ),
        },
        {
            "Indicator": f"Gross Output ({currency})",
            "Value": (
                f"{gross_output:,.2f}"
                if isinstance(gross_output, (int, float, np.number))
                else "N/A"
            ),
        },
    ]

    summary_df = pd.DataFrame(summary_data)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            summary_df.to_html(classes="summary-table2", escape=False, index = False),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="break-even-container ">
            To achieve a break-even point, the farmer needs to produce <b>{break_even_quantity / bag_weight:,.2f} bags</b> 
            at the current farmgate price of <b>{farmgate_price:,.2f} {currency}</b> per kg. Alternatively, with the current yield of <b>{yield_kg:,.2f} kg/ha</b>, the minimum farmgate price 
            required to break even is <b>{required_price_to_break_even:,.2f} {currency}</b> per kg.
            Currently, the farmer faces a gross margin of <b>{gross_margin:,.2f} {currency}</b>, with a total 
            gross output of <b>{gross_output:,.2f} {currency}</b>, emphasizing the need to optimize production 
            or adjust pricing strategies to move toward profitability.
            </div>
            """,
            unsafe_allow_html=True
        )

    categories = ["Gross Output", "Marketed Output", "Total Costs", "Gross Margin"]
    values = [gross_output, net_output, cost_df["Cost Per Unit"].sum(), gross_margin]
    fig1, total_costs, total_revenue, break_even_point = plot_break_even(fixed_costs, variable_cost_per_unit, farmgate_price)

    fig = plot_cost_and_revenue_distribution(categories, values, currency)
    col1, col2 = st.columns(2) 
    with col1:
    
        st.markdown(
        """
        <div class="cost-breakdown-title">Break-Even Analysis</div>
        """,
        unsafe_allow_html=True
    )
        
        st.plotly_chart(fig1, use_container_width=False, key="Break_Even_Chart")

    with col2:
    
        st.markdown(
        """
        <div class="cost-breakdown-title">Cost and Revenue Distribution</div>
        """,
        unsafe_allow_html=True
    )
        
        st.plotly_chart(plot_cost_and_revenue_distribution(categories, values, currency), use_container_width=False, key="Cost_Breakdown_Chart")