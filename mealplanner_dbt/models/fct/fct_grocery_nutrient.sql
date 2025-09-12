-- fct_grocery_nutrient.sql
WITH stg_nutrient AS (
    SELECT * FROM {{ ref('stg_nutrient') }}
),

dim_grocery AS (
    SELECT number, id AS grocery_id FROM {{ ref('dim_grocery') }}
),

dim_nutrient AS (
    SELECT name, abbreviation, measurement_unit, id AS nutrient_id FROM {{ ref('dim_nutrient') }}
)

SELECT 
    dg.grocery_id,
    dn.nutrient_id,
    sn.value          AS nutrient_value,
FROM stg_nutrient AS sn
JOIN dim_grocery AS dg on sn.grocery_number = dg.number
-- This below is to mirror the surrogate key in dim_nutrient
JOIN dim_nutrient AS dn on 
            sn.name = dn.name and
            sn.abbreviation = dn.abbreviation and
            sn.measurement_unit = dn.measurement_unit