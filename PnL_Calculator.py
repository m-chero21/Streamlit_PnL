import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Seed Requirement Calculator",  
    page_icon="logo2.png",  
    layout="wide"
)

LOGO_PATH = "logo.png"  
st.sidebar.image(LOGO_PATH, use_container_width=True)

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

# Initial data
data = {
    "County": kenyan_counties,
    "Hectares 2024": [
        42501, 27250, 92847, 44097, 43133, 34500, 142, 78795, 256, 33241, 87532, 40643,
        30537, 95674, 38467, 66221, 62195, 83618, 60518, 29596, 45800, 138830, 136912,
        3209, 142379, 78567, 2184, 876, 68399, 758, 71470, 67429, 132396, 48175, 20716,
        31317, 6448, 77550, 13596, 5734, 26617, 125065, 1750, 117923, 24921, 132, 49097
    ],
    "G% Hectares (2024-2028)": [0] * len(kenyan_counties),
    "2024 % of OPV": [30] * len(kenyan_counties),
    "2024 % of Hybrid": [70] * len(kenyan_counties),
    "2024 % of Biotech": [0] * len(kenyan_counties),
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

# Sidebar Inputs
st.sidebar.header("Global Inputs")
st.sidebar.markdown("---")
value_chains = ["Maize", "Potatoes", "Coffee", "Rice"]
selected_value_chain = st.sidebar.selectbox(
    label="Value Chain",
    options=value_chains,
)
seed_rate = st.sidebar.number_input("Seed Rate (kg/h):", value=25.0, step=1.0)
biotech_2024 = st.sidebar.slider("2024 Biotech %", 0, 100, 0)
biotech_2028 = st.sidebar.slider("2028 Biotech %", 0, 100, 0)

# Function to adjust percentages
def adjust_percentages(biotech, opv_base, hybrid_base):
    remaining = 100 - biotech
    opv = round(opv_base / (opv_base + hybrid_base) * remaining)
    hybrid = 100 - biotech - opv
    return opv, hybrid

opv_2024, hybrid_2024 = adjust_percentages(biotech_2024, 30, 70)
opv_2028, hybrid_2028 = adjust_percentages(biotech_2028, 30, 70)

df["2024 % of OPV"] = [opv_2024] * len(df)
df["2024 % of Hybrid"] = [hybrid_2024] * len(df)
df["2024 % of Biotech"] = [biotech_2024] * len(df)
df["2028 % of OPV"] = [opv_2028] * len(df)
df["2028 % of Hybrid"] = [hybrid_2028] * len(df)
df["2028 % of Biotech"] = [biotech_2028] * len(df)

# Add calculated columns
df["Hectares 2028"] = df["Hectares 2024"] * (1 + df["G% Hectares (2024-2028)"] / 100)
df["Biotech Hectares 2028"] = df["Hectares 2028"] * df["2028 % of Biotech"] / 100
df["2024 kg seed OPV"] = df["Hectares 2024"] * df["2024 % of OPV"] / 100 * seed_rate
df["2024 kg seed Hybrid"] = df["Hectares 2024"] * df["2024 % of Hybrid"] / 100 * seed_rate
df["2024 kg seed Biotech"] = df["Hectares 2024"] * df["2024 % of Biotech"] / 100 * seed_rate
df["2028 kg seed OPV"] = df["Hectares 2028"] * df["2028 % of OPV"] / 100 * seed_rate
df["2028 kg seed Hybrid"] = df["Hectares 2028"] * df["2028 % of Hybrid"] / 100 * seed_rate
df["2028 kg seed Biotech"] = df["Hectares 2028"] * df["2028 % of Biotech"] / 100 * seed_rate
df["Production Volume 2024"] = (
    df["Avg Yield OPV"] * df["Hectares 2024"] * df["2024 % of OPV"] / 100 +
    df["Avg Yield Hybrid"] * df["Hectares 2024"] * df["2024 % of Hybrid"] / 100
)
df["Production Volume 2028"] = (
    df["Avg Yield OPV"] * df["Hectares 2028"] * df["2028 % of OPV"] / 100 +
    df["Avg Yield Hybrid"] * df["Hectares 2028"] * df["2028 % of Hybrid"] / 100 +
    df["Avg Yield Biotech"] * df["Hectares 2028"] * df["2028 % of Biotech"] / 100
)

# Sidebar Summary Widgets
st.sidebar.header("Summary Metrics")

total_hectares = df["Hectares 2024"].sum()
total_biotech_hectares_2028 = df["Biotech Hectares 2028"].sum()
percent_national_hectares = (
    (total_biotech_hectares_2028 / total_hectares * 100) if total_hectares != 0 else 0
)
commercial_seed_2028 = df["2028 kg seed Biotech"].sum()

summary_data = {
    "Metric": [
        "Total Hectares (2024)",
        "Biotech Hectares (2028)",
        "% of National Hectares (2028)",
        "Commercial Seed (2028)",
    ],
    "Value": [
        f"{total_hectares:,.0f}",
        f"{total_biotech_hectares_2028:,.0f}",
        f"{percent_national_hectares:.1f}%",
        f"{commercial_seed_2028:,.0f}",
    ],
}
summary_df = pd.DataFrame(summary_data)
st.sidebar.write(summary_df.to_html(index=False), unsafe_allow_html=True)

# Display the full DataFrame with all columns
st.title("Seed Requirement Calculator")
st.markdown("---")

# st.dataframe(df.reset_index(drop=True), use_container_width=True, height=250)
# Define the desired column order (based on your screenshot)
column_order = [
    "County", "Hectares 2024", "G% Hectares (2024-2028)", "Hectares 2028",
    "2024 % of OPV", "2024 % of Hybrid", "2024 % of Biotech",
    "2028 % of OPV", "2028 % of Hybrid", "2028 % of Biotech",
    "2024 kg seed OPV", "2024 kg seed Hybrid", "2024 kg seed Biotech",
    "2028 kg seed OPV", "2028 kg seed Hybrid", "2028 kg seed Biotech",
    "Avg Yield OPV", "Avg Yield Hybrid", "Avg Yield Biotech",
    "Production Volume 2024", "Production Volume 2028"
]

# Reorder the DataFrame columns
df = df[column_order]
#___________________________________________

# Sort the DataFrame by index
df_sorted = df.sort_index()

# Display the sorted DataFrame in Streamlit
# st.dataframe(df_sorted, use_container_width=True, height=250)

#____________________________________________________________________________________

# Initialize the DataFrame in session state if not already set
if "df" not in st.session_state:
    st.session_state.df = df.copy()

# Display the main table in Streamlit
# Use a placeholder for the table to dynamically update it later
table_placeholder = st.empty()
table_placeholder.dataframe(st.session_state.df, use_container_width=True, height=250)

# Scenario Testing Section
st.header("Scenario Testing")

# Inputs for Scenario Testing
selected_county = st.selectbox("County:", options=kenyan_counties)
new_biotech_percentage = st.number_input(
    "2028 Biotech %:", min_value=0, max_value=100, value=0, key="biotech_input"
)
update_button = st.button("Update")

# Update logic
if update_button:
    # Retrieve the DataFrame from session state
    df = st.session_state.df

    # Update Biotech percentage for the selected county
    df.loc[df["County"] == selected_county, "2028 % of Biotech"] = new_biotech_percentage

    # Dynamically adjust OPV and Hybrid percentages
    remaining_percentage = 100 - new_biotech_percentage
    opv = round(30 / (30 + 70) * remaining_percentage)
    hybrid = 100 - new_biotech_percentage - opv

    df.loc[df["County"] == selected_county, "2028 % of OPV"] = opv
    df.loc[df["County"] == selected_county, "2028 % of Hybrid"] = hybrid

    # Recalculate relevant columns for the updated county
    df.loc[df["County"] == selected_county, "Hectares 2028"] = (
        df.loc[df["County"] == selected_county, "Hectares 2024"] *
        (1 + df.loc[df["County"] == selected_county, "G% Hectares (2024-2028)"] / 100)
    )
    df.loc[df["County"] == selected_county, "Biotech Hectares 2028"] = (
        df.loc[df["County"] == selected_county, "Hectares 2028"] *
        df.loc[df["County"] == selected_county, "2028 % of Biotech"] / 100
    )
    df.loc[df["County"] == selected_county, "2028 kg seed Biotech"] = (
        df.loc[df["County"] == selected_county, "Biotech Hectares 2028"] * seed_rate
    )
    df.loc[df["County"] == selected_county, "Production Volume 2028"] = (
        df.loc[df["County"] == selected_county, "Avg Yield OPV"] *
        df.loc[df["County"] == selected_county, "Hectares 2028"] *
        df.loc[df["County"] == selected_county, "2028 % of OPV"] / 100 +
        df.loc[df["County"] == selected_county, "Avg Yield Hybrid"] *
        df.loc[df["County"] == selected_county, "Hectares 2028"] *
        df.loc[df["County"] == selected_county, "2028 % of Hybrid"] / 100
    )

    # Save the updated DataFrame back to session state
    st.session_state.df = df

    # Update the main table dynamically
    table_placeholder.dataframe(st.session_state.df, use_container_width=True, height=250)
