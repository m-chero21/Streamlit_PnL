import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Gross Margin Calculator",
    page_icon= "logo2.png",
    layout="wide"
)
st.markdown(
    """
    <style>
    /* Hide Streamlit header, including GitHub icons */
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

primary_clr = st.get_option("theme.primaryColor")
txt_clr = st.get_option("theme.textColor")
theme = st.get_option("theme.font")
mode = st.get_option("theme.base")

nav_logo = "logo2.png"
LOGO_PATH = "logo.png"
st.sidebar.image(LOGO_PATH, use_container_width=True)

# Add custom CSS to center the title
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center; /* Center the title */
        font-size: 36px; /* Adjust font size if needed */
        font-weight: bold;
        color: black; /* Optional: Change title color */
        margin-top: 20px; /* Adjust spacing above the title */
        margin-bottom: 20px; /* Adjust spacing below the title */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add the centered title


# Add custom CSS for the navigation bar
st.markdown(
    """
    <style>
    .navbar {
        background-color: #F4F6FF; /* Set background color */
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .navbar-logo {
        display: flex;
        align-items: center;
        color: white !important;
        font-size: 24px;
        font-weight: bold;
        text-decoration: none;
    }
    .navbar-logo img{
        height: 40px; /* Adjust size */
        margin-right: 10px;
    }
    .navbar-links {
        display: flex;
        margin-left: auto; /* Push navigation items to the right */
        gap: 20px; /* Space between navigation items */
    }
    .navbar-link {
        color: black !important; /* Change font color to white */
        font-size: 18px;
        text-decoration: none;
        font-weight: normal;
        padding: 5px 10px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .navbar-link:hover {
        background-color: #a4343a; /* Darker background on hover */
        color: white !important; 
    }
    .navbar-button {
        background-color: #007278; /* Button color */
        color: white !important; /* Change button text color to white */
        font-size: 18px;
        padding: 5px 15px;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .navbar-button:hover {
        background-color: #a4343a /* Darker button on hover */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add the navigation bar
st.markdown(
    """
    <div class="navbar">
                <div class="navbar-links">
            <a href="https://integrated-seed-and-gross-margin-calculator.streamlit.app/" class="navbar-link">Seed Requirement Calculator </a>
            <a href="https://gross-margin-calculator.streamlit.app/" class="navbar-button">Gross Margin Calculator</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="centered-title">Gross Margin Calculator</div>', unsafe_allow_html=True)

primary_clr = st.get_option("theme.primaryColor")
txt_clr = st.get_option("theme.textColor")
theme = st.get_option("theme.font")
mode = st.get_option("theme.base")


# Global CSS for Styling and Aligning Buttons
st.markdown(
    """
    <style>
    div.stButton > button {
        float: right; /* Move the button to the right */
        background-color: #007278; /* Button color */
        color: white !important; /* White text color */
        font-size: 16px; /* Font size */
        font-weight: bold; /* Font weight */
        border: none; /* Remove border */
        border-radius: 5px; /* Rounded corners */
        padding: 10px 20px; /* Padding inside button */
        cursor: pointer; /* Pointer cursor on hover */
        transition: background-color 0.3s ease; /* Smooth hover effect */
        margin: 10px; /* Add some space around the button */
    }
    div.stButton > button:hover {
        background-color: #a4343a; /* Hover color */
        color: white !important; /* Keep text color white on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)




#_____________________________________________________________________________________________

# Load Data
@st.cache_data
def load_data():
    df = pd.read_excel("aggregate_farm_data_template.xlsx")
    cost = pd.read_excel("cost.xlsx")
    return df, cost

df, cost = load_data()

# Sidebar - Global Parameters
st.sidebar.header("Global Parameters")
counties = ["All"] + sorted(df["County"].unique().tolist())
selected_county = st.sidebar.selectbox("County:", counties)

value_chains = ["Maize", "Potatoes", "Rice", "Coffee"]
selected_value_chain = st.sidebar.selectbox("Value Chain:", value_chains)

scale_options = ["Small-scale", "Large-scale"]
selected_scale = st.sidebar.selectbox("Scale of Production:", scale_options)

subsidy_options = ["With Subsidy", "Without Subsidy"]
selected_subsidy = st.sidebar.selectbox("Fertilizer Subsidy:", subsidy_options)

fluctuation_levels = {"Low": 1, "Moderate": 2, "High": 3}
selected_fluctuation = st.sidebar.selectbox("Fluctuation Level:", list(fluctuation_levels.keys()))

currency = st.sidebar.selectbox("Currency:", ["KES", "USD", "Euro"])
exchange_rate = st.sidebar.number_input(
    "Exchange Rate:",
    value=1.0 if currency == "KES" else (0.008 if currency == "USD" else 0.007),
    step=0.001,
    format="%.3f"
)

bag_weight = st.sidebar.number_input("Weight Per Bag (Kg):", value=90.0, step=1.0)
farmgate_price = st.sidebar.number_input("Farmgate Price (KES):", value=28.62, step=1.0)
loss_percentage = st.sidebar.slider("Loss %:", 0, 50, 5)
own_consumption_percentage = st.sidebar.slider("Consumption %:", 0, 50, 10)


# Filter Data
filtered_df = df.copy()
if selected_county != "All":
    filtered_df = filtered_df[filtered_df["County"] == selected_county]
if selected_value_chain != "All":
    filtered_df = filtered_df[filtered_df["Crop Type"] == selected_value_chain]


# Sidebar - Unit Selection for Area
area_unit = st.sidebar.selectbox("Area Unit:", ["Hectares", "Acres"], index=0)
# Conversion Factor
acre_to_hectare = 2.47105  # 1 Hectare = 2.47105 Acres



# Aggregate Metrics
total_production = filtered_df["Production (Tonnes)"].sum()
total_area = filtered_df["Area (Ha)"].sum()
yield_kg = (total_production * 1000) / total_area if total_area > 0 else 0

# Adjust Area Based on Selected Unit
if area_unit == "Acres":
    total_area = total_area * acre_to_hectare  # Convert Hectares to Acres
    yield_kg = (total_production * 1000) / total_area if total_area > 0 else 0
else:
    total_area = total_area  # Use Hectares
    yield_kg = (total_production * 1000) / total_area if total_area > 0 else 0


# Create a DataFrame to organize the metrics
metrics_data = {
    "Indicator": ["Production (Tonnes)", "Area (Ha)", "Yield (MT/Ha)"],
    "Value": [f"{total_production:,.2f}", f"{total_area:,.2f}", f"{yield_kg:,.2f}"],
}



# Convert to a DataFrame
metrics_df = pd.DataFrame(metrics_data)

# Display as a table in the sidebar
st.sidebar.table(metrics_df)


# Filter Cost Data
filtered_costs = cost[
    (cost["Scale of Production"] == selected_scale) &
    (cost["Fertilizer Subsidy"] == selected_subsidy)
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

# Prepare Cost Parameters and Adjust for Exchange Rate
cost_parameters = []
for col, category in category_mapping.items():
    if col in filtered_costs.columns:
        # Apply the exchange rate dynamically
        raw_value = float(filtered_costs[col].iloc[0])  # Original value from the filtered costs
        value = round(raw_value * exchange_rate)  # Adjusted for exchange rate
        std_dev = value * (0.01 * fluctuation_levels[selected_fluctuation])  # Calculate standard deviation
        lower_bound = round(value - 1.96 * std_dev)  # Confidence interval lower bound
        upper_bound = round(value + 1.96 * std_dev)  # Confidence interval upper bound

        cost_parameters.append({
            "Item": col.replace(" (KES)", ""),
            "Category": category,
            "Quantity": int(filtered_costs["Quantity"].iloc[0]) if "Quantity" in filtered_costs else 1,
            "Cost Per Unit": value,
            "Confidence Interval": f"[{lower_bound}, {upper_bound}]",
        })

# Convert to DataFrame for Display
cost_df = pd.DataFrame(cost_parameters)
# Convert to DataFrame for Display
if "cost_df" not in st.session_state:
    st.session_state.cost_df = pd.DataFrame(cost_parameters)
else:
    # Ensure the table dynamically updates based on changes in exchange rate or other parameters
    st.session_state.cost_df = pd.DataFrame(cost_parameters)

# Display Cost Breakdown Section
st.markdown(
    """
    <style>
    .cost-breakdown-title {
        color: #007278; /* Set text color */
        font-size: 35px; /* Adjust font size if needed */
        font-weight: bold;
        text-align: left; /* Align text to the left */
        margin-bottom: 10px; /* Add some space below the title */
    }
    </style>
    <div class="cost-breakdown-title">Cost Breakdown</div>
    """,
    unsafe_allow_html=True
)

# Add or Edit Items Dynamically in the Table
if "add_item_expanded" not in st.session_state:
    st.session_state.add_item_expanded = False

# Button to expand or collapse the Add Item section
if st.button("Insert New Cost"):
    st.session_state.add_item_expanded = not st.session_state.add_item_expanded

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

        if st.button("Update", key="confirm_add_item"):
            # Create a new row with the entered data
            new_row = {
                "Item": new_item,
                "Category": new_category,
                "Quantity": new_quantity,
                "Cost Per Unit": new_cost_per_unit,
                "Confidence Interval": new_confidence_interval,
            }

            # Update the session state DataFrame
            st.session_state.cost_df = pd.concat(
                [st.session_state.cost_df, pd.DataFrame([new_row])], ignore_index=True
            )

            st.success(f"Item '{new_item}' added successfully!")

# Display the Updated Cost Breakdown Table
st.dataframe(st.session_state.cost_df, use_container_width=True)



# Gross Margin Calculation
def calculate_gross_margin(cost_df, yield_kg, farmgate_price, loss_percentage, own_consumption_percentage):
    gross_output = yield_kg * farmgate_price * exchange_rate
    post_harvest_loss = gross_output * (loss_percentage / 100)
    own_consumption = gross_output * (own_consumption_percentage / 100)
    net_output = gross_output - (post_harvest_loss + own_consumption)
    
    total_costs = cost_df["Cost Per Unit"].sum()
    gross_margin = net_output - total_costs
    
    return gross_output, net_output, gross_margin

gross_output, net_output, gross_margin = calculate_gross_margin(
    cost_df, yield_kg, farmgate_price, loss_percentage, own_consumption_percentage
)

# Calculate Best and Worst Case Scenarios
std_dev = gross_margin * (0.01 * fluctuation_levels[selected_fluctuation])
best_case_gross_margin = gross_margin + 1.96 * std_dev
worst_case_gross_margin = gross_margin - 1.96 * std_dev

# Break-Even Analysis
def calculate_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit):
    if selling_price_per_unit > variable_cost_per_unit:
        break_even_quantity = fixed_costs / (selling_price_per_unit - variable_cost_per_unit)
        break_even_revenue = break_even_quantity * selling_price_per_unit

        # Calculate variability for worst and best case scenarios
        break_even_quantity_std_dev = break_even_quantity * (0.01 * fluctuation_levels[selected_fluctuation])
        worst_case_quantity = break_even_quantity - 1.96 * break_even_quantity_std_dev
        best_case_quantity = break_even_quantity + 1.96 * break_even_quantity_std_dev

        return break_even_quantity, break_even_revenue, worst_case_quantity, best_case_quantity
    return None, None, None, None

fixed_costs = cost_df[cost_df["Category"] == "Fixed Cost"]["Cost Per Unit"].sum()
variable_costs = cost_df[cost_df["Category"] == "Variable Cost"]["Cost Per Unit"].sum()
variable_cost_per_unit = variable_costs / yield_kg if yield_kg > 0 else 0

break_even_quantity, break_even_revenue, worst_case_quantity, best_case_quantity = calculate_break_even(fixed_costs, variable_cost_per_unit, farmgate_price)

# Required Price to Break Even
required_price_to_break_even = (fixed_costs + variable_costs) / yield_kg if yield_kg > 0 else None

st.markdown(
    """
    <style>
    .cost-breakdown-title {
        color: #007278; /* Set text color */
        font-size: 35px; /* Adjust font size if needed */
        font-weight: bold;
        text-align: left; /* Align text to the left */
        margin-bottom: 10px; /* Add some space below the title */
    }
    </style>
    <div class="cost-breakdown-title">Results Summary</div>
    """,
    unsafe_allow_html=True
)

summary_data = [
    {"Indicator": f"Farmgate Price ({currency})", "Value": f"{farmgate_price*exchange_rate:,.2f} {currency}"},
    {"Indicator": "Break-Even Quantity (Bags)", "Value": f"{break_even_quantity / bag_weight:,.2f}" if break_even_quantity is not None else "N/A"},
    {"Indicator": "Break-Even Quantity (Kg)", "Value": f"{break_even_quantity:,.2f}" if break_even_quantity is not None else "N/A"},
    # {"Indicator": "Worst-Case Break-Even Quantity (Kg)", "Value": f"{worst_case_quantity:,.2f}" if worst_case_quantity is not None else "N/A"},
    # {"Indicator": "Best-Case Break-Even Quantity (Kg)", "Value": f"{best_case_quantity:,.2f}" if best_case_quantity is not None else "N/A"},
    
    {"Indicator": f"Break-Even Price ({currency})", "Value": f"{required_price_to_break_even:,.2f} {currency}" if required_price_to_break_even is not None else "N/A"},
    {"Indicator": f"Gross Margin ({currency})", "Value": f"{gross_margin:,.2f}" if best_case_quantity is not None else "N/A"},
    # {"Indicator": "Worst-Case Gross Margin", "Value": f"{worst_case_gross_margin:,.2f} {currency}"},
    # {"Indicator": "Best-Case Gross Margin", "Value": f"{best_case_gross_margin:,.2f} {currency}"},
]

summary_df = pd.DataFrame(summary_data)

st.markdown(
    summary_df.style
    .set_table_styles([
        {"selector": "thead", "props": [("background-color", "#007278"), ("color", "white"), ("font-size", "18px")]},
        {"selector": "tbody td", "props": [("font-size", "16px"), ("text-align", "center"), ("padding", "10px")]}])
    .hide(axis="index")
    .to_html(),
    unsafe_allow_html=True,
)



import plotly.graph_objects as go

# Break-Even Plot Function
def plot_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit):
    units = np.arange(0, 2000, 10)
    total_costs = fixed_costs + variable_cost_per_unit * units
    total_revenue = selling_price_per_unit * units

    # Create interactive Plotly figure
    fig = go.Figure()

    # Add Total Costs line
    fig.add_trace(
        go.Scatter(
            x=units,
            y=total_costs,
            mode='lines',
            name='Total Costs',
            line=dict(color='#a4343a', width=2)
        )
    )

    # Add Total Revenue line
    fig.add_trace(
        go.Scatter(
            x=units,
            y=total_revenue,
            mode='lines',
            name='Total Revenue',
            line=dict(color='#37B7C3', width=2)
        )
    )

    # Add Break-Even Point line
    fig.add_trace(
        go.Scatter(
            x=[break_even_quantity, break_even_quantity],
            y=[0, max(total_costs.max(), total_revenue.max())],
            mode='lines',
            name='Break-Even Point',
            line=dict(color='#000000', dash='dash')
        )
    )

    # Layout and labels
    fig.update_layout(
        xaxis_title='Units Produced/Sold',
        yaxis_title='Cost/Revenue',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="seaborn",
        width=700,  # Set plot width
        height=600   # Set plot height
    )

    return fig

# Cost and Revenue Distribution Plot Function
def plot_cost_and_revenue_distribution(categories, values, currency):
    # Create Plotly bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=categories,
                y=values,
                text=[f"{value:,.2f}" for value in values],  # Add formatted values as text
                textposition='auto',
                marker=dict(color=["#007278", "#6295A2", "#80B9AD", "#B3E2A7"])  # Set bar colors
            )
        ]
    )

    # Layout and labels
    fig.update_layout(
        xaxis_title='Category',
        yaxis_title=f'Value ({currency})',
        template="seaborn",
        bargap=0.2,
        width=700,  # Set plot width
        height=600   # Set plot height
    )

    return fig

# Define categories and values
categories = ["Gross Output", "Net Output", "Total Costs", "Gross Margin"]
values = [gross_output, net_output, cost_df["Cost Per Unit"].sum(), gross_margin]

# Use Streamlit Columns to Place Plots Side by Side
col1, col2 = st.columns(2)  # Create two columns

with col1:
    # Title for Break-Even Plot
    st.markdown(
    """
    <style>
    .cost-breakdown-title {
        color: #007278; /* Set text color */
        font-size: 35px; /* Adjust font size if needed */
        font-weight: bold;
        text-align: left; /* Align text to the left */
        margin-bottom: 10px; /* Add some space below the title */
    }
    </style>
    <div class="cost-breakdown-title">Break-Even Analysis</div>
    """,
    unsafe_allow_html=True
)
    # Break-Even Plot
    if break_even_quantity is not None:
        st.plotly_chart(plot_break_even(fixed_costs, variable_cost_per_unit, farmgate_price), use_container_width=False)

with col2:
    # Title for Cost and Revenue Distribution Plot
    st.markdown(
    """
    <style>
    .cost-breakdown-title {
        color: #007278; /* Set text color */
        font-size: 35px; /* Adjust font size if needed */
        font-weight: bold;
        padding: 10px;
        text-align: left; /* Align text to the left */
        margin-bottom: 10px; /* Add some space below the title */
    }
    </style>
    <div class="cost-breakdown-title">Cost and Revenue Distribution</div>
    """,
    unsafe_allow_html=True
)
    # Cost and Revenue Distribution Plot
    st.plotly_chart(plot_cost_and_revenue_distribution(categories, values, currency), use_container_width=False)
