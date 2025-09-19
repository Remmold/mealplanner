WITH mart_grocery_nutrion_menu as ( -- This will be a mart later with dbt 
  SELECT
    dg.number AS number,
    dg.name AS grocery_name,
    dn.name AS nutrient_name,
    dn.abbreviation,
    fgn.nutrient_value,
    fgn.nutrient_measurement_unit,
  FROM {{ ref('fct_grocery_nutrient') }} as fgn
  JOIN {{ ref('dim_grocery') }} as dg ON dg.id = fgn.grocery_id
  JOIN {{ ref('dim_nutrient') }} as dn ON dn.id = fgn.nutrient_id
  ORDER BY number
  )

SELECT * FROM mart_grocery_nutrion_menu
