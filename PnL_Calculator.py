import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="Seed Requirement Calculator",
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

# Render the sticky navigation bar
st.markdown(
    """
    <div class="navbar">
        <div class="navbar-links">
            <a href="https://integrated-seed-and-gross-margin-calculator.streamlit.app/" class="navbar-button">Seed Requirement Calculator</a>
            <a href="https://gross-margin-calculator.streamlit.app/" class="navbar-link">Gross Margin Calculator</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="centered-title">Seed Requirement Calculator</div>', unsafe_allow_html=True)

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

#___________________________________________________________________________________________________________
# # Define Kenyan counties
# kenyan_counties = [
#     "Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo-Marakwet", "Embu",
#     "Garissa", "Homa Bay", "Isiolo", "Kajiado", "Kakamega", "Kericho",
#     "Kiambu", "Kilifi", "Kirinyaga", "Kisii", "Kisumu", "Kitui",
#     "Kwale", "Laikipia", "Lamu", "Machakos", "Makueni", "Mandera",
#     "Meru", "Migori", "Marsabit", "Mombasa", "Murang'a", "Nairobi",
#     "Nakuru", "Nandi", "Narok", "Nyamira", "Nyandarua", "Nyeri",
#     "Samburu", "Siaya", "Taita-Taveta", "Tana River", "Tharaka Nithi",
#     "Trans Nzoia", "Turkana", "Uasin Gishu", "Vihiga", "Wajir", "West Pokot"
# ]

# data = {
#     "County": kenyan_counties,
#     "Hectares 2023": [
#         42501, 27250, 92847, 44097, 43133, 34500, 142, 78795, 256, 33241, 87532, 40643,
#         30537, 95674, 38467, 66221, 62195, 83618, 60518, 29596, 45800, 138830, 136912,
#         3209, 142379, 78567, 2184, 876, 68399, 758, 71470, 67429, 132396, 48175, 20716,
#         31317, 6448, 77550, 13596, 5734, 26617, 125065, 1750, 117923, 24921, 132, 49097
#     ],
#     "G% Hectares (2023-2028)": [0] * len(kenyan_counties),
#     "2023 % of OPV": [30] * len(kenyan_counties),
#     "2023 % of Hybrid": [70] * len(kenyan_counties),
#     "2023 % of Biotech": [0] * len(kenyan_counties),
#     "2028 % of OPV": [30] * len(kenyan_counties),
#     "2028 % of Hybrid": [70] * len(kenyan_counties),
#     "2028 % of Biotech": [0] * len(kenyan_counties),
#     "Avg Yield OPV": [
#         0.67, 0.70, 0.72, 0.48, 1.04, 0.36, 0.28, 0.44, 0.21, 0.37, 0.45, 0.82,
#         0.29, 0.26, 0.39, 0.54, 0.51, 0.13, 0.30, 0.45, 0.49, 0.38, 0.18, 0.26,
#         0.05, 0.32, 0.39, 0.30, 0.25, 0.27, 0.90, 0.71, 0.71, 0.39, 0.68, 0.34,
#         0.71, 0.45, 0.27, 0.31, 0.38, 1.07, 0.23, 1.21, 0.36, 0.08, 0.59
#     ],
#     "Avg Yield Hybrid": [
#         1.56, 1.62, 1.68, 1.13, 2.44, 0.84, 0.65, 1.03, 0.48, 0.86, 1.06, 1.91,
#         0.68, 0.60, 0.90, 1.26, 1.18, 0.30, 0.71, 1.05, 1.14, 0.88, 0.42, 0.60,
#         0.11, 0.74, 0.90, 0.70, 0.58, 0.62, 2.11, 1.66, 1.66, 0.92, 1.58, 0.79,
#         1.66, 1.04, 0.64, 0.72, 0.89, 2.51, 0.53, 2.83, 0.83, 0.18, 1.37
#     ],
#     "Avg Yield Biotech": [0] * len(kenyan_counties),
# }

df = pd.read_csv('country_data.csv')


st.markdown("""
    <style>
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th {
        background-color: #007278;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ddd;
    }
    td {
        text-align: center;
        padding: 10px;
        border: 1px solid #ddd;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    tr:hover {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Inputs
st.sidebar.header("Global Inputs")

df['Country'] = df['Country'].dropna().str.strip()
country = df['Country'].unique() 
selected_country = st.sidebar.selectbox("Country:", country)


# Filter the DataFrame based on the selected country
filtered_c_df = df[df['Country'] == selected_country]


year = ["2023","2024","2025", "2026", "2027", "2028"]
selected_value_chain = st.sidebar.selectbox("Year:", year)

seed_rate = st.sidebar.number_input("Seed Rate (kg/h):", value=25.0, step=1.0)
#_______________________________________________________________________
st.markdown("""
    <style>
        /* Customize the entire expander container */
        .streamlit-expander {
            border: 2px solid #007278 !important; /* Add a border */
            border-radius: 8px !important; /* Rounded corners */
            margin-bottom: 10px !important; /* Add spacing */
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2); /* Soft shadow */
        }
        
        /* Target the header part of the expander */
        .streamlit-expanderHeader {
            background-color: #007278 !important; /* Background color */
            color: white !important; /* Text color */
            font-size: 16px !important; /* Font size */
            font-weight: bold !important; /* Bold text */
            padding: 10px !important; /* Add padding */
            border-top-left-radius: 8px !important;
            border-top-right-radius: 8px !important;
        }
        
        /* Optional: Style the collapsed arrow icon */
        .streamlit-expanderHeader svg {
            fill: white !important; /* Arrow icon color */
        }
    </style>
""", unsafe_allow_html=True)

#________________________________________________________________________
# Function to dynamically adjust percentages
def adjust_percentages(biotech, opv, country):
    remaining = 100 - biotech  # Remaining percentage after Biotech
    
    if country == "Nigeria":
        opv_start = 90
        hybrid_start = 10
        opv_ratio = 0.9  # 90% of remaining
        hybrid_ratio = 0.1  # 10% of remaining
    else:
        opv_start = 30
        hybrid_start = 70
        opv_ratio = 0.3  # 30% of remaining
        hybrid_ratio = 0.7  # 70% of remaining

    # Start with the predefined OPV and Hybrid values when Biotech is 0
    if biotech == 0:
        adjusted_opv = opv_start
        adjusted_hybrid = hybrid_start
    else:
        adjusted_opv = min(opv, remaining)  # OPV takes as much as possible
        extra_remaining = remaining - adjusted_opv
        
        # Split the extra remaining percentage
        adjusted_opv += opv_ratio * extra_remaining
        adjusted_hybrid = hybrid_ratio * extra_remaining

    return round(adjusted_opv), round(adjusted_hybrid)

with st.sidebar.expander("Select OPV %", expanded=False):
    default_opv_2023 = st.number_input("2023 OPV %", min_value=0, max_value=100, value=30, step=1)
    default_opv_2028 = st.number_input("2028 OPV %", min_value=0, max_value=100, value=30, step=1)
    
biotech_2023 = st.sidebar.slider("2023 Biotech %", 0, 100, 0)
biotech_2028 = st.sidebar.slider("2028 Biotech %", 0, 100, 0)



opv_2023, hybrid_2023 = adjust_percentages(biotech_2023, default_opv_2023, selected_country)
opv_2028, hybrid_2028 = adjust_percentages(biotech_2028, default_opv_2028, selected_country)




filtered_c_df["2023 % of OPV"] = [opv_2023] * len(filtered_c_df)
filtered_c_df["2023 % of Hybrid"] = [hybrid_2023] * len(filtered_c_df)
filtered_c_df["2023 % of Biotech"] = [biotech_2023] * len(filtered_c_df)
filtered_c_df["2028 % of OPV"] = [opv_2028] * len(filtered_c_df)
filtered_c_df["2028 % of Hybrid"] = [hybrid_2028] * len(filtered_c_df)
filtered_c_df["2028 % of Biotech"] = [biotech_2028] * len(filtered_c_df)

# Add calculated columns
filtered_c_df["Hectares 2028"] = (filtered_c_df["Hectares 2023"] * (1 + filtered_c_df["G% Hectares (2023-2028)"] / 100)).round(1)
filtered_c_df["2023 kg seed OPV"] = (filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of OPV"] / 100 * seed_rate).round(1)
filtered_c_df["2023 kg seed Hybrid"] =(filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of Hybrid"] / 100 * seed_rate).round(1)
filtered_c_df["2023 kg seed Biotech"] = (filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of Biotech"] / 100 * seed_rate).round(1)
filtered_c_df["2028 kg seed OPV"] = (filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of OPV"] / 100 * seed_rate).round(1)
filtered_c_df["2028 kg seed Hybrid"] = (filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of Hybrid"] / 100 * seed_rate).round(1)
filtered_c_df["2028 kg seed Biotech"] = (filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of Biotech"] / 100 * seed_rate).round(1)

# filtered_c_df["Production Volume 2023"] = (
#     filtered_c_df["Avg Yield OPV"] * filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of OPV"] / 100 +
#     filtered_c_df["Avg Yield Hybrid"] * filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of Hybrid"] / 100 +
#     filtered_c_df["Avg Yield Biotech"] * filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of Biotech"] / 100
# ).round(1)

filtered_c_df["Production Volume 2023"] = (
    filtered_c_df["Avg Yield OPV"] * filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of OPV"] / 100 +
    filtered_c_df["Avg Yield Hybrid"] * filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of Hybrid"] / 100 +
    (filtered_c_df["Avg Yield Biotech"] * filtered_c_df["Hectares 2023"] * filtered_c_df["2023 % of Biotech"] / 100).fillna(0)
).round(1)


filtered_c_df["Production Volume 2028"] = (
    filtered_c_df["Avg Yield OPV"] * filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of OPV"] / 100 +
    filtered_c_df["Avg Yield Hybrid"] * filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of Hybrid"] / 100 +
    filtered_c_df["Avg Yield Biotech"] * filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of Biotech"] / 100
).round(1)

st.sidebar.header("Scenario Testing")
# Dynamically get unique counties or states from the DataFrame
county_options = filtered_c_df['County/State'].unique()

# Use multi-select to select multiple counties
selected_counties = st.sidebar.multiselect("County/State:", options=county_options, placeholder="Choose a County/State")


new_biotech_percentage = st.sidebar. number_input("2028 Biotech %:", min_value=0, max_value=100, value=0)

update_button = st.sidebar.button("Update")

def update_combined_summary_metrics():
    total_hectares_national = filtered_c_df["Hectares 2023"].sum()
    opv_seed_2028_national = filtered_c_df["2028 kg seed OPV"].sum()
    hybrid_seed_2028_national = filtered_c_df["2028 kg seed Hybrid"].sum()
    total_biotech_hectares_2028_national = (
        (filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of Biotech"] / 100).sum()
    )
    percent_national_hectares_national = (
        (total_biotech_hectares_2028_national / total_hectares_national * 100)
        if total_hectares_national != 0
        else 0
    )
    commercial_seed_2028_national = filtered_c_df["2028 kg seed Biotech"].sum()



    if selected_counties:
        filtered_df = filtered_c_df[filtered_c_df["County/State"].isin(selected_counties)]
        total_hectares_sub = filtered_df["Hectares 2023"].sum()
        opv_seed_2028_sub = filtered_df["2028 kg seed OPV"].sum()
        hybrid_seed_2028_sub = filtered_df["2028 kg seed Hybrid"].sum()
        total_biotech_hectares_2028_sub = (
            (filtered_df["Hectares 2028"] * filtered_df["2028 % of Biotech"] / 100).sum()
        )
        percent_national_hectares_sub = (
            (total_biotech_hectares_2028_sub / total_hectares_sub * 100)
            if total_hectares_sub != 0
            else 0
        )
        commercial_seed_2028_sub = filtered_df["2028 kg seed Biotech"].sum()
    else:
        total_hectares_sub = 0
        opv_seed_2028_sub = 0
        hybrid_seed_2028_sub = 0
        total_biotech_hectares_2028_sub = 0
        percent_national_hectares_sub = 0
        commercial_seed_2028_sub = 0

    summary_data = {
        "Indicator": [
            "Area under maize (Ha)",
            "Area under biotech seed (Ha)",
            "Area under biotech seed (%)",
            "Biotech seed requirement 2028 (Kg)",
            "OPV seed requirement 2028 (Kg)",
            "Hybrid seed requirement 2028 (Kg)",
        ],
        "National": [
            f"{total_hectares_national:,.0f}",
            f"{total_biotech_hectares_2028_national:,.0f}",
            f"{percent_national_hectares_national:.1f}%",
            f"{commercial_seed_2028_national:,.0f}",
            f"{opv_seed_2028_national:,.0f}",
            f"{hybrid_seed_2028_national:,.0f}",
        ],
        "Sub-National":[
            f"{total_hectares_sub:,.0f}" if total_hectares_sub > 0 else "N/A",
            f"{total_biotech_hectares_2028_sub:,.0f}" if total_biotech_hectares_2028_sub > 0 else "N/A",
            f"{percent_national_hectares_sub:.1f}%" if total_hectares_sub > 0 else "N/A",
            f"{commercial_seed_2028_sub:,.0f}" if commercial_seed_2028_sub > 0 else "N/A",
            f"{opv_seed_2028_sub:,.0f}" if opv_seed_2028_sub > 0 else "N/A",
            f"{hybrid_seed_2028_sub:,.0f}" if hybrid_seed_2028_sub > 0 else "N/A",
        ],
    }

    
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
        <div class="cost-breakdown-title">Summary</div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(f"""
    <div style="text-align: center; background-color: #a4343a; color: white; padding: 10px; border-radius: 5px;">
        <b>Updated {', '.join(selected_counties)} , the 2028 Biotech  for the selected county/ies is now: {new_biotech_percentage} %</b>
    </div>
""", unsafe_allow_html=True)

    summary_df = pd.DataFrame(summary_data)

    
    html_table = summary_df.to_html(index=False)

   
    html_table = html_table.replace(
        "<thead>", '<thead style="text-align: center;">'
    )
    st.write(summary_df.to_html(index=False), unsafe_allow_html=True)



# The logic to handle updates
if update_button:
    for county in selected_counties:
        
        filtered_c_df.loc[df["County/State"] == county, "2028 % of Biotech"] = new_biotech_percentage
        
        remaining_percentage = 100 - new_biotech_percentage
        
   
        filtered_c_df.loc[df["County/State"] == county, "2028 % of OPV"] = round(30 / (30 + 70) * remaining_percentage)
        filtered_c_df.loc[df["County/State"] == county, "2028 % of Hybrid"] = (
            100 - new_biotech_percentage - filtered_c_df.loc[df["County/State"] == county, "2028 % of OPV"]
        )
        
        
        filtered_c_df.loc[df["County/State"] == county, "2028 kg seed Biotech"] = (
            filtered_c_df.loc[df["County/State"] == county, "Hectares 2028"] *
            filtered_c_df.loc[df["County/State"] == county, "2028 % of Biotech"] / 100 * seed_rate
        )
        
        
        filtered_c_df.loc[df["County/State"] == county, "Production Volume 2028"] = (
            filtered_c_df.loc[df["County/State"] == county, "Avg Yield OPV"] *
            filtered_c_df.loc[df["County/State"] == county, "Hectares 2028"] *
            filtered_c_df.loc[df["County/State"] == county, "2028 % of OPV"] / 100 +
            filtered_c_df.loc[df["County/State"] == county, "Avg Yield Hybrid"] *
            filtered_c_df.loc[df["County/State"] == county, "Hectares 2028"] *
            filtered_c_df.loc[df["County/State"] == county, "2028 % of Hybrid"] / 100 +
            filtered_c_df.loc[df["County/State"] == county, "Avg Yield Biotech"] *
            filtered_c_df.loc[df["County/State"] == county, "Hectares 2028"] *
            filtered_c_df.loc[df["County/State"] == county, "2028 % of Biotech"] / 100
        )
    
formatted_df = filtered_c_df.copy()

columns_to_round = ["Avg Yield OPV", "Avg Yield Hybrid", "Avg Yield Biotech"]
for col in columns_to_round:
    if col in formatted_df.columns:
        formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.1f}" if pd.notnull(x) else x)


for col in formatted_df.columns:
    if col not in columns_to_round and pd.api.types.is_numeric_dtype(formatted_df[col]):
        formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else x)

# Render table without showing the "Country" column
columns_to_display = [col for col in formatted_df.columns if col != "Country"]

table_style = """
<style>
    .custom-table-container {{
        max-height: 300px; /* Desired height */
        overflow-y: auto; /* Enable scrolling */
        overflow-x: auto; /* Enable horizontal scrolling */
        width: 100%;
    }}
    .custom-table-container table {{
        width: 100%; /* Make table responsive */
        font-size: 12px; /* Decrease overall text size */
    }}
    .custom-table-container table th, 
    .custom-table-container table td {{
        font-size: 11px; /* Decrease header and cell text size */
        padding: 2px; /* Reduce padding for a compact look */
        text-align: center; /* Center-align text */
    }}
</style>
<div class="custom-table-container">
    {table_html}
</div>
"""
update_combined_summary_metrics()

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
    <div class="cost-breakdown-title">Calculator</div>
    """,
    unsafe_allow_html=True
)

# Render the table
st.markdown(
    table_style.format(
        table_html=formatted_df[columns_to_display].to_html(index=False, escape=False)
    ),
    unsafe_allow_html=True
)
