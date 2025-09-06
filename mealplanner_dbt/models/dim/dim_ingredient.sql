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
    water_weight_change_factor,
    fat_weight_change_factor,
    weight_before_cooking,
    weight_after_cooking,
    yield_factor_name

FROM stg_ingredient