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
# Define Kenyan counties
kenyan_counties = [
    "Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo-Marakwet", "Embu",
    "Garissa", "Homa Bay", "Isiolo", "Kajiado", "Kakamega", "Kericho",
    "Kiambu", "Kilifi", "Kirinyaga", "Kisii", "Kisumu", "Kitui",
    "Kwale", "Laikipia", "Lamu", "Machakos", "Makueni", "Mandera",
    "Meru", "Migori", "Marsabit", "Mombasa", "Murang'a", "Nairobi",
    "Nakuru", "Nandi", "Narok", "Nyamira", "Nyandarua", "Nyeri",
    "Samburu", "Siaya", "Taita-Taveta", "Tana River", "Tharaka Nithi",
    "Trans Nzoia", "Turkana", "Uasin Gishu", "Vihiga", "Wajir", "West Pokot"
]

data = {
    "County": kenyan_counties,
    "Hectares 2023": [
        42501, 27250, 92847, 44097, 43133, 34500, 142, 78795, 256, 33241, 87532, 40643,
        30537, 95674, 38467, 66221, 62195, 83618, 60518, 29596, 45800, 138830, 136912,
        3209, 142379, 78567, 2184, 876, 68399, 758, 71470, 67429, 132396, 48175, 20716,
        31317, 6448, 77550, 13596, 5734, 26617, 125065, 1750, 117923, 24921, 132, 49097
    ],
    "G% Hectares (2023-2028)": [0] * len(kenyan_counties),
    "2023 % of OPV": [30] * len(kenyan_counties),
    "2023 % of Hybrid": [70] * len(kenyan_counties),
    "2023 % of Biotech": [0] * len(kenyan_counties),
    "2028 % of OPV": [30] * len(kenyan_counties),
    "2028 % of Hybrid": [70] * len(kenyan_counties),
    "2028 % of Biotech": [0] * len(kenyan_counties),
    "Avg Yield OPV": [
        0.67, 0.70, 0.72, 0.48, 1.04, 0.36, 0.28, 0.44, 0.21, 0.37, 0.45, 0.82,
        0.29, 0.26, 0.39, 0.54, 0.51, 0.13, 0.30, 0.45, 0.49, 0.38, 0.18, 0.26,
        0.05, 0.32, 0.39, 0.30, 0.25, 0.27, 0.90, 0.71, 0.71, 0.39, 0.68, 0.34,
        0.71, 0.45, 0.27, 0.31, 0.38, 1.07, 0.23, 1.21, 0.36, 0.08, 0.59
    ],
    "Avg Yield Hybrid": [
        1.56, 1.62, 1.68, 1.13, 2.44, 0.84, 0.65, 1.03, 0.48, 0.86, 1.06, 1.91,
        0.68, 0.60, 0.90, 1.26, 1.18, 0.30, 0.71, 1.05, 1.14, 0.88, 0.42, 0.60,
        0.11, 0.74, 0.90, 0.70, 0.58, 0.62, 2.11, 1.66, 1.66, 0.92, 1.58, 0.79,
        1.66, 1.04, 0.64, 0.72, 0.89, 2.51, 0.53, 2.83, 0.83, 0.18, 1.37
    ],
    "Avg Yield Biotech": [0] * len(kenyan_counties),
}

df = pd.DataFrame(data)

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
st.sidebar.markdown("---")
seed_rate = st.sidebar.number_input("Seed Rate (kg/h):", value=25.0, step=1.0)

default_opv_2023 = st.sidebar.number_input("2023 OPV Default %", min_value=0, max_value=100, value=30, step=1)
default_hybrid_2023 = st.sidebar.number_input("2023 Hybrid Default %", min_value=0, max_value=100, value=70, step=1)

default_opv_2028 = st.sidebar.number_input("2028 OPV Default %", min_value=0, max_value=100, value=30, step=1)
default_hybrid_2028 = st.sidebar.number_input("2028 Hybrid Default %", min_value=0, max_value=100, value=70, step=1)
biotech_2023 = st.sidebar.slider("2023 Biotech %", 0, 100, 0)
biotech_2028 = st.sidebar.slider("2028 Biotech %", 0, 100, 0)

# Function to dynamically adjust percentages
def adjust_percentages(biotech, opv_base, hybrid_base):
    remaining = 100 - biotech
    opv = round(opv_base / (opv_base + hybrid_base) * remaining)
    hybrid = 100 - biotech - opv
    return opv, hybrid


opv_2023, hybrid_2023 = adjust_percentages(biotech_2023, default_opv_2023, default_hybrid_2023)
opv_2028, hybrid_2028 = adjust_percentages(biotech_2028, default_opv_2028, default_hybrid_2028)


df["2023 % of OPV"] = [opv_2023] * len(df)
df["2023 % of Hybrid"] = [hybrid_2023] * len(df)
df["2023 % of Biotech"] = [biotech_2023] * len(df)
df["2028 % of OPV"] = [opv_2028] * len(df)
df["2028 % of Hybrid"] = [hybrid_2028] * len(df)
df["2028 % of Biotech"] = [biotech_2028] * len(df)

# Add calculated columns
df["Hectares 2028"] = df["Hectares 2023"] * (1 + df["G% Hectares (2023-2028)"] / 100)
df["2023 kg seed OPV"] = df["Hectares 2023"] * df["2023 % of OPV"] / 100 * seed_rate
df["2023 kg seed Hybrid"] = df["Hectares 2023"] * df["2023 % of Hybrid"] / 100 * seed_rate
df["2023 kg seed Biotech"] = df["Hectares 2023"] * df["2023 % of Biotech"] / 100 * seed_rate
df["2028 kg seed OPV"] = df["Hectares 2028"] * df["2028 % of OPV"] / 100 * seed_rate
df["2028 kg seed Hybrid"] = df["Hectares 2028"] * df["2028 % of Hybrid"] / 100 * seed_rate
df["2028 kg seed Biotech"] = df["Hectares 2028"] * df["2028 % of Biotech"] / 100 * seed_rate
df["Production Volume 2023"] = (
    df["Avg Yield OPV"] * df["Hectares 2023"] * df["2023 % of OPV"] / 100 +
    df["Avg Yield Hybrid"] * df["Hectares 2023"] * df["2023 % of Hybrid"] / 100
)
df["Production Volume 2028"] = (
    df["Avg Yield OPV"] * df["Hectares 2028"] * df["2028 % of OPV"] / 100 +
    df["Avg Yield Hybrid"] * df["Hectares 2028"] * df["2028 % of Hybrid"] / 100 +
    df["Avg Yield Biotech"] * df["Hectares 2028"] * df["2028 % of Biotech"] / 100
)


# Sidebar Summary Metrics
def update_summary_metrics():
    total_hectares = df["Hectares 2023"].sum()
    opv_seed_2028 = df["2028 kg seed OPV"].sum()
    hybrid_seed_2028= df["2028 kg seed OPV"].sum()
    total_biotech_hectares_2028 = (df["Hectares 2028"] * df["2028 % of Biotech"] / 100).sum()
    percent_national_hectares = (
        (total_biotech_hectares_2028 / total_hectares * 100) if total_hectares != 0 else 0
    )
    commercial_seed_2028 = df["2028 kg seed Biotech"].sum()
    opv_seed_2028 = df["2028 kg seed OPV"].sum()
    hybrid_seed_2028= df["2028 kg seed OPV"].sum()

    summary_data = {
        "Indicator": [
            "Area under maize (Ha)",
            "Area under biotech seed (Ha)",
            "National area under biotech seed (%)",
            "Biotech seed requirement 2028 (Kg)",
            "OPV seed requirement 2028 (Kg)",
            "Hybrid seed requirement 2028 (Kg)",
        ],
        "Value": [
            f"{total_hectares:,.0f}",
            f"{total_biotech_hectares_2028:,.0f}",
            f"{percent_national_hectares:.1f}%",
            f"{commercial_seed_2028:,.0f}",
            f"{opv_seed_2028:,.0f}",
            f"{hybrid_seed_2028:,.0f}",


        ],
    }
    st.sidebar.subheader("Summary (National)")
    summary_df = pd.DataFrame(summary_data)
    st.sidebar.write(summary_df.to_html(index=False), unsafe_allow_html=True)

update_summary_metrics()

def update_summary2_metrics():
    opv_seed_2028 = df["2028 kg seed OPV"].sum()
    hybrid_seed_2028= df["2028 kg seed OPV"].sum()
    total_hectares = df["Hectares 2023"].sum()
    total_biotech_hectares_2028 = (df["Hectares 2028"] * df["2028 % of Biotech"] / 100).sum()
    percent_national_hectares = (
        (total_biotech_hectares_2028 / total_hectares * 100) if total_hectares != 0 else 0
    )
    commercial_seed_2028 = df["2028 kg seed Biotech"].sum()


    summary_data = {
        "Indicator": [
            "Area under maize (Ha)",
            "Area under biotech seed (Ha)",
            "National area under biotech Seed (%)",
            "Biotech seed requirement 2028 (Kg)",
            "OPV seed requirement 2028 (Kg)",
            "Hybrid seed requirement 2028 (Kg)",
        ],
        "Value": [
            f"{total_hectares:,.0f}",
            f"{total_biotech_hectares_2028:,.0f}",
            f"{percent_national_hectares:.1f}%",
            f"{commercial_seed_2028:,.0f}",
            f"{opv_seed_2028:,.0f}",
            f"{hybrid_seed_2028:,.0f}",
        ],
    }
    st.sidebar.subheader("Summary (Sub-National)")
    summary_df = pd.DataFrame(summary_data)
    st.sidebar.write(summary_df.to_html(index=False), unsafe_allow_html=True)



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
    <div class="cost-breakdown-title">Scenario Testing</div>
    """,
    unsafe_allow_html=True
)



# Use multi-select to select multiple counties
selected_counties = st.multiselect("Counties:", options=kenyan_counties)

new_biotech_percentage = st.number_input("2028 Biotech %:", min_value=0, max_value=100, value=0)

update_button = st.button("Update")

# The logic to handle updates
if update_button:
    for county in selected_counties:
        
        df.loc[df["County"] == county, "2028 % of Biotech"] = new_biotech_percentage
        
        remaining_percentage = 100 - new_biotech_percentage
        
   
        df.loc[df["County"] == county, "2028 % of OPV"] = round(30 / (30 + 70) * remaining_percentage)
        df.loc[df["County"] == county, "2028 % of Hybrid"] = (
            100 - new_biotech_percentage - df.loc[df["County"] == county, "2028 % of OPV"]
        )
        
        
        df.loc[df["County"] == county, "2028 kg seed Biotech"] = (
            df.loc[df["County"] == county, "Hectares 2028"] *
            df.loc[df["County"] == county, "2028 % of Biotech"] / 100 * seed_rate
        )
        
        
        df.loc[df["County"] == county, "Production Volume 2028"] = (
            df.loc[df["County"] == county, "Avg Yield OPV"] *
            df.loc[df["County"] == county, "Hectares 2028"] *
            df.loc[df["County"] == county, "2028 % of OPV"] / 100 +
            df.loc[df["County"] == county, "Avg Yield Hybrid"] *
            df.loc[df["County"] == county, "Hectares 2028"] *
            df.loc[df["County"] == county, "2028 % of Hybrid"] / 100 +
            df.loc[df["County"] == county, "Avg Yield Biotech"] *
            df.loc[df["County"] == county, "Hectares 2028"] *
            df.loc[df["County"] == county, "2028 % of Biotech"] / 100
        )


    
    update_summary2_metrics()
    
    
    st.markdown(f"""
    <div style="text-align: center; background-color: #a4343a; color: white; padding: 10px; border-radius: 5px;">
        <b>Updated {', '.join(selected_counties)} the 2028 Biotech  for the selected counties is now: {new_biotech_percentage} %</b>
    </div>
""", unsafe_allow_html=True)
    

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
st.markdown(df.to_html(index=False), unsafe_allow_html=True)

