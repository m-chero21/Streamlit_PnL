import streamlit as st
from views.seed import Seed
from views.gross import Gross

class App:
    def __init__(self):
        pass

    def render_page(self):
        """Render the appropriate page based on session state."""
        st.session_state['page_view'] = 'seed'

        st.set_page_config(layout="wide")
        
        if st.session_state.page_view == "gross":
            Gross()
        else:
            Seed()


# Run the application
if __name__ == "__main__":
    app = App()
    app.render_page()
