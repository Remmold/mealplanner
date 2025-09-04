import streamlit as st
from ui.main.components import *
from ui.sidebar.components import sidebar

# Main content
st.title("Welcome to Meal Planner")
sidebar()

with st.container():
    heading("Get Started")
    st.write("Welcome to your personal meal planning assistant! Use the navigation menu to:")
    st.markdown("""
    - Browse and manage your recipes 📖
    - Plan your meals for the week 📅
    - Manage household members and preferences 👥
    """)
