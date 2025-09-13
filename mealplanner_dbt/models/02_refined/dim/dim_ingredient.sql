-- dim_ingredient.sql
WITH stg_ingredient AS (
    SELECT * FROM {{ ref ('stg_ingredient') }}
)

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key([
    'number',
    'name'
    ]) }} AS id,
    number,
    name,
FROM stg_ingredient