import streamlit as st
from config.margin_data import Data
from views.side_margin import setup_sidebar

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
    selected_county, selected_value_chain, area_unit, fluctuation_level, exchange_rate = setup_sidebar(data.df)

    # Gross Margin Calculation
    farmgate_price = st.sidebar.number_input("Farmgate Price (KES):", value=38.89, step=1.0)
    loss_percentage = st.sidebar.slider("Post-Harvest Loss %:", 0, 50, 5)
    own_consumption_percentage = st.sidebar.slider("Own Consumption %:", 0, 50, 10)

    # Filter Data Based on Sidebar Inputs
    filtered_df = data.filter_data(selected_county, selected_value_chain)

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

    break_even = data.calculate_break_even(fixed_costs, variable_cost_per_unit, farmgate_price)
    break_even_quantity = break_even["break_even_quantity"]
    break_even_revenue = break_even["break_even_revenue"]

    # Display Results
    st.header("Gross Margin Calculator")

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

