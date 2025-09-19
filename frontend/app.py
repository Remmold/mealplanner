import streamlit as st
from utils import get_list_options,get_nutrients_for_grocery

st.title("Hej och välkomna!")

st.subheader("Välj ett livsmedel du är sugen på att konsumera eller använda!")

# Grocery list to populate selectbox options
r = get_list_options()
options_list = [x["grocery_name"] for x in r]

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

    df = get_nutrients_for_grocery(selected_id=selected_id)
    st.dataframe(df,hide_index=True)