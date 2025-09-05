SELECT 
  nummer AS ingredient_id,
  namn AS name,
  vatten_faktor AS water_factor,
  fett_faktor AS fat_factor,
  vikt_fore_tillagning AS weight_prior_to_cooking,
  vikt_efter_tillagning AS weight_post_cooking,
  tillagningsfaktor AS cooking_factor,
  grocery_number AS grocery_id,
FROM {{ source ('livsmedelsverket', 'raw_ingredient') }} 