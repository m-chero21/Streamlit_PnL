# Seed Requirement and Gross Margin Calculator App

## Overview

This Streamlit application provides two core functionalities essential for agricultural planning:  
1. 🌱 **Seed Requirement Calculator**: Calculates the seed needed based on user inputs such as area and seed rate.  
2. 💰 **Gross Margin Calculator**: Evaluates costs, revenues, and profits to determine the gross margin for agricultural operations.

## Features
- **Interactive Navigation**:  
  An intuitive navigation bar allows users to switch seamlessly between the calculators.
  
- **Custom Styling and Branding**:  
  Includes custom logos and assets for a professional appearance.

- **Component-based Architecture**:  
  The app is structured using modular components for scalability and maintainability.

## Code Structure
The application is organized into the following directories and files:

### Directory Structure
```
.
├── assets/                    # Assets for icons and logos
│   ├── icons8-remove-96.png   # Icon for UI
│   ├── logo.png               # Primary logo
│   └── logo2.png              # Secondary logo
├── components/                # Reusable UI components
│   ├── side_margin.py         # Sidebar for Gross Margin Calculator
│   └── side_seed.py           # Sidebar for Seed Calculator
├── config/                    # Configuration files and data
│   ├── margin_data.py         # Data for margin calculations
│   └── seed_data.py           # Data for seed calculations
├── resources/                 # Placeholder for additional resources
├── utils/                     # Utility functions (e.g., styling)
├── views/                     # Main views for the app
│   ├── margin.py              # Gross Margin Calculator view
│   └── seed.py                # Seed Calculator view
├── .gitignore                 # Git ignore file
├── app.py                     # Main application file
├── config.toml                # Configuration settings
├── Gross.py                   # **Old Gross Margin calculation script
├── PnL_Calculator.py          # **Old Profit and Loss Calculator script
├── readme.md                  # Project README (this file)
└── requirements.txt           # Python dependencies
```

## Key Files
- **`app.py`**: Entry point of the application. It initializes the app, renders the navigation bar, and handles page routing.
- **`views/seed.py`**: Implements the UI and logic for the Seed Calculator.
- **`views/margin.py`**: Implements the UI and logic for the Gross Margin Calculator.
- **`config/margin_data.py`** and **`config/seed_data.py`**: Contains data models and constants for calculations.
- **`components/side_margin.py`** and **`components/side_seed.py`**: Sidebar components for respective calculators.

## How to Run
1. Clone the repository.
2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```
3. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # For Linux/Mac
   .venv\Scripts\activate     # For Windows
   pip install -r requirements.txt
   ```
4. Launch the app:
   ```bash
   streamlit run app.py
   ```

## Navigation
- **🌱 Seed Calculator**: 
  - Input area, seed rate, and other variables to determine seed requirements.
  - Accessed via the "Seed Calculator" button.
  
- **💰 Gross Margin Calculator**:
  - Input costs, revenues, and other parameters to calculate gross margin.
  - Accessed via the "Gross Margin Calculator" button.

## Dependencies
Dependencies are managed in `requirements.txt`. Install them using:
```bash
pip install -r requirements.txt
```

## Customization
- **Styling**: Update styles in `utils/` to customize the look and feel.
- **Logos**: Replace assets in the `assets/` directory as needed.

---

This modular, user-friendly application is your one-stop solution for efficient agricultural planning and profitability analysis! 🚜📈