SELECT 
  nummer AS number,
  namn AS name,
  vatten_faktor AS water_weight_change_factor,
  fett_faktor AS fat_weight_change_factor,
  vikt_fore_tillagning AS weight_before_cooking,
  vikt_efter_tillagning AS weight_after_cooking,
  tillagningsfaktor AS yield_factor_name,
  grocery_number
FROM {{ source ('livsmedelsverket', 'raw_ingredient') }} 