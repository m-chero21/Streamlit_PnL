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
st.markdown("### Add New Item")
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
st.markdown("## Cost Breakdown")
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

st.markdown("### Summary")
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
st.markdown("### Break-Even Analysis")
def plot_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit):
    units = np.arange(0, 2000, 10)  # Change range if needed
    total_costs = fixed_costs + variable_cost_per_unit * units
    total_revenue = selling_price_per_unit * units
    plt.rcParams["font.family"] = "serif"
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
st.markdown("### Cost and Revenue Distribution")
categories = ["Gross Output", "Net Output", "Total Costs", "Gross Margin"]
values = [gross_output, net_output, cost_df["Cost Per Unit"].sum(), gross_margin]
plt.rcParams["font.family"] = "serif"
fig, ax = plt.subplots()
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

















































































































#_________________________________________________________________________________________________________________________________________________________________

# # Initial items with simplified cost categories
# default_items = [
#     {"name": "Labour", "category": "Variable Cost", "unit": "Days"},
#     {"name": "Seed Cost", "category": "Variable Cost", "unit": "kg"},
#     {"name": "Fertilizer", "category": "Variable Cost", "unit": "kg"},
#     {"name": "Gunny bags", "category": "Variable Cost", "unit": "Number"},
#     {"name": "Pesticide Cost", "category": "Variable Cost", "unit": "g"},
#     {"name": "Land Lease", "category": "Fixed Cost", "unit": "Year"},
#     {"name": "Crop Insurance", "category": "Fixed Cost", "unit": "Season"},
#     {"name": "Miscellaneous", "category": "Other Cost", "unit": "Lump Sum"}
# ]

# # Initialize session state for items and their data
# if "items" not in st.session_state:
#     st.session_state["items"] = default_items
#     st.session_state["item_data"] = {
#         f"{idx}_{item['name']}": {"quantity": 0.0, "cost": 0.0, "category": item["category"]}
#         for idx, item in enumerate(default_items)
#     }

# # Function to display items
# def display_items():
#     st.markdown("""
#     <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr auto; gap: 10px; padding-top: 40px; margin-bottom: 10px;">
#         <b>Item</b><b>Quantity</b><b>Cost/Unit (KES)</b><b>Category</b>
#     </div>
#     """, unsafe_allow_html=True)

#     for idx, item in enumerate(st.session_state["items"]):
#         # Generate unique key for each item based on its index and name
#         unique_key = f"{idx}_{item['name']}"

#         cols = st.columns([1, 1, 1, 1, 1])
#         with cols[0]:
#             st.write(item["name"])
#         with cols[1]:
#             st.session_state["item_data"][unique_key]["quantity"] = st.number_input(
#             "",
#             value=int(st.session_state["item_data"][unique_key]["quantity"]),  # Ensure value is an integer
#             step=1,  # Step is an integer
#             format="%d",  # Display as an integer
#             key=f"quantity_{unique_key}"  # Use unique key
#             )
#         with cols[2]:
#             st.session_state["item_data"][unique_key]["cost"] = st.number_input(
#                 "",
#                 value=st.session_state["item_data"][unique_key]["cost"],
#                 key=f"cost_{unique_key}"  # Use unique key
#             )
#         with cols[3]:
#             st.session_state["item_data"][unique_key]["category"] = st.selectbox(
#                 "",
#                 options=["Variable Cost", "Fixed Cost", "Other Cost"],
#                 index=["Variable Cost", "Fixed Cost", "Other Cost"].index(
#                     st.session_state["item_data"][unique_key]["category"]),
#                 key=f"category_{unique_key}"  # Use unique key
#             )
# #         with cols[4]:
# #             if st.button("Remove", key=f"remove_{unique_key}"):
# #                 remove_item(idx)

# # # Function to remove an item
# # def remove_item(index):
# #     item = st.session_state["items"][index]
# #     unique_key = f"{index}_{item['name']}"
# #     del st.session_state["item_data"][unique_key]
# #     del st.session_state["items"][index]

# # Function to add a new parameter
# def add_new_parameter(name, quantity, cost, category):
#     if name:
#         index = len(st.session_state["items"])  # New unique index
#         unique_key = f"{index}_{name}"
#         new_item = {"name": name, "category": category, "unit": ""}
#         st.session_state["items"].append(new_item)
#         st.session_state["item_data"][unique_key] = {"quantity": quantity, "cost": cost, "category": category}

# # # Display the items
# # if st.button("Update Parameters"):  # Ensures unique keys are refreshed after update
# #     st.rerun()

# display_items()

# # Section for adding new parameters
# st.markdown("<h3 style='color:black; font-weight:bold;'>Add New Parameter</h3>", unsafe_allow_html=True)
# new_param_name = st.text_input("Item", placeholder="Enter a new item")
# new_param_quantity = st.number_input("Quantity", value=0.0)
# new_param_cost = st.number_input("Cost/Unit (KES)", value=0.0)
# new_param_category = st.selectbox("Category", ["Variable Cost", "Fixed Cost", "Other Cost"])

# # Buttons for adding and updating parameters
# col1, col2 = st.columns([1, 1])

# with col1:
#     if st.button("Add Parameter"):
#         add_new_parameter(new_param_name, new_param_quantity, new_param_cost, new_param_category)
#         st.rerun()  # Rerun the app to include the new parameter dynamically


# #___________________________________________________________________________________________________________________________________
# def plot_cost_distribution(gross_margin_df, currency="KES", exchange_rate=1):
#     """
#     Plot the cost and revenue distribution based on the gross margin DataFrame.

#     Args:
#     - gross_margin_df (DataFrame): DataFrame summarizing costs, outputs, and gross margin.
#     - currency (str): Currency being used (KES, USD, Euro).
#     - exchange_rate (float): Exchange rate for currency conversion.

#     Returns:
#     - matplotlib.figure.Figure: The figure object to be displayed in Streamlit.
#     """
#     import matplotlib.pyplot as plt

#     # Define the relevant categories for plotting
#     categories = ["Net Output", "TOTAL VARIABLE COSTS", "TOTAL FIXED COSTS", "TOTAL OTHER COSTS", "GROSS MARGIN"]

#     # Extract the values for the categories, applying the exchange rate if necessary
#     values = [
#         gross_margin_df[gross_margin_df["ITEM"] == category]["VALUE-KES"].values[0]
#         * (1 if currency == "KES" else exchange_rate)
#         if category in gross_margin_df["ITEM"].values
#         else 0
#         for category in categories
#     ]

#     # Create a bar plot for the categories
#     fig, ax = plt.subplots(figsize=(10, 6))
#     bars = ax.bar(categories, values, color=["#007278", "#6A1E55", "#EB5B00", "#f7b731", "#a4343a"])

#     # Annotate the bars with the values
#     for bar, value in zip(bars, values):
#         ax.text(
#             bar.get_x() + bar.get_width() / 2,
#             bar.get_height(),
#             f"{value:,.2f} {currency}",
#             ha="center",
#             va="bottom",
#             fontsize=10,
#         )

#     ax.set_title("Cost and Revenue Distribution", fontsize=16)
#     ax.set_ylabel(f"Value ({currency})", fontsize=14)
#     ax.grid(axis="y", linestyle="--", alpha=0.7)
#     plt.xticks(rotation=45, ha="right")

#     return fig

# # Function to calculate gross margins
# def calculate_gross_margins_dynamic(item_widgets, farmgate_price, exchange_rate, loss_percentage,
#                                     own_consumption_percentage, yield_kg, bag_weight, currency="KES"):
#     output_values = []
#     variable_costs = []
#     fixed_costs = []
#     other_costs = []

#     # 1. Calculate Gross Output
#     gross_output_quantity = yield_kg / bag_weight
#     gross_output_cost_per_unit = farmgate_price * bag_weight
#     gross_output_value_kes = gross_output_quantity * gross_output_cost_per_unit
#     output_values.append(["Gross Output", "Bags", round(gross_output_quantity, 2),
#                           round(gross_output_cost_per_unit, 2), round(gross_output_value_kes, 2)])

#     # 2. Calculate Post-Harvest Losses
#     post_harvest_loss_quantity = -gross_output_quantity * loss_percentage
#     post_harvest_loss_value_kes = post_harvest_loss_quantity * gross_output_cost_per_unit
#     output_values.append(["Post-Harvest Losses", "Bags", round(post_harvest_loss_quantity, 2),
#                           round(gross_output_cost_per_unit, 2), round(post_harvest_loss_value_kes, 2)])

#     # 3. Calculate Own Consumption
#     own_consumption_quantity = -gross_output_quantity * own_consumption_percentage
#     own_consumption_value_kes = own_consumption_quantity * gross_output_cost_per_unit
#     output_values.append(["Own Consumption", "Bags", round(own_consumption_quantity, 2),
#                           round(gross_output_cost_per_unit, 2), round(own_consumption_value_kes, 2)])

#     # 4. Calculate Net Output
#     net_output_quantity = gross_output_quantity + post_harvest_loss_quantity + own_consumption_quantity
#     net_output_value_kes = net_output_quantity * gross_output_cost_per_unit
#     output_values.append(["Net Output", "Bags", round(net_output_quantity, 2),
#                           round(gross_output_cost_per_unit, 2), round(net_output_value_kes, 2)])

#     # 5. Classify and Calculate Costs
#     for name, widget_dict in item_widgets.items():
#         quantity = widget_dict["quantity"]
#         cost_per_unit = widget_dict["cost"]
#         category = widget_dict["category"]
#         value_kes = quantity * cost_per_unit

#         if category == "Variable Cost":
#             variable_costs.append([name, "Unit", round(quantity, 2), round(cost_per_unit, 2), round(value_kes, 2)])
#         elif category == "Fixed Cost":
#             fixed_costs.append([name, "Unit", round(quantity, 2), round(cost_per_unit, 2), round(value_kes, 2)])
#         elif category == "Other Cost":
#             other_costs.append([name, "Unit", round(quantity, 2), round(cost_per_unit, 2), round(value_kes, 2)])

#     # Create DataFrames
#     output_df = pd.DataFrame(output_values, columns=["ITEM", "UNIT", "QUANTITY", "COST/UNIT", "VALUE-KES"])
#     variable_costs_df = pd.DataFrame(variable_costs, columns=["ITEM", "UNIT", "QUANTITY", "COST/UNIT", "VALUE-KES"])
#     fixed_costs_df = pd.DataFrame(fixed_costs, columns=["ITEM", "UNIT", "QUANTITY", "COST/UNIT", "VALUE-KES"])
#     other_costs_df = pd.DataFrame(other_costs, columns=["ITEM", "UNIT", "QUANTITY", "COST/UNIT", "VALUE-KES"])

#     # 6. Totals and Gross Margin
#     total_output_kes = net_output_value_kes
#     total_variable_costs_kes = variable_costs_df["VALUE-KES"].sum()
#     total_fixed_costs_kes = fixed_costs_df["VALUE-KES"].sum()
#     total_other_costs_kes = other_costs_df["VALUE-KES"].sum()
#     grand_total_costs_kes = total_variable_costs_kes + total_fixed_costs_kes + total_other_costs_kes
#     gross_margin_kes = total_output_kes - grand_total_costs_kes

#     # Summary Data
#     summary_data = [
#         ["Outputs", "", "", "", ""],
#         *output_df.values.tolist(),
#         ["", "", "", "", ""],
#         ["Variable Costs", "", "", "", ""],
#         *variable_costs_df.values.tolist(),
#         ["TOTAL VARIABLE COSTS", "", "", "", round(total_variable_costs_kes, 2)],
#         ["", "", "", "", ""],
#         ["Fixed Costs", "", "", "", ""],
#         *fixed_costs_df.values.tolist(),
#         ["TOTAL FIXED COSTS", "", "", "", round(total_fixed_costs_kes, 2)],
#         ["", "", "", "", ""],
#         ["Other Costs", "", "", "", ""],
#         *other_costs_df.values.tolist(),
#         ["TOTAL OTHER COSTS", "", "", "", round(total_other_costs_kes, 2)],
#         ["", "", "", "", ""],
#         ["GROSS MARGIN", "", "", "", round(gross_margin_kes, 2)],
#     ]

#     gross_margin_df = pd.DataFrame(summary_data, columns=["ITEM", "UNIT", "QUANTITY", "COST/UNIT", "VALUE-KES"])

#     return gross_margin_df


# # Button for Gross Margin Calculation
# if st.button("Calculate Gross Margins"):
#     # Calculate Gross Margins
#     gross_margin_df = calculate_gross_margins_dynamic(
#         item_widgets=st.session_state["item_data"],
#         farmgate_price=farmgate_price,
#         exchange_rate=exchange_rate if exchange_rate else 1,
#         loss_percentage=loss_percentage,
#         own_consumption_percentage=own_consumption_percentage,
#         yield_kg=yield_kg,
#         bag_weight=bag_weight,
#         currency=currency
#     )

#     # Display Results
#     st.subheader("Gross Margin Results")
#     st.dataframe(gross_margin_df)

#     # Visualize Cost Distribution
#     st.subheader("Cost and Revenue Distribution")
#     fig = plot_cost_distribution(gross_margin_df, currency=currency, exchange_rate=exchange_rate if exchange_rate else 1)
#     st.pyplot(fig)

#     #________________________________________________________________________________

# def plot_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit, max_units=1000, currency="KES", exchange_rate=1):
#     """
#     Plot the break-even analysis showing total costs, total revenue, and break-even point.

#     Args:
#     - fixed_costs (float): Total fixed costs.
#     - variable_cost_per_unit (float): Variable cost per unit.
#     - selling_price_per_unit (float): Selling price per unit.
#     - max_units (int): Maximum number of units to consider in the analysis.
#     - currency (str): Currency being used (KES, USD, Euro).
#     - exchange_rate (float): Exchange rate for currency conversion.
#     """
#     if selling_price_per_unit <= variable_cost_per_unit:
#         st.warning("Break-even analysis is not feasible: Selling price must exceed variable cost.")
#         return

#     # Calculate units and costs/revenue
#     units = range(0, max_units + 1)
#     total_costs = [fixed_costs + variable_cost_per_unit * q for q in units]
#     total_revenue = [selling_price_per_unit * q for q in units]

#     # Convert to chosen currency
#     total_costs = [cost * exchange_rate if currency != "KES" else cost for cost in total_costs]
#     total_revenue = [revenue * exchange_rate if currency != "KES" else revenue for revenue in total_revenue]

#     # Determine break-even point
#     break_even_quantity = fixed_costs / (selling_price_per_unit - variable_cost_per_unit)
#     break_even_revenue = break_even_quantity * selling_price_per_unit

#     # Plot
#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.plot(units, total_costs, label="Total Costs", color="#a4343a")
#     ax.plot(units, total_revenue, label="Total Revenue", color="green")
#     ax.axvline(x=break_even_quantity, color="#007278", linestyle="--", label=f"Break-Even Point: {break_even_quantity:.2f} units")
#     ax.axhline(y=break_even_revenue, color="#007278", linestyle="--", alpha=0.5)
#     ax.set_title("Break-Even Analysis", fontsize=14)
#     ax.set_xlabel("Units Produced/Sold")
#     ax.set_ylabel(f"Cost/Revenue ({currency})")
#     ax.legend()
#     ax.grid(alpha=0.3)

#     # Annotate the break-even point
#     ax.annotate(
#         f"Break-Even: {break_even_quantity:.2f} units\n{break_even_revenue:,.2f} {currency}",
#         xy=(break_even_quantity, break_even_revenue),
#         xytext=(break_even_quantity * 0.6, break_even_revenue * 1.1),
#         arrowprops=dict(facecolor='black', arrowstyle="->"),
#         fontsize=10,
#         bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
#     )

#     st.pyplot(fig)

# # Implement Break-Even Analysis in the Streamlit App
# if st.button("Break-Even Analysis"):
#     # Calculate fixed and variable costs
#     fixed_costs = sum(
#         [widget["cost"] * widget["quantity"] for widget in st.session_state["item_data"].values() if widget["category"] == "Fixed Cost"]
#     )
#     variable_costs = sum(
#         [widget["cost"] * widget["quantity"] for widget in st.session_state["item_data"].values() if widget["category"] == "Variable Cost"]
#     )
#     variable_cost_per_unit = variable_costs / yield_kg if yield_kg > 0 else 0  # Avoid division by zero
#     selling_price_per_unit = farmgate_price

#     # Perform break-even analysis
#     if selling_price_per_unit > variable_cost_per_unit:
#         # Break-even calculations
#         break_even_quantity_kg = fixed_costs / (selling_price_per_unit - variable_cost_per_unit)
#         break_even_quantity_bags = break_even_quantity_kg / bag_weight
#         required_yield_to_break_even = fixed_costs / (selling_price_per_unit - variable_cost_per_unit)
#         required_price_to_break_even = (fixed_costs + (variable_cost_per_unit * yield_kg)) / yield_kg if yield_kg > 0 else None

#         # Display Insights
#         st.subheader("Break-Even Insights")
#         st.markdown(f"""
#             - **Break-Even Quantity (Bags):** {break_even_quantity_bags:.2f}
#             - **Break-Even Quantity (Kg):** {break_even_quantity_kg:.2f}
#             - **Required Yield to Break-Even (Kg):** {required_yield_to_break_even:.2f}
#             - **Required Price to Break-Even (Per Unit):** {required_price_to_break_even:,.2f} {currency}
#         """)
#     else:
#         st.warning("Break-even analysis is not feasible: Selling price must exceed variable cost.")

#     # Plot Break-Even
#     plot_break_even(
#         fixed_costs=fixed_costs,
#         variable_cost_per_unit=variable_cost_per_unit,
#         selling_price_per_unit=selling_price_per_unit,
#         max_units=1000,
#         currency=currency,
#         exchange_rate=exchange_rate if exchange_rate else 1
#     )
