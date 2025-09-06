WITH stg_nutrient AS (
    SELECT * FROM {{ ref('stg_nutrient') }}
),

dim_grocery AS (
    SELECT number, id AS grocery_id FROM {{ ref('dim_grocery') }}
),

dim_nutrient AS (
    SELECT name, abbreviation, id AS nutrient_id FROM {{ ref('dim_nutrient') }}
)

SELECT 
    dg.grocery_id,
    dn.nutrient_id,
    sn.value                AS nutrient_value,
    sn.measurement_unit     AS nutrient_measurement_unit
FROM stg_nutrient sn
JOIN dim_grocery dg on sn.grocery_number = dg.number
JOIN dim_nutrient dn on sn.name = dn.name