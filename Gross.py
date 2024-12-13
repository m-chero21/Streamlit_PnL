import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Gross Margin Calculator",
    page_icon= "logo2.png",
    layout="wide"
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
st.markdown('<div class="centered-title">Gross Margin Calculator</div>', unsafe_allow_html=True)

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
            <a href="https://seed-requirement-calculator.streamlit.app/" class="navbar-link">Seed Requirement Calculator </a>
            <a href="https://gross-margin-calculator.streamlit.app/" class="navbar-button">Gross Margin Calculator</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

primary_clr = st.get_option("theme.primaryColor")
txt_clr = st.get_option("theme.textColor")
theme = st.get_option("theme.font")
mode = st.get_option("theme.base")
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
farmgate_price = st.sidebar.number_input("Farmgate Price (KES):", value=65.0, step=1.0)
loss_percentage = st.sidebar.slider("Loss %:", 0, 50, 5)
own_consumption_percentage = st.sidebar.slider("Consumption %:", 0, 50, 10)

# Filter Data
filtered_df = df.copy()
if selected_county != "All":
    filtered_df = filtered_df[filtered_df["County"] == selected_county]
if selected_value_chain != "All":
    filtered_df = filtered_df[filtered_df["Crop Type"] == selected_value_chain]

# Aggregate Metrics
total_production = filtered_df["Production (Tonnes)"].sum()
total_area = filtered_df["Area (Ha)"].sum()
yield_kg = (total_production * 1000) / total_area if total_area > 0 else 0

# Display Sidebar Metrics
st.sidebar.markdown(f"**Production (Tonnes):** {total_production:,.2f}")
st.sidebar.markdown(f"**Area (Ha):** {total_area:,.2f}")
st.sidebar.markdown(f"**Yield (Kg/Ha):** {yield_kg:,.2f}")

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

cost_parameters = []
for col, category in category_mapping.items():
    if col in filtered_costs.columns:
        value = round(float(filtered_costs[col].iloc[0]) * exchange_rate)
        std_dev = value * (0.01 * fluctuation_levels[selected_fluctuation])
        lower_bound = round(value - 1.96 * std_dev)
        upper_bound = round(value + 1.96 * std_dev)

        cost_parameters.append({
            "Item": col.replace(" (KES)", ""),
            "Category": category,
            "Quantity": int(filtered_costs["Quantity"].iloc[0]),
            "Cost Per Unit": value,
            "Confidence Interval": f"[{lower_bound}, {upper_bound}]",
        })

# Convert to DataFrame for Display
cost_df = pd.DataFrame(cost_parameters)

# Add New Item
st.markdown(
    """
    <div style="background-color:#007278;padding:2px;border-radius:5px">
        <h3 style="color:white;text-align:center;">Add New Item</h2>
    </div>
    """,
    unsafe_allow_html=True
)
new_item = st.text_input("Item Name", "New Item")
new_category = st.selectbox("Category", ["Variable Cost", "Fixed Cost", "Other Cost"])
new_quantity = st.number_input("Quantity", value=1, min_value=1, step=1)
new_cost_per_unit = st.number_input("Cost Per Unit", value=0.0, step=1.0)

# Calculate Confidence Interval for New Item
std_dev = new_cost_per_unit * (0.01 * fluctuation_levels[selected_fluctuation])
new_lower_bound = round(new_cost_per_unit - 1.96 * std_dev)
new_upper_bound = round(new_cost_per_unit + 1.96 * std_dev)
new_confidence_interval = f"[{new_lower_bound}, {new_upper_bound}]"

if st.button("Add Item"):
    new_row = {
        "Item": new_item,
        "Category": new_category,
        "Quantity": new_quantity,
        "Cost Per Unit": new_cost_per_unit,
        "Confidence Interval": new_confidence_interval,
    }
    # Append the new row to the DataFrame
    cost_df = pd.concat([cost_df, pd.DataFrame([new_row])], ignore_index=True)
    st.success(f"Item '{new_item}' added successfully!")

# Display Updated Cost Breakdown Table
st.markdown(
    """
    <div style="background-color:#007278;padding:2px;border-radius:5px">
        <h3 style="color:white;text-align:center;">Cost Breakdown</h2>
    </div>
    """,
    unsafe_allow_html=True
)
st.dataframe(cost_df)

# Gross Margin Calculation
def calculate_gross_margin(cost_df, yield_kg, farmgate_price, loss_percentage, own_consumption_percentage):
    gross_output = yield_kg * farmgate_price
    post_harvest_loss = gross_output * (loss_percentage / 100)
    own_consumption = gross_output * (own_consumption_percentage / 100)
    net_output = gross_output - (post_harvest_loss + own_consumption)
    
    total_costs = cost_df["Cost Per Unit"].sum()
    gross_margin = net_output - total_costs
    
    return gross_output, net_output, gross_margin

gross_output, net_output, gross_margin = calculate_gross_margin(
    cost_df, yield_kg, farmgate_price, loss_percentage, own_consumption_percentage
)

st.markdown(
    """
    <div style="background-color:#007278;padding:2px;border-radius:5px">
        <h4 style="color:white;text-align:center;">Summary</h2>
    </div>
    """,
    unsafe_allow_html=True
)
# Display the selected county
if selected_county == "All":
    st.markdown("**Selected County:** All Counties")
else:
    st.markdown(f"**Selected County:** {selected_county} County")

st.markdown(f"**Gross Output:** {gross_output:,.2f} {currency}")
st.markdown(f"**Net Output:** {net_output:,.2f} {currency}")
st.markdown(f"**Gross Margin:** {gross_margin:,.2f} {currency}")

# Break-Even Analysis
def calculate_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit):
    if selling_price_per_unit > variable_cost_per_unit:
        break_even_quantity = fixed_costs / (selling_price_per_unit - variable_cost_per_unit)
        break_even_revenue = break_even_quantity * selling_price_per_unit
        return break_even_quantity, break_even_revenue
    return None, None

fixed_costs = cost_df[cost_df["Category"] == "Fixed Cost"]["Cost Per Unit"].sum()
variable_costs = cost_df[cost_df["Category"] == "Variable Cost"]["Cost Per Unit"].sum()
variable_cost_per_unit = variable_costs / yield_kg if yield_kg > 0 else 0

break_even_quantity, break_even_revenue = calculate_break_even(fixed_costs, variable_cost_per_unit, farmgate_price)

if break_even_quantity is not None:
    st.markdown(f"**Break-Even Quantity (Kg):** {break_even_quantity:,.2f}")
    st.markdown(f"**Break-Even Revenue:** {break_even_revenue:,.2f} {currency}")

# Break-Even Plot
st.markdown(
    """
    <div style="background-color:#007278;padding:2px;border-radius:5px">
        <h3 style="color:white;text-align:center;">Break-Even Analysis</h2>
    </div>
    """,
    unsafe_allow_html=True
)
def plot_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit):
    units = np.arange(0, 2000, 10)  # Change range if needed
    total_costs = fixed_costs + variable_cost_per_unit * units
    total_revenue = selling_price_per_unit * units
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.size"] = 10 
    plt.figure(figsize=(10, 6))
    plt.plot(units, total_costs, label="Total Costs", color="#a4343a")
    plt.plot(units, total_revenue, label="Total Revenue", color="#37B7C3")
    plt.axvline(break_even_quantity, color="#000000", linestyle="--", label="Break-Even Point")
    plt.xlabel("Units Produced/Sold")
    plt.ylabel("Cost/Revenue")
    plt.legend()
    st.pyplot(plt)

if break_even_quantity is not None:
    plot_break_even(fixed_costs, variable_cost_per_unit, farmgate_price)

# Cost and Revenue Distribution Plot
st.markdown(
    """
    <div style="background-color:#007278;padding:2px;border-radius:5px">
        <h3 style="color:white;text-align:center;">Cost and Revenue Distribution</h2>
    </div>
    """,
    unsafe_allow_html=True
)
categories = ["Gross Output", "Net Output", "Total Costs", "Gross Margin"]
values = [gross_output, net_output, cost_df["Cost Per Unit"].sum(), gross_margin]
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 8
fig, ax = plt.subplots()
plt.figure(figsize=(10, 6))
bars = ax.bar(categories, values, color=["#007278", "#6295A2", "#80B9AD", "#B3E2A7"])
ax.set_ylabel(f"Value ({currency})")
# Add labels on the bars
for bar, value in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,  # Center of the bar
        bar.get_height() + 0.01 * max(values),  # Slightly above the bar
        f"{value:,.2f}",  # Format the value
        ha="center",  # Center horizontally
        va="bottom",  # Align to bottom of text
        fontsize= 7  # Adjust font size as needed
    )


st.pyplot(fig)