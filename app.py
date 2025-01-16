import streamlit as st
from views.seed import seed
from views.margin import margin

class App:
    def __init__(self):
        pass

    def render_page(self):
        """Render the appropriate page based on session state."""
        st.set_page_config(layout="wide")

        st.session_state['page_view'] = 'seed'
            
        if st.session_state.page_view == "margin":
            margin()
        else:
            seed()


# Run the application
if __name__ == "__main__":
    app = App()
    app.render_page()
