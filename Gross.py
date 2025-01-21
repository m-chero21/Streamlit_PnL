import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode


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

st.markdown(
    """
    <style>
    html, body, [class*="st-"] {
        font-family: serif; /* Apply generic serif font globally */
    }
     h1, h2, h3, h4, h5, h6 {
        font-family: serif; /* Ensure headers are also serif */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add custom CSS for the sticky sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        position: fixed;
        top: 0;
        left: 0;
        width: inherit;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

nav_logo = "logo2.png"
LOGO_PATH = "logo.png"
st.sidebar.image(LOGO_PATH, use_container_width=True)



st.markdown(
    """
    <style>
    .centered-title {
        position: sticky; /* Make the title sticky */
        top: 0; /* Stick to the top of the page */
        z-index: 1000; /* Ensure it stays above other elements */
        text-align: center; /* Center the title */
        font-size: 36px; /* Adjust font size if needed */
        font-weight: bold;
        color: black; /* Optional: Change title color */
        background-color: white; /* Background to prevent content overlap */
        margin-top: 0; /* Remove extra spacing above */
        padding-top: 10px; /* Add padding for better appearance */
        padding-bottom: 10px; /* Add padding below the title */
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* Optional: Add a subtle shadow */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
    .navbar {
        position: sticky; /* Make the navbar sticky */
        top: 0; /* Stick to the top of the page */
        z-index: 1000; /* Ensure it stays above other elements */
        background-color: #F4F6FF; /* Set background color */
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* Optional: Add a subtle shadow */
    }
    .navbar-links {
        display: flex;
        margin-left: auto; /* Push navigation items to the right */
        gap: 20px; /* Space between navigation items */
    }
    .navbar-link {
        color: black !important; /* Set font color */
        font-size: 18px;
        text-decoration: none; /* Remove underline */
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
        color: white !important;
        font-size: 18px;
        text-decoration: none;
        padding: 5px 15px;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .navbar-button:hover {
        background-color: #a4343a; /* Darker button on hover */
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
    cost_data = [
    ["Large-scale", "With Subsidy", 23, 2400, 9600, 1800, 1000, 9750, 6125, 15000, 2557, 48232, 2144, 1],
    ["Large-scale", "Without Subsidy", 23, 2400, 14250, 1800, 1000, 9750, 6125, 15000, 2962, 53287, 2368, 1],
    ["Small-scale", "With Subsidy", 18, 2400, 7100, 1500, 0, 7050, 12000, 10000, 2379, 42429, 2357, 1],
    ["Small-scale", "Without Subsidy", 18, 2400, 11500, 1500, 0, 7050, 12000, 10000, 2628, 47078, 2615, 1],
]

# Define column names
    columns = [
    "Scale of Production", "Fertilizer Subsidy", "Average Yield (90kg bags/acre)",
    "Seed Cost (KES)", "Fertilizer Cost (KES)", "Pesticides Cost",
    "Herbicides Cost (KES)", "Machinery Cost (KES)", "Labour Cost (KES)",
    "Landrent Cost (KES)", "Other Costs (KES)", "Total Cost/Acre (KES)",
    "Total Cost/Bag (KES)", "Quantity"
]

# Create the DataFrame
    cost = pd.DataFrame(cost_data, columns=columns)
    return df, cost

df, cost = load_data()

# Sidebar - Global Parameters
st.sidebar.header("Global Inputs")
country = ["Kenya", "Nigeria"]
selected_value_chain = st.sidebar.selectbox("Country:", country)


counties = ["All"] + sorted(df["County"].unique().tolist())
selected_county = st.sidebar.selectbox("County:", counties)

value_chains = ["Maize", "Irish Potatoes", "Coffee"]
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
farmgate_price = st.sidebar.number_input("Farmgate Price (KES):", value=38.89, step=1.0)
loss_percentage = st.sidebar.slider("Post-Harvest Loss %:", 0, 50, 5)
own_consumption_percentage = st.sidebar.slider("Own Consumption %:", 0, 50, 10)

selling_price_per_unit = farmgate_price

# Filter Data

filtered_df = df.copy()
if selected_county != "All":
    filtered_df = filtered_df[filtered_df["County"] == selected_county]
if selected_value_chain != "All":
    filtered_df = filtered_df[filtered_df["Crop Type"] == selected_value_chain]


# Sidebar Area Selector
area_unit = st.sidebar.selectbox("Area Unit:", ["Hectares", "Acres"], index=0)
# Acre conversion
acre_to_hectare = 2.47105  

# Aggregate Metrics
total_production = filtered_df["Production (Tonnes)"].sum()
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
cost_parameters = []
for col, category in category_mapping.items():
    if col in filtered_costs.columns:
       
        raw_value = float(filtered_costs[col].iloc[0]) 
        if area_unit == "Hectares":
            raw_value *= acre_to_hectare
        else:
            raw_value = raw_value

       
        value = round(raw_value * exchange_rate) 
        std_dev = value * (0.01 * fluctuation_levels[selected_fluctuation])
        lower_bound = round(value - 1.96 * std_dev) 
        upper_bound = round(value + 1.96 * std_dev)  

        cost_parameters.append({
            "Item": col.replace(" (KES)", ""),
            "Category": category,
            "Quantity": int(filtered_costs["Quantity"].iloc[0]) if "Quantity" in filtered_costs else 1,
            "Cost Per Unit": value,
            "Confidence Interval": f"[{lower_bound}, {upper_bound}]",
        })

cost_df = pd.DataFrame(cost_parameters)



if "cost_df" not in st.session_state:
    st.session_state.cost_df = pd.DataFrame(cost_parameters) 



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
#_________________________________________________________________________________________________
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Function to calculate Confidence Interval
def calculate_confidence_interval(cost_per_unit, fluctuation_level, quantity):
    # Calculate standard deviation with quantity and fluctuation level
    std_dev = cost_per_unit * quantity * (0.01 * fluctuation_level)  # Standard deviation
    lower_bound = round(cost_per_unit * quantity - 1.96 * std_dev)  # 95% CI lower bound
    upper_bound = round(cost_per_unit * quantity + 1.96 * std_dev)  # 95% CI upper bound
    return f"[{lower_bound}, {upper_bound}]"

# Exclude Confidence Interval from the editable table
editable_df = cost_df.drop(columns=["Confidence Interval"])  # Remove Confidence Interval for editing

# Collapsible section for editing
with st.expander("Update Costs", expanded=False):
    # Initialize AgGrid with the modified editable dataframe
    grid_options_builder = GridOptionsBuilder.from_dataframe(editable_df)

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

    # Render the editable AgGrid table
    response = AgGrid(
        editable_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,  # Track changes in the table
        fit_columns_on_grid_load=True,
        theme="balham",
    )

    # Update the dataframe directly with edited values
    if response['data'] is not None:
        # Update editable_df with the edited table
        updated_df = pd.DataFrame(response['data'])

        # Merge back the Confidence Interval column
        cost_df.update(updated_df)

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

# Display the updated table outside the expander for reference
st.markdown(
    """
    <style>
    .custom-table-container {
        max-height: 400px; /* Limit table height */
        overflow-y: auto; /* Enable vertical scrolling */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="custom-table-container">', unsafe_allow_html=True)
# st.dataframe(cost_df)  # Display the updated table for reference
st.markdown('</div>', unsafe_allow_html=True)



#_________________________________________________________________________________________________
        
# Display the Updated Cost Breakdown Table

table_style = """
<style>
    .custom-table-container {{
        max-height: 300px; /* Desired height */
        overflow-y: auto; /* Enable vertical scrolling */
        overflow-x: auto; /* Enable horizontal scrolling */
        width: 100%;
    }}
    .custom-table-container table {{
        width: 100%; /* Make table responsive */
        font-size: 12px; /* Decrease overall text size */
        border-collapse: collapse; /* Remove spacing between cells */
    }}
    .custom-table-container table th, 
    .custom-table-container table td {{
        font-size: 11px; /* Decrease header and cell text size */
        padding: 5px; /* Adjust padding for a compact look */
        text-align: center; /* Center-align text */
        border: 1px solid #ddd; /* Add borders to cells */
    }}
    .custom-table-container table th {{
        background-color: #007278; /* Header background color */
        color: white; /* Header text color */
    }}
</style>
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

#___________________________________________________________________________________________

# # Define a function to delete an item
# def delete_item(index):
#     st.session_state.cost_df = st.session_state.cost_df.drop(index).reset_index(drop=True)
#     st.success("Item deleted successfully!")



# cost_df = st.session_state.cost_df

# # Render the table header

# st.markdown(
#     """
#     <style>
#         table {
#             border-collapse: collapse;
#             width: 100%;
#         }
#         th, td {
#             border: 1px solid #ddd;
#             padding: 8px;
#             text-align: center;
#         }
#         th {
#             background-color: #007278;
#             color: white;
#         }
#         .delete-button {
#             background-color: #f44336;
#             color: white;
#             border: none;
#             padding: 5px 10px;
#             text-align: center;
#             font-size: 12px;
#             cursor: pointer;
#             border-radius: 4px;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Render the table with delete buttons
# st.markdown("<table><thead><tr>", unsafe_allow_html=True)

# # Add column headers
# columns = cost_df.columns.tolist() + ["Delete"]
# st.markdown("".join(f"<th>{col}</th>" for col in columns), unsafe_allow_html=True)

# st.markdown("</tr></thead><tbody>", unsafe_allow_html=True)

# # Add rows
# for i, row in cost_df.iterrows():
#     st.markdown("<tr>", unsafe_allow_html=True)
    
#     # Add data cells
#     for col in cost_df.columns:
#         st.markdown(f"<td>{row[col]}</td>", unsafe_allow_html=True)

#     # Add a delete button in the last column
#     delete_button_key = f"delete_{i}"
#     if st.button("Delete", key=delete_button_key):
#         delete_item(i)

#     st.markdown("</tr>", unsafe_allow_html=True)

# st.markdown("</tbody></table>", unsafe_allow_html=True)










#____________________________________________________________________

# Gross Margin Calculation
def calculate_gross_margin(cost_df, yield_kg, farmgate_price, loss_percentage, own_consumption_percentage):
    gross_output = yield_kg * farmgate_price * exchange_rate
    post_harvest_loss = gross_output * (loss_percentage / 100)
    own_consumption = gross_output * (own_consumption_percentage / 100)
    net_output = gross_output - (post_harvest_loss + own_consumption)
    
    total_costs = cost_df["Cost Per Unit"].sum() * exchange_rate
    gross_margin = net_output - total_costs + own_consumption
    real_g_margin= total_costs-gross_output
    return gross_output, net_output, gross_margin, real_g_margin

# gross_output, net_output, gross_margin = calculate_gross_margin(
#     cost_df, yield_kg, farmgate_price, loss_percentage, own_consumption_percentage
# )
gross_output, net_output, gross_margin, real_g_margin = calculate_gross_margin(
    cost_df, yield_kg, farmgate_price, loss_percentage, own_consumption_percentage
)



# Calculate Best and Worst Case Scenarios
std_dev = gross_margin * (0.01 * fluctuation_levels[selected_fluctuation])
best_case_gross_margin = gross_margin + 1.96 * std_dev
worst_case_gross_margin = gross_margin - 1.96 * std_dev

# Break-Even Analysis
def calculate_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit, total_costs, break_even_point):
    if selling_price_per_unit > variable_cost_per_unit:
        # break_even_quantity = fixed_costs / (selling_price_per_unit - variable_cost_per_unit - other_costs)
        break_even_quantity = (total_costs / selling_price_per_unit) * exchange_rate
        break_even_revenue = break_even_quantity * selling_price_per_unit * exchange_rate
        

        
        break_even_quantity_std_dev = break_even_quantity * (0.01 * fluctuation_levels[selected_fluctuation])
        worst_case_quantity = break_even_quantity - 1.96 * break_even_quantity_std_dev
        best_case_quantity = break_even_quantity + 1.96 * break_even_quantity_std_dev

        return break_even_quantity, break_even_revenue, worst_case_quantity, best_case_quantity
    return None, None, None, None

fixed_costs = cost_df[cost_df["Category"] == "Fixed Cost"]["Cost Per Unit"].sum() 
variable_costs = cost_df[cost_df["Category"] == "Variable Cost"]["Cost Per Unit"].sum() 
other_costs= cost_df[cost_df["Category"] == "Other Cost"]["Cost Per Unit"].sum() 
variable_cost_per_unit = (variable_costs / yield_kg) 
import numpy as np

total_costs = exchange_rate*(fixed_costs + variable_costs +other_costs)
required_price_to_break_even = (fixed_costs + variable_costs + other_costs) / yield_kg 

break_even_quantity, break_even_revenue, worst_case_quantity, best_case_quantity = calculate_break_even(fixed_costs, variable_cost_per_unit, farmgate_price, total_costs, required_price_to_break_even)



#_____________________________________________________________
import plotly.graph_objects as go

# Break-Even Plot Function
def plot_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit):
    units = np.arange(0, 7000, 10)
    total_costs = fixed_costs + variable_cost_per_unit * exchange_rate * units 
    total_revenue = selling_price_per_unit * units * exchange_rate
    

    # Calculate the break-even point
    break_even_index = np.where(total_costs <= total_revenue)[0][0]  # Find the first point where costs <= revenue
    break_even_units = units[break_even_index]
    break_even_revenue = total_revenue[break_even_index]
    break_even_point = (break_even_units, break_even_revenue)
    
    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            x=units,
            y=total_costs,
            mode='lines',
            name='Total Costs',
            line=dict(color='#a4343a', width=2)
        )
    )

    
    fig.add_trace(
        go.Scatter(
            x=units,
            y=total_revenue,
            mode='lines',
            name='Total Revenue',
            line=dict(color='#37B7C3', width=2)
        )
    )

  
    fig.add_trace(
        go.Scatter(
            x=[break_even_units],
            y=[break_even_revenue],
            mode='markers',
            name='Break-Even Point',
            marker=dict(color='#000000', size=10, symbol='x')
        )
    )


    fig.update_layout(
        xaxis_title='Units Produced/Sold',
        yaxis_title='Cost/Revenue',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="seaborn",
        width=700,  
        height=600   # 
    )

    return fig, total_costs, total_revenue, break_even_point 
fig, total_costs, total_revenue, break_even_point  = plot_break_even(fixed_costs, variable_cost_per_unit, farmgate_price)


# def plot_break_even_dynamic(fixed_costs, variable_cost_per_unit, selling_price_per_unit):
#     # Generate units and calculate costs/revenues
#     units = np.arange(0, 7000, 10)
#     total_costs = fixed_costs + variable_cost_per_unit * exchange_rate * units
#     total_revenue = selling_price_per_unit * units * exchange_rate
    
#     # Calculate break-even point dynamically
#     if selling_price_per_unit > variable_cost_per_unit:
#         break_even_quantity = total_costs/(selling_price_per_unit - variable_cost_per_unit)
#         break_even_revenue = selling_price_per_unit * break_even_quantity * exchange_rate
#     else:
#         break_even_quantity = None
#         break_even_revenue = None

#     # Create the plot
#     fig = go.Figure()

#     # Add Total Costs Line
#     fig.add_trace(
#         go.Scatter(
#             x=units,
#             y=total_costs,
#             mode='lines',
#             name='Total Costs',
#             line=dict(color='#a4343a', width=2)
#         )
#     )

#     # Add Total Revenue Line
#     fig.add_trace(
#         go.Scatter(
#             x=units,
#             y=total_revenue,
#             mode='lines',
#             name='Total Revenue',
#             line=dict(color='#37B7C3', width=2)
#         )
#     )

#     # Add Break-Even Point Line if break-even is valid
#     if break_even_quantity is not None:
#         fig.add_trace(
#             go.Scatter(
#                 x=[break_even_quantity, break_even_quantity],
#                 y=[0, max(total_costs.max(), total_revenue.max())],
#                 mode='lines',
#                 name='Break-Even Point',
#                 line=dict(color='#000000', dash='dash')
#             )
#         )

#     # Update layout
#     fig.update_layout(
#         xaxis_title='Units Produced/Sold',
#         yaxis_title='Cost/Revenue',
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
#         template="seaborn",
#         width=700,
#         height=600
#     )

#     return fig, total_costs, total_revenue, break_even_quantity, break_even_revenue

# fig, total_costs, total_revenue, break_even_quantity, break_even_revenue = plot_break_even_dynamic(
#     fixed_costs, variable_cost_per_unit, farmgate_price
# )



# Cost and Revenue Distribution Plot Function
def plot_cost_and_revenue_distribution(categories, values, currency):
    # Define colors based on whether the value is negative or not
    colors = ['#a4343a' if value < 0 else '#2D9596' for value in values]

    fig = go.Figure(
        data=[
            go.Bar(
                x=categories,
                y=values,
                text=[f"{value:,.2f}" for value in values],  
                textposition='auto',
                marker=dict(color=colors)  # Use the colors defined based on value
            )
        ]
    )

    fig.update_layout(
        xaxis_title='Category',
        yaxis_title=f'Value ({currency})',
        template="seaborn",
        bargap=0.2,
        width=700,   
        height=600   
    )

    return fig

#________________________________________________________________________________________


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

import numpy as np
break_even_bags = break_even_quantity / bag_weight



summary_data = [
    {
        "Indicator": f"Farmgate Price ({currency})",
        "Value": (
            f"{(farmgate_price * exchange_rate):,.2f} {currency}"
        
        ),
    },
    {
        "Indicator": "Break-Even Quantity (Bags)",
        "Value": (
            f"{(break_even_bags):,.2f}"
            if isinstance(break_even_bags, (int, float, np.number)) and isinstance(bag_weight, (int, float, np.number))
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
        """
        <style>
        .cost-breakdown-title {
            color: #007278; /* Set text color */
            font-size: 35px; /* Adjust font size if needed */
            font-weight: bold;
            text-align: left; /* Align text to the left */
            margin-bottom: 10px; /* Add some space below the title */
        }
        .summary-table {
            width: 100%; /* Increase the table width */
        }
        </style>
        
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        summary_df.style
        .set_table_styles([
            {"selector": "thead", "props": [("background-color", "#007278"), ("color", "white"), ("font-size", "18px")]},
            {"selector": "tbody td", "props": [("font-size", "16px"), ("text-align", "center"), ("padding", "10px")]},
        ])
        .hide(axis="index")
        .to_html()
        .replace('<table', '<table class="summary-table"'),  # Add a class to the table for custom styling
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div style="font-size: 20px; line-height: 2.0; text-align: center; padding-top: 40px; ">
        At the farmgate price of <b>{farmgate_price*exchange_rate:,.2f} {currency}</b>, 
        the break-even quantity is estimated at <b> {f"{break_even_bags:,.2f}" if break_even_quantity is not None else "N/A"} bags</b> 
        To break even, the required price is 
        <b>{required_price_to_break_even:,.2f} {currency}</b>. The gross margin stands at 
        <b>{gross_margin:,.2f} {currency}</b>, while the gross output is <b>{gross_output:,.2f} {currency}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )



categories = ["Gross Output", "Marketed Output", "Total Costs", "Gross Margin"]
values = [gross_output, net_output, cost_df["Cost Per Unit"].sum(), gross_margin]


col1, col2 = st.columns(2) 

with col1:
 
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
    
    st.plotly_chart(fig, use_container_width=False)

with col2:
   
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
    
    st.plotly_chart(plot_cost_and_revenue_distribution(categories, values, currency), use_container_width=False)