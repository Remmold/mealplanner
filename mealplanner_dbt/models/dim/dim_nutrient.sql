WITH stg_nutrient AS (
    SELECT * FROM {{ ref ('stg_nutrient') }}
)

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key([
    'name',
    'abbreviation'
    ]) }} AS id,
    name,
    abbreviation,
    measurement_unit

FROM stg_nutrient