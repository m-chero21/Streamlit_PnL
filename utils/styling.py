import streamlit as st

def apply_global_styling():
    """Apply global CSS styling."""
    st.markdown(f"""
        <style>
            {header_css}
            {title_css}
            {nav_css}
            {button_css}
            {table_css}
            {cost_css}
        </style>
    """, unsafe_allow_html=True)

def render_navigation_bar():
    """Render the navigation bar."""
    st.markdown("""
        <div class="navbar">
            <a href="https://integrated-seed-and-gross-margin-calculator.streamlit.app/" class="navbar-button">
                Seed Requirement Calculator
            </a>
            <a href="https://gross-margin-calculator.streamlit.app/" class="navbar-link">
                Gross Margin Calculator
            </a>
        </div>
    """, unsafe_allow_html=True)

# Header CSS
header_css = """
/* Hide Streamlit header */
header {visibility: hidden;}

/* Apply serif font globally */
html, body, [class*="st-"] {
    font-family: 'Helvetica', serif;;
}

/* Ensure headers use serif font */
h1, h2, h3, h4, h5, h6 {
    font-family: serif;
}
"""

# Title CSS
title_css =  """
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
    """

# Navigation CSS
nav_css = """
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
    """

# Button CSs
button_css = """
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
    """


cost_css = """
        .cost-breakdown-title {
            color: #007278;
            font-size: 35px;
            font-weight: bold;
            text-align: left;
            margin-bottom: 10px;
        }
    """

table_css = """
            .custom-table-container {{
                max-height: 300px;
                overflow-y: auto;
                overflow-x: auto;
                width: 100%;
            }}
            .custom-table-container table {{
                width: 100%;
                font-size: 12px;
                border-collapse: collapse;
            }}
            .custom-table-container table th,
            .custom-table-container table td {{
                font-size: 11px;
                padding: 5px;
                text-align: center;
                border: 1px solid #ddd;
            }}
            .custom-table-container table th {{
                background-color: #007278;
                color: white;
            }}
        """