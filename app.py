import streamlit as st
from ui.main.components import *
from ui.sidebar.components import sidebar

# Main page settings
st.set_page_config(page_title="Meal Planner", page_icon=":shallow_pan_of_food:", layout="wide")

# Define pages structure
pages = {
    "Main": [
        st.Page("pages/1_Home.py", title="Home", icon="🏠"),
        st.Page("pages/2_My_Recipes.py", title="My Recipes", icon="📖"),
        st.Page("pages/3_Meal_Planning.py", title="Meal Planning", icon="📅"),
    ],
    "My Household": [
        st.Page("pages/4_Members.py", title="Members", icon="👥"),
        st.Page("pages/5_Preferences.py", title="Preferences", icon="❤️"),
        st.Page("pages/6_Dietary_Restrictions.py", title="Dietary Restrictions", icon="🚫"),
    ]
}

# Add navigation
pg = st.navigation(pages)

# Run the selected page
pg.run()
