WITH stg_classification AS (
    SELECT * FROM {{ ref ('stg_classification') }}
)

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key([
    'facet_code',
    'facet_name'
    ]) }} AS id,
    description,
    facet_code,
    facet_name,
    type

FROM stg_classification