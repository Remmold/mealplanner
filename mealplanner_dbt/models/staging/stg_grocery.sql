SELECT 
  nummer AS id,
  namn AS name,
  version,
FROM {{ source ('livsmedelsverket', 'raw_grocery') }} 