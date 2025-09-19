import streamlit as st
from ui.main.components import *
from ui.sidebar.components import sidebar
import duckdb
import pandas as pd
import os
import plotly.graph_objects as go
from helpers.dataframe_helpers import convert_nutrients_to_grams

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # project root
DB_PATH = os.path.join(BASE_DIR, "groceries.duckdb")

# Mapping of all nutrients available
NUTRIENT_CATEGORIES = {
    # --- Macros ---
    "Protein": "macro",
    "Fett, totalt": "macro",
    "Kolhydrater, tillgängliga": "macro",
    "Fibrer": "macro",
    "Salt, NaCl": "macro",
    "Vatten": "macro",

    # --- Energy ---
    "Energi (kJ)": "energy",
    "Energi (kcal)": "energy",

    # --- Micronutrients (Vitamins & Minerals) ---
    "Natrium, Na": "micro",
    "Magnesium, Mg": "micro",
    "Kalium, K": "micro",
    "Zink, Zn": "micro",
    "Järn, Fe": "micro",
    "Jod, I": "micro",
    "Kalcium, Ca": "micro",
    "Selen, Se": "micro",
    "Fosfor, P": "micro",

    # Vitamins
    "Vitamin D": "micro",
    "Vitamin D inkl 25-OH-D3": "micro",
    "Tiamin": "micro",   # Vitamin B1
    "Riboflavin": "micro",  # Vitamin B2
    "Niacin": "micro",  # Vitamin B3
    "Niacinekvivalenter": "micro",
    "Vitamin B6": "micro",
    "Folat, totalt": "micro",  # B9
    "Vitamin B12": "micro",
    "Vitamin C": "micro",
    "Vitamin A": "micro",
    "Retinol": "micro",
    "Betakaroten/β-Karoten": "micro",
    "Vitamin E": "micro",

    # --- Sub-nutrients (fatty acids, sugars, alcohol, by-products, etc.) ---
    # Fatty acids
    "Summa mättade fettsyror": "sub",
    "Summa enkelomättade fettsyror": "sub",
    "Summa fleromättade fettsyror": "sub",
    "Fettsyra 4:0-10:0": "sub",
    "Laurinsyra C12:0": "sub",
    "Myristinsyra C14:0": "sub",
    "Palmitinsyra C16:0": "sub",
    "Palmitoljesyra C16:1": "sub",
    "Stearinsyra C18:0": "sub",
    "Oljesyra C18:1": "sub",
    "Linolsyra C18:2": "sub",
    "Linolensyra C18:3": "sub",
    "Arakidonsyra C20:4": "sub",
    "Arakidinsyra C20:0": "sub",
    "EPA (C20:5)": "sub",
    "DPA (C22:5)": "sub",
    "DHA (C22:6)": "sub",

    # Sugars
    "Sockerarter, totalt": "sub",
    "Monosackarider": "sub",
    "Disackarider": "sub",
    "Sackaros": "sub",
    "Fritt socker": "sub",
    "Tillsatt socker": "sub",

    # Other
    "Kolesterol": "sub",
    "Alkohol": "sub",
    "Fullkorn totalt": "sub",
    "Aska": "sub",
    "Avfall (skal etc.)": "sub",  # non-nutrient but reported
}


def categorize_nutrients(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Split nutrients into categories based on mapping."""
    def get_category(nutrient):
        return NUTRIENT_CATEGORIES.get(nutrient, "micro")
    
    df["category"] = df["nutrient"].map(get_category)
    
    return {
        "macros": df[df["category"] == "macro"],
        "energy": df[df["category"] == "energy"],
        "subs": df[df["category"] == "sub"],
        "micros": df[df["category"] == "micro"]
    }

# Donut chart function
def OLD_create_donut_chart(data, labels: str, values: str):
    labels = data[labels]
    values = data[values]

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.15,
            xanchor="left",
            x=0.05,
        ),
        width=500,
        height=500
    )
    return fig

def create_donut_chart(data, energy_kcal: float):
    fig = go.Figure(data=[go.Pie(
        labels=data["nutrient"],
        values=data["nutrient_value"],
        hole=.6
    )])

    # Add kcal annotation in center
    if energy_kcal is not None:
        fig.add_annotation(
            text=f"{energy_kcal:.0f} kcal",
            showarrow=False,
            font=dict(size=16, color="black"),
            x=0.5, y=0.5
        )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.15,
            xanchor="left",
            x=0.05,
        ),
        width=500,
        height=500
    )
    return fig

def create_micro_bar_chart(data):
    fig = go.Figure(data=[go.Bar(
        x=data["nutrient_value"],
        y=data["nutrient"],
        orientation="h"
    )])
    fig.update_layout(
        title="",
        height=600
    )
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
    ORDER BY fgn.nutrient_value DESC
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
        # Load in all options from grocery table
        options = load_grocery_options()

        # Multiselect-box for searching
        selected_groceries = st.multiselect(
            label="Search groceries",
            options=options,
            key="grocery_multiselect"
        )
        
        if selected_groceries:
            # Only handle the first selection (multiple might not be doable)
            grocery = selected_groceries[0]

            df_nutrients = load_grocery_nutrients(grocery)

            # Plot if df_nutrients contains data
            if not df_nutrients.empty:
                # Convert to grams
                df_for_chart = convert_nutrients_to_grams(df_nutrients)
                
                # Categorize
                categorized = categorize_nutrients(df_for_chart)
                macros = categorized["macros"]
                energy = categorized["energy"]
                micros = categorized["micros"]

                # Get kcal value as a float
                energy_row = energy.loc[energy["nutrient"] == "Energi (kcal)", "nutrient_value"]
                energy_kcal = float(energy_row.iloc[0]) if not energy_row.empty else None

                # Layout
                col1, col2, col3 = st.columns(3)
                with col1:
                    # Nutrient dataframe
                    st.subheader(f"Nutrients per 100g for {grocery}")
                    st.dataframe(df_nutrients, width="content", hide_index=True)
                with col2:
                    # Macronutrient chart
                    st.subheader("Nutrient distribution")
                    fig = create_donut_chart(macros, energy_kcal)
                    st.plotly_chart(fig, use_container_width=True)
                with col3:
                    # Micronutrient chart
                    if not micros.empty:
                        st.subheader("Micronutrient levels")
                        fig_micros = create_micro_bar_chart(micros)
                        st.plotly_chart(fig_micros, use_container_width=True)


# Call function to load page
grocery_search_page()
