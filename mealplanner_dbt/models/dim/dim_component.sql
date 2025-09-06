WITH stg_component AS (
    SELECT * FROM {{ ref ('stg_component') }}
)

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key([
    'ex2_code',
    'name'
    ]) }} AS id,
    ex2_code,
    name,
    cooking_style,
    final_share,
    factor,
    raw_share    

FROM stg_component