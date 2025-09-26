import streamlit as st

# Main content
st.title("Welcome to Meal Planner")

with st.container():
    st.header("Get Started")
    st.write("Welcome to your personal meal planning assistant! Use the navigation menu to:")
    st.markdown("""
    - Browse and manage your recipes 📖
    - Plan your meals for the week 📅
    - Manage household members and preferences 👥
    """)
