import streamlit as st
# Set up page configuration
st.set_page_config(
    page_title="Integrated Seed and Gross Margin Calculators",
    page_icon="assets/images/logos/SAFIC - Dark.png",
    layout="wide"
)

from views.Seed_Requirement_Calculator import seed
from views.Gross_Margin_Calculator import margin
from utils.file_operations import load_css  

# Initialize session state for page selection
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Seed Requirement Calculator"

# Function to switch pages
def switch_page(page_name):
    st.session_state.selected_page = page_name


# Navigation Bar using Buttons (Avoiding Raw HTML Rendering)
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Seed Requirement Calculator", key="seed", help="Go to Seed Requirement Calculator",
                 use_container_width=True):
        switch_page("Seed Requirement Calculator")

with col2:
    if st.button("Gross Margin Calculator", key="gross", help="Go to Gross Margin Calculator",
                 use_container_width=True):
        switch_page("Gross Margin Calculator")

# Render the selected page
if st.session_state.selected_page == "Seed Requirement Calculator":
    seed()
elif st.session_state.selected_page == "Gross Margin Calculator":
    margin()

# Load additional CSS if necessary
load_css()
