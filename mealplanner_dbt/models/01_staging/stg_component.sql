SELECT 
  grocery_number,
  food_ex2 AS ex2_code,
  namn AS name,
  tillagning AS cooking_style,
  andel AS final_share,
  faktor AS factor,
  omraknad_till_ra AS raw_share
FROM {{ source ('livsmedelsverket', 'raw_component') }} 