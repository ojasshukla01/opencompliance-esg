with source_data as (
    SELECT * FROM {{ ref('stg_esg_source') }}
)

SELECT
    cast(org_id as varchar) as org_id,
    upper(org_name) as org_name,
    sector,
    country,
    cast(emissions_score as double) as emissions_score,
    cast(labor_compliance_score as double) as labor_compliance_score,
    cast(governance_index as double) as governance_index,
    cast(esg_flagged as boolean) as esg_flagged,
    cast(strptime(cast(report_date as varchar), '%Y-%m-%d') as date) as report_date
FROM source_data
WHERE emissions_score <= 100
