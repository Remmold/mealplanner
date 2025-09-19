import streamlit as st

# -------------------- KLIPPA ÖREN
import requests

base_url = "http://127.0.0.1:8000"
endpoint = "/groceries"
r = requests.get(url=base_url+endpoint).json()


# -------------------- KLIPPA

st.title("Hej och välkomna!")

st.subheader("Välj ett livsmedel du är sugen på att konsumera eller använda!")

# Grocery list to populate selectbox options
options_list = [
    x["grocery_name"] for x in r
]

# Selectbox for choosing a grocery
selected_grocery = st.selectbox(
    label="Välj ett livsmedel",
    options=options_list,
    index=None
)

# If a grocery has been selected
if selected_grocery:
    selected_id = [
        x["grocery_id"] for x in r if x["grocery_name"] == selected_grocery
    ][0]

    st.text(selected_id)

with st.expander(label="response output", expanded=False):
    st.text(r)