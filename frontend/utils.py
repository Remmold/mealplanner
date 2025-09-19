import streamlit as st
import requests
import pandas as pd

base_url = "http://127.0.0.1:8000"
endpoint = "/groceries/"

@st.cache_data
def get_list_options():
    r = requests.get(url=base_url+endpoint).json()
    
    return r

def get_nutrients_for_grocery(selected_id:str):

    full_r = requests.get(f"{base_url}{endpoint}{selected_id}").json()
    return pd.DataFrame(full_r)