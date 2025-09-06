WITH stg_classification AS (
    SELECT * FROM {{ ref('stg_classification') }}
),

dim_grocery AS (
    SELECT number, id AS grocery_id FROM {{ ref('dim_grocery') }}
),

dim_classification AS (
    SELECT facet_code, id AS classification_id FROM {{ ref('dim_classification') }}
)

SELECT 
    dg.grocery_id,
    dc.classification_id,
    sc.description,
    sc.type
FROM stg_classification sc
JOIN dim_grocery dg ON sc.grocery_number = dg.number
JOIN dim_classification dc ON sc.facet_code = dc.facet_code