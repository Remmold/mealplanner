SELECT 
  nummer AS number,
  namn AS name,
  version
FROM {{ source ('livsmedelsverket', 'raw_grocery') }} 