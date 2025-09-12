import streamlit as st
from ui.main.components import *
from ui.sidebar.components import sidebar
import duckdb
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # project root
DB_PATH = os.path.join(BASE_DIR, "groceries.duckdb")


# Donut chart function
def create_donut_chart(data, labels: str, values: str):
    labels = data[labels]
    values = data[values]

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    return fig


# Temporary function for quickly running the query towards duckdb
def run_query(query: str, params: tuple = None) -> pd.DataFrame:
    """Run a SQL query against DuckDB and return a DataFrame."""
    with duckdb.connect(DB_PATH, read_only=True) as conn:
        if params:
            return conn.execute(query, params).fetchdf()
        else:
            return conn.execute(query).fetchdf()
        
@st.cache_data
def load_grocery_options():
    df = run_query("SELECT * FROM refined.dim_grocery")
    return df["name"].drop_duplicates().astype(str).tolist()

@st.cache_data
def load_grocery_nutrients(grocery_name: str) -> pd.DataFrame:
    query = """
    SELECT 
        dn.name AS nutrient,
        fgn.nutrient_value,
        fgn.nutrient_measurement_unit
    FROM refined.fct_grocery_nutrient fgn
    JOIN refined.dim_grocery dg ON fgn.grocery_id = dg.id
    JOIN refined.dim_nutrient dn ON fgn.nutrient_id = dn.id
    WHERE dg.name = ?
    -- AND fgn.nutrient_value != 0
    -- AND nutrient IN ('Energi (kJ)', 'Energi (kcal)', 'Fett, totalt', 'Kolhydrater, tillgängliga', 'Sockerarter, totalt', 'Fibrer', 'Protein', 'Salt, NaCl')
    ORDER BY dn.name
    """
    return run_query(query, (grocery_name,))

# The whole page with its title+content
def grocery_search_page():
    # Debug page
    st.title("Dev page")
    sidebar()
    grocery_search_content()

# The page content
def grocery_search_content():
    with st.container():
        heading("Grocery search")
        st.write("Welcome to your personal meal planning assistant! Use the navigation menu to:")

        # 1. Load in full df from database table so you can search by typing
        options = load_grocery_options()

        # 2. User can search by typing and results will appear live as options
        selected_groceries = st.multiselect(
            label="Search groceries",
            options=options,
            key="grocery_multiselect"
        )
        
        # 3. If a grocery has been selected, a dataframe displaying the
        # nutrients (per 100g) for the selected grocery is displayed,
        # together with a pie chart showing the distribution
        if selected_groceries:
            # Only handle the first selection for now
            grocery = selected_groceries[0]

            df_nutrients = load_grocery_nutrients(grocery)

            if not df_nutrients.empty:
                df_nutrients["share"] = df_nutrients["nutrient_value"] / df_nutrients["nutrient_value"].sum()
                df_donut = df_nutrients[df_nutrients["share"] >= 0.02]
                # Remove energy content from filtered_data
                kj_index = df_donut[(df_donut.nutrient == 'Energi (kJ)')].index
                kcal_index = df_donut[(df_donut.nutrient == 'Energi (kcal)')].index
                df_donut_dropped = df_donut.drop(kj_index)
                df_donut_dropped = df_donut_dropped.drop(kcal_index)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"Nutrients per 100g for {grocery}")
                st.dataframe(df_nutrients, use_container_width=True, hide_index=True)
            with col2:
                st.subheader("Nutrient distribution")
                fig = create_donut_chart(
                    df_donut_dropped,
                    labels="nutrient",
                    values="nutrient_value",
                    )
                st.plotly_chart(fig, use_container_width=True)


# Call function to load page
grocery_search_page()
