import streamlit as st
import pathlib

# Main page settings
st.set_page_config(page_title="Meal Planner", page_icon=":shallow_pan_of_food:", layout="wide")

# Load and inject CSS
def load_css():
    css_file = pathlib.Path(__file__).parent / "styles.css"
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS first
load_css()

# Define pages structure
pages = {
    "Main": [
        st.Page("pages/1_Home.py", title="Start", icon="🏠"),
        st.Page("pages/2_Grocery_Catalog.py", title="Livsmedelskatalog", icon="🍓"),
        st.Page("pages/3_My_Recipes.py", title="Mina recept", icon="📖"),
        st.Page("pages/4_Meal_Planning.py", title="Måltidsplanering", icon="📅"),
    ],
    "Mitt hushåll": [
        st.Page("pages/5_Members.py", title="Familjemedlemmar", icon="👥"),
        st.Page("pages/6_Preferences.py", title="Inställningar", icon="❤️"),
        st.Page("pages/7_Dietary_Restrictions.py", title="Kostrestriktioner", icon="🚫"),
    ],
    "Dev" : [
        st.Page("pages/8_Grocery_Search.py", title="DEV Grocery Search", icon="👾"),
    ]
}

# Add navigation
pg = st.navigation(pages)

# Run the selected page
pg.run()
