-- dim_grocery.sql
WITH stg_grocery AS (
    SELECT * FROM {{ ref ('stg_grocery') }}
)

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key([
    'number',
    'name'
    ]) }} AS id,
    number,
    name,
    version

FROM stg_grocery