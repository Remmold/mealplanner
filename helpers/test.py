import pandas as pd
import duckdb
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # project root
DB_PATH = os.path.join(BASE_DIR, "groceries.duckdb")

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
def run_query(query: str, params: tuple = None) -> pd.DataFrame:
    """Run a SQL query against DuckDB and return a DataFrame."""
    with duckdb.connect(DB_PATH, read_only=True) as conn:
        if params:
            return conn.execute(query, params).fetchdf()
        else:
            return conn.execute(query).fetchdf()
        

df = load_grocery_nutrients("Nöt talg")



import io
def convert_nutrients_to_grams(df: pd.DataFrame, decimals: int = 6) -> pd.DataFrame:
    """
    Converts nutrient values in a DataFrame to a standardized 'g' unit and rounds them. 

    This function takes a DataFrame with nutritional data, converts values
    from units like '%', 'mg', and 'µg' to grams ('g'), rounds the result,
    and removes rows with non-mass units like 'kcal' or 'kJ'.

    Args:
        df: A pandas DataFrame expected to have the columns:
            'nutrient' (str): The name of the nutrient.
            'nutrient_value' (float/int): The value of the nutrient.
            'nutrient_measurement_unit' (str): The unit for the value.
        decimals (int, optional): The number of decimal places to round the
                                  final gram value to. Defaults to 6.

    Returns:
        A new pandas DataFrame where all convertible nutrient values are
        expressed in grams and rounded. Rows with units that cannot be
        converted to a mass measurement are excluded.
    """
    # Create a copy to avoid modifying the original DataFrame
    df_copy = df.copy()

    # Define the conversion factors for converting each unit to grams.
    conversion_factors = {
        'g': 1.0,
        'mg': 0.001,        # Milligram to gram
        'µg': 0.000001,     # Microgram to gram
        '%': 1.0            # Assuming X% of a 100g serving is Xg
    }

    # Add a temporary column with the conversion factor for each row
    # If a unit is not in the dictionary, it will get a NaN value.
    df_copy['factor'] = df_copy['nutrient_measurement_unit'].map(conversion_factors)

    # Filter out rows that could not be mapped (i.e., non-mass units)
    df_converted = df_copy.dropna(subset=['factor']).copy()

    # Apply the conversion to the nutrient_value column
    converted_values = df_converted['nutrient_value'] * df_converted['factor']

    # Round the converted values to the specified number of decimals
    df_converted.loc[:, 'nutrient_value'] = converted_values.round(decimals)

    # Update the measurement unit for all rows to 'g'
    df_converted.loc[:, 'nutrient_measurement_unit'] = 'g'

    # Remove the temporary 'factor' column before returning
    df_converted = df_converted.drop(columns=['factor'])

    return df_converted



df = convert_nutrients_to_grams(df)
print(df.value_counts)