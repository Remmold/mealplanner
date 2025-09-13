import io
import pandas as pd
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
