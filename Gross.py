import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd 
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode

st.set_page_config(
    page_title="Gross Margin Calculator",  
    page_icon="logo2.png",  
    layout="wide"
)
LOGO_PATH = "logo.png"
st.image(LOGO_PATH, width = 300) 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode

# Define the calculate_yield function
def calculate_yield(production_value, production_unit, area_value, area_unit):
    production_conversion = 1000 if production_unit == "Tonnes" else 1
    production_in_kg = production_value * production_conversion
    area_conversion = 0.404686 if area_unit == "Acres" else 1
    area_in_ha = area_value * area_conversion
    return round(production_in_kg / area_in_ha, 2) if area_in_ha > 0 else 0

# Sidebar: Global Parameters
st.sidebar.header("Global Parameters")

production_unit = st.sidebar.selectbox("Production Unit:", ["Tonnes", "Kilograms"])
production_value = st.sidebar.number_input("Production Value:", value=84000)
area_unit = st.sidebar.selectbox("Area Unit:", ["Hectares (Ha)", "Acres"])
area_value = st.sidebar.number_input("Area under Cultivation:", value=47000)
bag_weight = st.sidebar.number_input("Weight per Bag (Kg):", value=90)
farmgate_price = st.sidebar.number_input("Farmgate Price (KES):", value=65)
currency = st.sidebar.selectbox("Currency:", ["USD", "Euro", "KES"])
exchange_rate = st.sidebar.number_input("Exchange Rate (KES):", value=0.008)
loss_percentage = st.sidebar.slider("Loss Percentage (%):", min_value=0.0, max_value=50.0, value=3.0) / 100
own_consumption_percentage = st.sidebar.slider("Own Consumption Percentage (%):", min_value=0.0, max_value=50.0, value=10.0) / 100

# Calculate yield dynamically
yield_kg = calculate_yield(production_value, production_unit, area_value, area_unit)
st.sidebar.write(f"Calculated Yield (Kg/Ha): {yield_kg}")

# Initialize cost items if not already in session state
if "cost_items" not in st.session_state:
    st.session_state.cost_items = pd.DataFrame({
        "Item": ["Labour", "Seed Cost", "Fertilizer", "Gunny Bags", "Pesticide Cost", "Land Lease", "Crop Insurance", "Miscellaneous"],
        "Category": ["Variable Cost", "Variable Cost", "Variable Cost", "Variable Cost", "Variable Cost", "Fixed Cost", "Fixed Cost", "Other Cost"],
        "Quantity": [10, 20, 50, 100, 5, 1, 1, 1],
        "Cost/Unit (KES)": [300, 50, 100, 20, 200, 5000, 3000, 1000],
    })

# Editable Table with st_aggrid
st.header("Cost Parameters")

gb = GridOptionsBuilder.from_dataframe(st.session_state.cost_items)
gb.configure_default_column(editable=True, groupable=True)
grid_options = gb.build()

grid_response = AgGrid(
    st.session_state.cost_items,
    gridOptions=grid_options,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    update_mode="value_changed",
    fit_columns_on_grid_load=True,
    height=300,
    theme="streamlit",
)

st.session_state.cost_items = grid_response['data']

# Add New Parameters
st.subheader("Add New Parameter")

new_item_name = st.text_input("Item Name")
new_category = st.selectbox("Category", ["Variable Cost", "Fixed Cost", "Other Cost"], key="new_category")
new_quantity = st.number_input("Quantity", min_value=0.0, value=0.0, step=1.0, key="new_quantity")
new_cost = st.number_input("Cost per Unit (KES)", min_value=0.0, value=0.0, step=1.0, key="new_cost")

if st.button("Add Item"):
    if new_item_name:
        new_row = pd.DataFrame(
            {"Item": [new_item_name], "Category": [new_category], "Quantity": [new_quantity], "Cost/Unit (KES)": [new_cost]}
        )
        st.session_state.cost_items = pd.concat([st.session_state.cost_items, new_row], ignore_index=True)
        st.success(f"Added '{new_item_name}' successfully!")
    else:
        st.error("Item name cannot be empty.")

# Gross Margin Calculation
def calculate_gross_margin(yield_kg, bag_weight, farmgate_price, loss_percentage, own_consumption_percentage, cost_items, exchange_rate):
    gross_output_quantity = yield_kg / bag_weight
    gross_output_cost_per_unit = farmgate_price * bag_weight
    gross_output_value_kes = gross_output_quantity * gross_output_cost_per_unit

    post_harvest_loss_quantity = -gross_output_quantity * loss_percentage
    own_consumption_quantity = -gross_output_quantity * own_consumption_percentage
    net_output_quantity = gross_output_quantity + post_harvest_loss_quantity + own_consumption_quantity
    net_output_value_kes = net_output_quantity * gross_output_cost_per_unit

    cost_items["Total Cost (KES)"] = cost_items["Quantity"] * cost_items["Cost/Unit (KES)"]
    total_variable_costs = cost_items[cost_items["Category"] == "Variable Cost"]["Total Cost (KES)"].sum()
    total_fixed_costs = cost_items[cost_items["Category"] == "Fixed Cost"]["Total Cost (KES)"].sum()
    total_other_costs = cost_items[cost_items["Category"] == "Other Cost"]["Total Cost (KES)"].sum()

    grand_total_costs = total_variable_costs + total_fixed_costs + total_other_costs
    gross_margin_kes = net_output_value_kes - grand_total_costs
    gross_margin_usd = gross_margin_kes * exchange_rate

    return gross_margin_kes, gross_margin_usd, total_variable_costs, total_fixed_costs, total_other_costs, net_output_value_kes, net_output_quantity

# Perform Gross Margin Calculations
gross_margin_kes, gross_margin_usd, total_variable_costs, total_fixed_costs, total_other_costs, net_output_value_kes, net_output_quantity = calculate_gross_margin(
    yield_kg, bag_weight, farmgate_price, loss_percentage, own_consumption_percentage, st.session_state.cost_items, exchange_rate
)

st.subheader("Gross Margin Results")
st.write(f"**Gross Margin (KES):** {gross_margin_kes:,.2f}")
st.write(f"**Gross Margin (USD):** {gross_margin_usd:,.2f}")
st.write(f"**Net Output Value (KES):** {net_output_value_kes:,.2f}")

# Cost and Revenue Distribution Chart
st.subheader("Cost and Revenue Distribution")

cost_distribution = {
    "Category": ["Net Output", "TOTAL VARIABLE COSTS", "TOTAL FIXED COSTS", "TOTAL OTHER COSTS", "GROSS MARGIN"],
    "Cost (KES)": [net_output_value_kes, total_variable_costs, total_fixed_costs, total_other_costs, gross_margin_kes],
}
cost_df = pd.DataFrame(cost_distribution)

fig, ax = plt.subplots()
ax.bar(cost_df["Category"], cost_df["Cost (KES)"], color=['#007278', '#00205b', 'orange', '#a4343a', 'purple'])
ax.set_xticklabels(cost_df["Category"], rotation=45, ha='right')
for i, value in enumerate(cost_df["Cost (KES)"]):
    ax.text(i, value, f"{value:,.2f} KES", ha='center', va='bottom')
ax.set_title("Cost and Revenue Distribution")
ax.set_ylabel("KES")
st.pyplot(fig)  # Pass the figure object explicitly

# Break-Even Analysis
st.subheader("Break-Even Analysis")

def plot_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit, max_units=1000):
    units = list(range(0, max_units + 1))
    total_costs = [fixed_costs + variable_cost_per_unit * q for q in units]
    total_revenue = [selling_price_per_unit * q for q in units]
    break_even_quantity = fixed_costs / (selling_price_per_unit - variable_cost_per_unit) if selling_price_per_unit > variable_cost_per_unit else 0

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(units, total_costs, label="Total Costs", color="red")
    ax.plot(units, total_revenue, label="Total Revenue", color="green")
    ax.axvline(x=break_even_quantity, color="blue", linestyle="--", label=f"Break-Even Point: {break_even_quantity:.2f} units")
    ax.set_title("Break-Even Analysis")
    ax.set_xlabel("Units Produced/Sold")
    ax.set_ylabel("KES")
    ax.legend()
    ax.grid()
    st.pyplot(fig)  # Pass the figure object explicitly

# Call Break-Even Plot Function
fixed_costs = total_fixed_costs
variable_cost_per_unit = farmgate_price * 0.75  # Example for variable cost per unit
selling_price_per_unit = farmgate_price
plot_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit)

