WITH stg_ingredient AS (
    SELECT * FROM {{ ref('stg_ingredient') }}
),

dim_grocery AS (
    SELECT number, id AS grocery_id FROM {{ ref('dim_grocery') }}
),

dim_ingredient AS (
    SELECT number, name, id AS ingredient_id FROM {{ ref('dim_ingredient') }}
)

SELECT 
    dg.grocery_id,
    di.ingredient_id,
    si.water_weight_change_factor    AS ingredient_water_weight_change_factor,
    si.fat_weight_change_factor      AS ingredient_fat_weight_change_factor,
    si.weight_before_cooking         AS ingredient_weight_before_cooking,
    si.weight_after_cooking          AS ingredient_weight_after_cooking,
    si.yield_factor_name             AS ingredient_yield_factor_name
FROM stg_ingredient si
JOIN dim_grocery dg ON si.grocery_number = dg.number
JOIN dim_ingredient di ON si.name = di.name