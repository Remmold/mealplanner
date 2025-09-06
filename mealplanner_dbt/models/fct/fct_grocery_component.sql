WITH stg_component AS (
    SELECT * FROM {{ ref('stg_component') }}
),

dim_grocery AS (
    SELECT number, id AS grocery_id FROM {{ ref('dim_grocery') }}
),

dim_component AS (
    SELECT ex2_code, id AS component_id FROM {{ ref('dim_component') }}
)

SELECT 
    dg.grocery_id,
    dc.component_id,
    sc.final_share,
    sc.factor,
    sc.raw_share,
    sc.cooking_style
FROM stg_component sc
JOIN dim_grocery dg ON sc.grocery_number = dg.number
JOIN dim_component dc ON sc.ex2_code = dc.ex2_code