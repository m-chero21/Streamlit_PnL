import streamlit as st
from utils.styling import render_summary_table
from config.margin_data import Data
from components.side_margin import setup_sidebar

def margin():
    # Page Configuration
    st.title("Gross Margin Calculator")
    # Set the favicon
    st.markdown("""
        <link rel="icon" href="assets/logo.png">
    """, unsafe_allow_html=True)

    # Constants
    CURRENCY_EXCHANGE_RATES = {"KES": 1, "USD": 0.008, "Euro": 0.007}

    # Sidebar Config
    st.session_state.update({
        "selected_county": None,
        "selected_value_chain": None,
        "selected_scale": "Small-scale",
        "selected_subsidy": "With Subsidy",
        "selected_fluctuation": "Low",
        "currency": "KES",
        "exchange_rate": CURRENCY_EXCHANGE_RATES["KES"],
        "bag_weight": 90.0,
        "farmgate_price": 38.89,
        "loss_percentage": 5,
        "own_consumption_percentage": 10,
        "cost_df": None
    })

    # Load Data
    data = Data("resources/aggregate_farm_data_template.xlsx")

    # Sidebar Inputs
    (selected_county, selected_value_chain, selected_subsidy, area_unit, fluctuation_level, currency, bag_weight, 
     farmgate_price, exchange_rate, loss_percentage, own_consumption_percentage) = setup_sidebar(data.df)

    # Filter Data Based on Sidebar Inputs
    filtered_df = data.filter_data(selected_county, selected_value_chain, selected_subsidy)

    # Aggregate Metrics
    total_production, total_area, yield_kg  = data.calculate_aggregate_metrics(filtered_df, area_unit)

    # Adjust Costs
    adjusted_costs = data.adjust_costs(area_unit, exchange_rate, fluctuation_level)

    # Display Aggregate Metrics
    st.sidebar.markdown("### Aggregate Metrics")
    st.sidebar.metric("Total Production (Tonnes)", f"{total_production:,.2f}")
    st.sidebar.metric(f"Total Area ({area_unit})", f"{total_area:,.2f}")
    st.sidebar.metric("Yield (kg/Area)", f"{yield_kg:,.2f}")

    gross_output, net_output, gross_margin = data.calculate_gross_margin(
        adjusted_costs, farmgate_price, loss_percentage, own_consumption_percentage
    )

    # Break-Even Analysis
    fixed_costs = adjusted_costs[adjusted_costs["Category"] == "Fixed Cost"]["Cost Per Unit"].sum()
    variable_costs = adjusted_costs[adjusted_costs["Category"] == "Variable Cost"]["Cost Per Unit"].sum()
    variable_cost_per_unit = variable_costs / yield_kg if yield_kg else 0

    break_even_quantity, break_even_revenue = data.calculate_break_even(fixed_costs, variable_cost_per_unit, farmgate_price)

    required_price_to_break_even = (fixed_costs + variable_costs) / yield_kg 

    # Display Results
    st.markdown(
        """
        <div class="cost-breakdown-title">Cost Breakdown</div>
        """,
        unsafe_allow_html=True
    )

    # Display Metrics
    st.dataframe(adjusted_costs)

    st.markdown(
        """
        <div class="cost-breakdown-title">Results Summary</div>
        """,
        unsafe_allow_html=True
    )

    # Create summary data
    summary_df = data.create_summary_data(
        farmgate_price=farmgate_price,
        exchange_rate=exchange_rate,
        break_even_quantity=break_even_quantity,
        bag_weight=bag_weight,
        required_price_to_break_even=required_price_to_break_even,
        gross_margin=gross_margin,
        gross_output=gross_output,
        currency=currency
    )

    # Layout for table and story side by side
    col1, col2 = st.columns([1, 1])

    # Display the summary table on the left
    with col1:
        render_summary_table(summary_df)

    # Display the story on the right
    with col2:
        st.markdown(
            f"""
            <div class="summary-story">
            At the farmgate price of <b>{farmgate_price * exchange_rate:,.2f} {currency}</b>, 
            the break-even quantity is estimated at <b>{break_even_quantity / bag_weight:,.2f} bags</b> 
            or <b>{break_even_quantity:,.2f} kg</b>. To break even, the required price is 
            <b>{required_price_to_break_even:,.2f} {currency}</b>. The gross margin stands at 
            <b>{gross_margin:,.2f} {currency}</b>, while the gross output is <b>{gross_output:,.2f} {currency}</b>.
            </div>
            """,
            unsafe_allow_html=True,
        )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Break-Even Analysis")
        if break_even_quantity:
            st.write(f"Break-Even Quantity: {break_even_quantity:,.2f} units")
            st.write(f"Break-Even Revenue: {break_even_revenue:,.2f} KES")
        st.plotly_chart(data.plot_break_even(fixed_costs, variable_cost_per_unit, farmgate_price))

    with col2:
        st.subheader("Cost and Revenue Distribution")
        categories = ["Gross Output", "Net Output", "Total Costs", "Gross Margin"]
        values = [gross_output, net_output, adjusted_costs["Cost Per Unit"].sum(), gross_margin]
        st.plotly_chart(data.plot_cost_and_revenue_distribution(categories, values))

