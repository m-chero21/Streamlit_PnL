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
    cost = pd.read_excel("cost.xlsx")
    return df, cost

df, cost = load_data()

# Sidebar - Global Parameters
st.sidebar.header("Global Inputs")

country =sorted(set(df['Country']).union(set(cost['Country'])))
selected_country = st.sidebar.selectbox("Country:", country)
cost['Country'] = cost['Country'].astype(str).str.strip()

# Filter the DataFrame based on the selected country
filtered_c_df = df[df['Country'] == selected_country]
f_cost=  cost[cost['Country'] == selected_country]


counties = ["All"] + sorted(filtered_c_df["County"].unique().tolist())
selected_county = st.sidebar.selectbox("County:", counties)


# Collapsible section for all cost-related parameters
with st.sidebar.expander("Production Variables", expanded=False):

    # Value Chain
    value_chains = ["Maize", "Irish Potatoes", "Coffee"]
    selected_value_chain = st.selectbox("Value Chain:", value_chains)

    # Scale of Production
    scale_options = f_cost["Scale of Production"].unique()
    selected_scale = st.selectbox("Scale of Production:", scale_options)

    # Fertilizer Subsidy
    subsidy_options = f_cost["Fertilizer Subsidy"].unique()
    selected_subsidy = st.selectbox("Fertilizer Subsidy:", subsidy_options)

    # Fluctuation Levels
    fluctuation_levels = {"Low": 1, "Moderate": 2, "High": 3}
    selected_fluctuation = st.selectbox("Fluctuation Level:", list(fluctuation_levels.keys()))

    # Bag Weight
    # Set bag weight based on country selection
    if selected_country == "Nigeria":
        bag_weight = 1.0
    else:
        bag_weight = st.number_input("Weight Per Bag (Kg):", value=90.0, step=1.0)


with st.sidebar.expander("Currency", expanded=False):
    # Default currency and exchange rate based on selected country
    if selected_country == "Nigeria":
        currency = st.selectbox("Currency:", ["NGN", "USD"])  # Restrict to NGN & USD
        if currency == "NGN":
            exchange_rate = 11.6
        elif currency == "USD":
            exchange_rate = 11.6 * 0.00066  # Apply 0.85 multiplier
    else:
        currency = st.selectbox("Currency:", ["KES", "USD", "Euro"])  # Default options for other countries
        exchange_rate = st.number_input(
            "Exchange Rate:",
            value=1.0 if currency == "KES" else (0.008 if currency == "USD" else 0.007),
            step=0.001,
            format="%.3f"
        )


# Set Farmgate Price dynamically
default_farmgate_price = 41351.64 if selected_country == "Nigeria" else 38.89

farmgate_price = st.sidebar.number_input(
    f"Farmgate Price ({currency}):", value=default_farmgate_price, step=1.0
)
loss_percentage = st.sidebar.slider("Post-Harvest Loss %:", 0, 50, 5)
own_consumption_percentage = st.sidebar.slider("Own Consumption %:", 0, 50, 10)

selling_price_per_unit = farmgate_price

# Filter Data

filtered_df = filtered_c_df.copy()
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
    upper_bound = round(cost_per_unit* quantity + 1.96 * std_dev)  # 95% CI upper bound
    return f"[{lower_bound:,}, {upper_bound:,}]"



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
st.markdown(
    """
    <style>
    .custom-table-container {
        max-height: 200px; /* Limit table height */
        overflow-y: auto; /* Enable vertical scrolling */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="custom-table-container">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)



#_________________________________________________________________________________________________
        
# Display the Updated Cost Breakdown Table

table_style = """
<style>
    .custom-table-container {{
        max-height: 600px; /* Desired height */
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
        font-size: 14px; /* Decrease header and cell text size */
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

# Gross Margin Calculation
def calculate_gross_margin(cost_df, yield_kg, farmgate_price, loss_percentage, own_consumption_percentage):
    gross_output = yield_kg * farmgate_price * exchange_rate
    post_harvest_loss = gross_output * (loss_percentage / 100)
    own_consumption = gross_output * (own_consumption_percentage / 100)
    net_output = gross_output - (post_harvest_loss + own_consumption)
    
    total_costs = cost_df["Cost Per Unit"].sum() 
    gross_margin = net_output - total_costs + own_consumption
    real_g_margin= total_costs-gross_output
    return gross_output, net_output, gross_margin, real_g_margin

gross_output, net_output, gross_margin, real_g_margin = calculate_gross_margin(
    cost_df, yield_kg, farmgate_price, loss_percentage, own_consumption_percentage
)



# Calculate Best and Worst Case Scenarios
std_dev = gross_margin * (0.01 * fluctuation_levels[selected_fluctuation])
best_case_gross_margin = gross_margin + 1.96 * std_dev
worst_case_gross_margin = gross_margin - 1.96 * std_dev

# Break-Even Analysis
def calculate_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit, total_costs, break_even_point):
   
        
    break_even_quantity = total_costs / selling_price_per_unit
        
       
    break_even_revenue = break_even_quantity * selling_price_per_unit * exchange_rate
        

        
    break_even_quantity_std_dev = break_even_quantity * (0.01 * fluctuation_levels[selected_fluctuation])
    worst_case_quantity = break_even_quantity - 1.96 * break_even_quantity_std_dev
    best_case_quantity = break_even_quantity + 1.96 * break_even_quantity_std_dev

    return break_even_quantity, break_even_revenue, worst_case_quantity, best_case_quantity
    

fixed_costs = cost_df[cost_df["Category"] == "Fixed Cost"]["Cost Per Unit"].sum() 
variable_costs = cost_df[cost_df["Category"] == "Variable Cost"]["Cost Per Unit"].sum() 
other_costs= cost_df[cost_df["Category"] == "Other Cost"]["Cost Per Unit"].sum() 
variable_cost_per_unit = (variable_costs / yield_kg) 
import numpy as np

total_costs = fixed_costs + variable_costs +other_costs
required_price_to_break_even = (fixed_costs + variable_costs + other_costs) / yield_kg 

break_even_quantity, break_even_revenue, worst_case_quantity, best_case_quantity = calculate_break_even(fixed_costs, variable_cost_per_unit, farmgate_price, total_costs, required_price_to_break_even)



#_____________________________________________________________
import plotly.graph_objects as go

# Break-Even Plot Function
def plot_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit, exchange_rate):
    units = np.arange(0, 8000, 10)
    
    # Compute total costs and revenue
    total_costs = fixed_costs + variable_cost_per_unit * exchange_rate * units 
    total_revenue = selling_price_per_unit * units * exchange_rate

    # Find break-even point
    break_even_indices = np.where(total_costs <= total_revenue)[0]

    if break_even_indices.size > 0:
        break_even_index = break_even_indices[0]
        break_even_units = units[break_even_index]
        break_even_revenue = total_revenue[break_even_index]
    else:
        break_even_units = None
        break_even_revenue = None

    break_even_point = (break_even_units, break_even_revenue)
    
    # Create Plotly figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=units,
        y=total_costs,
        mode='lines',
        name='Total Costs',
        line=dict(color='#a4343a', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=units,
        y=total_revenue,
        mode='lines',
        name='Total Revenue',
        line=dict(color='#37B7C3', width=2)
    ))

    # Plot break-even point if it exists
    if break_even_units is not None and break_even_revenue is not None:
        fig.add_trace(go.Scatter(
            x=[break_even_units],
            y=[break_even_revenue],
            mode='markers',
            name='Break-Even Point',
            marker=dict(color='#000000', size=10, symbol='x')
        ))

    # # Update figure layout
    # fig.update_layout(
    #     xaxis_title='Units Produced/Sold',
    #     yaxis_title='Cost/Revenue',
    #     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    #     template="seaborn",
    #     width=700,  
    #     height=600
    # )
    # Update figure layout
    fig.update_layout(
        xaxis_title='Units Produced/Sold',
        yaxis_title='Cost/Revenue',
        xaxis=dict(
            title_font=dict(color='black', size=14, family='Arial', weight='bold'),
            tickfont=dict(color='black', size=12)
        ),
        yaxis=dict(
            title_font=dict(color='black', size=14, family='Arial', weight='bold'),
            tickfont=dict(color='black', size=12)
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="seaborn",
        width=700,  
        height=600
    )
    return fig, total_costs, total_revenue, break_even_point 

# Example function call (ensure exchange_rate is defined)
fig, total_costs, total_revenue, break_even_point = plot_break_even(
    fixed_costs, variable_cost_per_unit, farmgate_price, exchange_rate
)

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
        xaxis=dict(
            title_font=dict(color='black', size=14, family='Arial', weight='bold'),
            tickfont=dict(color='black', size=12)
        ),
        yaxis=dict(
            title_font=dict(color='black', size=14, family='Arial', weight='bold'),
            tickfont=dict(color='black', size=12)
        ),
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
        <b>Breaking Even: The Path to Sustainability</b><br><br>
        To achieve a break-even point, the farmer needs to produce <b>{break_even_quantity / bag_weight:,.2f} bags</b> 
        (equivalent to <b>{break_even_quantity:,.2f} kg</b>) at the current farmgate price of 
        <b>{farmgate_price*exchange_rate:,.2f} {currency}</b> per kg. Alternatively, with the current yield of <b>{yield_kg:,.2f} kg/ha</b>, the minimum farmgate price 
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