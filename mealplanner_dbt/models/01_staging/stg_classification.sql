SELECT 
  grocery_number,
  langual_id,
  namn AS description,
  fasettkod AS facet_code,
  fasett AS facet_name,
  typ AS type
FROM {{ source ('livsmedelsverket', 'raw_classification') }} 