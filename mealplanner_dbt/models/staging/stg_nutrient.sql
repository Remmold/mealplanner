-- stg_nutrient.sql
SELECT 
  grocery_number,
  namn AS name,
  euro_fi_rkod AS euro_fir_code,
  forkortning AS abbreviation,
  varde AS value,
  enhet AS measurement_unit,
  vikt_gram AS weight_gram,
  matrisenhet AS matrix_unit,
  matrisenhetkod AS matrix_unit_code,
  berakning AS calculation,
  vardetyp AS value_type
FROM {{ source ('livsmedelsverket', 'raw_nutrient') }} 