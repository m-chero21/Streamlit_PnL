import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode
from matplotlib.ticker import FixedLocator

# Configure Streamlit Page
st.set_page_config(
    page_title="Gross Margin Calculator",
    page_icon="logo2.png",
    layout="wide"
)

#___________________________________________________________________________________________________________
nav_logo = r"C:\Users\mkiprono\Desktop\SAFIC\PnL Calculator\logo2.png"
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
st.markdown('<div class="centered-title"> Gross Margin Calculator </div>', unsafe_allow_html=True)

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
            <a href="seed-requirement-calculator.streamlit.app" class="navbar-link">Seed Requirement Calculator </a>
            <a href="https://gross-margin-calculator.streamlit.app/" class="navbar-button">Gross Margin Calculator</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


#___________________________________________________________________________________________________________

df = pd. read_excel(r"C:\Users\mkiprono\Desktop\SAFIC\PnL Calculator\aggregate_farm_data_template.xlsx")

# Sidebar title
st.sidebar.header("Global Parameters")

# Dropdown to select counties
counties = ["All"] + sorted(df["County"].unique().tolist())
selected_county = st.sidebar.selectbox("County:", counties)

# Dropdown to select value chains
value_chains = ["Maize", "Potatoes", "Rice", "Coffee"]
selected_value_chain = st.sidebar.selectbox("Value Chain:", value_chains)

# Filter data based on dropdown selection
filtered_df = df.copy()
if selected_value_chain != "All":
    filtered_df = filtered_df[filtered_df["Crop Type"] == selected_value_chain]
if selected_county != "All":
    filtered_df = filtered_df[filtered_df["County"] == selected_county]

# Aggregate values
total_production = filtered_df["Production (Tonnes)"].sum()
total_area = filtered_df["Area (Ha)"].sum()

# Display production and area under cultivation
summary_table = pd.DataFrame({
    "Metric": ["Production Value (Tonnes)", "Area under Cultivation (Ha)"],
    "Value": [f"{total_production:,.2f}", f"{total_area:,.2f}"]
})
# Display the table without an index column
st.sidebar.table(summary_table.set_index("Metric"))
# Bag weight and farmgate price
bag_weight = st.sidebar.number_input("Weight Per Bag (Kg):", value=90.0, step=0.1)
farmgate_price = st.sidebar.number_input("Farmgate Price (KES):", value=65.0, step=0.1)

# Dropdown for currency selection
currency = st.sidebar.selectbox("Currency:", ["KES", "USD", "Euro"])

# Exchange rate input (only shown if USD or Euro is selected)
if currency in ["USD", "Euro"]:
    exchange_rate = st.sidebar.number_input(
        "Exchange Rate:", 
        value=0.008 if currency == "USD" else 0.007, 
        step=0.001,
        format="%.3f"
    )
else:
    exchange_rate = None

# Calculate and display yield (Kg/Ha)
if total_area > 0:
    yield_kg = (total_production * 1000) / total_area  # Convert tonnes to kg
else:
    yield_kg = 0
# Loss percentage and own consumption percentage
loss_percentage = st.sidebar.slider("Loss %:", min_value=0.0, max_value=50.0, value=3.0, step=1.0) / 100
own_consumption_percentage = st.sidebar.slider("Consumption %:", min_value=0.0, max_value=50.0, value=10.0, step=5.0) / 100


st.sidebar.markdown(f"""
    <div style="text-align: center; background-color: #007278; color: white; padding: 10px; border-radius: 5px;">
        <b>Yield (Kg/Ha): {round(yield_kg, 2):,}</b>
    </div>
""", unsafe_allow_html=True)


#_________________________________________________________________________________________________________________________________________________________________

# Initial items with simplified cost categories
default_items = [
    {"name": "Labour", "category": "Variable Cost", "unit": "Days"},
    {"name": "Seed Cost", "category": "Variable Cost", "unit": "kg"},
    {"name": "Fertilizer", "category": "Variable Cost", "unit": "kg"},
    {"name": "Gunny bags", "category": "Variable Cost", "unit": "Number"},
    {"name": "Pesticide Cost", "category": "Variable Cost", "unit": "g"},
    {"name": "Land Lease", "category": "Fixed Cost", "unit": "Year"},
    {"name": "Crop Insurance", "category": "Fixed Cost", "unit": "Season"},
    {"name": "Miscellaneous", "category": "Other Cost", "unit": "Lump Sum"}
]

# Initialize session state for items and their data
if "items" not in st.session_state:
    st.session_state["items"] = default_items
    st.session_state["item_data"] = {
        f"{idx}_{item['name']}": {"quantity": 0.0, "cost": 0.0, "category": item["category"]}
        for idx, item in enumerate(default_items)
    }

# Function to display items
def display_items():
    st.markdown("""
        <div style='display: grid; grid-template-columns: 2fr 1fr 1fr 1fr auto; text-align: center; margin-bottom: 10px;'>
            <b>Item</b><b>Quantity</b><b>Cost/Unit (KES)</b><b>Category</b><b>Remove</b>
        </div>
    """, unsafe_allow_html=True)

    for idx, item in enumerate(st.session_state["items"]):
        # Generate unique key for each item based on its index and name
        unique_key = f"{idx}_{item['name']}"

        cols = st.columns([2, 1, 1, 1, 1])
        with cols[0]:
            st.write(item["name"])
        with cols[1]:
            st.session_state["item_data"][unique_key]["quantity"] = st.number_input(
                "",
                value=st.session_state["item_data"][unique_key]["quantity"],
                key=f"quantity_{unique_key}"  # Use unique key
            )
        with cols[2]:
            st.session_state["item_data"][unique_key]["cost"] = st.number_input(
                "",
                value=st.session_state["item_data"][unique_key]["cost"],
                key=f"cost_{unique_key}"  # Use unique key
            )
        with cols[3]:
            st.session_state["item_data"][unique_key]["category"] = st.selectbox(
                "",
                options=["Variable Cost", "Fixed Cost", "Other Cost"],
                index=["Variable Cost", "Fixed Cost", "Other Cost"].index(
                    st.session_state["item_data"][unique_key]["category"]),
                key=f"category_{unique_key}"  # Use unique key
            )
        with cols[4]:
            if st.button("Remove", key=f"remove_{unique_key}"):
                remove_item(idx)

# Function to remove an item
def remove_item(index):
    item = st.session_state["items"][index]
    unique_key = f"{index}_{item['name']}"
    del st.session_state["item_data"][unique_key]
    del st.session_state["items"][index]

# Function to add a new parameter
def add_new_parameter(name, quantity, cost, category):
    if name:
        index = len(st.session_state["items"])  # New unique index
        unique_key = f"{index}_{name}"
        new_item = {"name": name, "category": category, "unit": ""}
        st.session_state["items"].append(new_item)
        st.session_state["item_data"][unique_key] = {"quantity": quantity, "cost": cost, "category": category}

# # Display the items
# if st.button("Update Parameters"):  # Ensures unique keys are refreshed after update
#     st.rerun()

display_items()

# Section for adding new parameters
st.markdown("<h3 style='color:black; font-weight:bold;'>Add New Parameter</h3>", unsafe_allow_html=True)
new_param_name = st.text_input("Item", placeholder="Enter a new item")
new_param_quantity = st.number_input("Quantity", value=0.0)
new_param_cost = st.number_input("Cost/Unit (KES)", value=0.0)
new_param_category = st.selectbox("Category", ["Variable Cost", "Fixed Cost", "Other Cost"])

# Buttons for adding and updating parameters
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Add Parameter"):
        add_new_parameter(new_param_name, new_param_quantity, new_param_cost, new_param_category)
        st.rerun()  # Rerun the app to include the new parameter dynamically

