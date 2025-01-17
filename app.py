import streamlit as st
from views.seed import seed
from views.margin import margin
from utils.styling import apply_global_styling

class App:
    def __init__(self):
        pass

    
    # Navigation Bar
    def render_navigation_bar(self):
        """Render an inline navigation bar with clickable links using Streamlit."""
        # Initialize session state for active button
        if "active_button" not in st.session_state:
            st.session_state.active_button = "seed"  # Default active button

        # Centered horizontal buttons with active styling
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])  # Side columns for centering

        with col2:  # Center column
            seed_btn = st.button(
                    "🌱 Seed Calculator",
                    key="seed_btn",
                    help="Go to Seed Calculator",
                    use_container_width=True
                )

        with col4:
            margin_btn = st.button(
                "💰 Gross Margin Calculator",
                key="margin_btn",
                help="Go to Gross Margin Calculator",
                use_container_width=True
                )

        # Logic for active button
        if seed_btn:
            st.session_state.active_button = "seed"
        elif margin_btn:
            st.session_state.active_button = "margin"


    def render_page(self):
        """Render the appropriate page based on session state."""
        st.set_page_config(layout="wide")

        # Apply Global CSS Styling
        apply_global_styling()

        # Display navigation bar
        self.render_navigation_bar()
            
        if st.session_state.active_button == "margin":
            margin()
        else:
            seed()


# Run the application
if __name__ == "__main__":
    app = App()
    app.render_page()
