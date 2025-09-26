import streamlit as st
import requests
import pandas as pd

from mealplanner.utils.constants import BASE_URL, ENDPOINT

@st.cache_data
def get_list_options():
    r = requests.get(url=BASE_URL+ENDPOINT).json()
    return r


def get_nutrients_for_grocery(selected_id:str):
    full_r = requests.get(f"{BASE_URL}{ENDPOINT}{selected_id}").json()
    return pd.DataFrame(full_r)