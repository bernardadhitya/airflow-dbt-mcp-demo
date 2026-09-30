{{
    config(
        alias='customer',
        incremental_strategy='delete+insert',
        unique_key='business_date',
        indexes=[{'columns': ['business_date']}, {'columns': ['cif']}],
    )
}}

-- Partitioned by business_date, the Jakarta calendar date of the record's last change.
-- dbt-postgres has no partition_by, so delete+insert keyed on business_date gives
-- partition-overwrite semantics: each run replaces whole business dates, so re-runs are idempotent.

with source as (
    select
        *,
        (updated_at at time zone 'Asia/Jakarta')::date as business_date
    from {{ ref('bronze_customer') }}
)

select
    business_date,
    cif,
    trim(full_name) as full_name,
    upper(customer_type) as customer_type,
    upper(segment) as segment,
    nullif(upper(merchant_category), '') as merchant_category,
    date_of_birth,
    gender,
    city,
    occupation,
    upper(kyc_risk_level) as kyc_risk_level,
    onboarded_at,
    updated_at
from source
{% if is_incremental() %}
where business_date >= (select max(business_date) from {{ this }}) - {{ var('silver_lookback_days') }}
{% endif %}
