SELECT 
  grocery_number AS grocery_id,
  namn AS name,
  euro_fi_rkod AS euro_fir_code,
  forkortning AS abreviation,
  varde AS value,
  enhet AS unit_type,
  vikt_gram AS weight_gram,
  matrisenhet AS matrix_unit,
  matrisenhetkod AS matrix_unit_code,
  berakning AS calculation,
  vardetyp AS value_type,
FROM {{ source ('livsmedelsverket', 'raw_grocery_nutrients') }} 