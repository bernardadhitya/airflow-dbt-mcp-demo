{{
    config(
        alias='account',
        incremental_strategy='delete+insert',
        unique_key='business_date',
        indexes=[{'columns': ['business_date']}, {'columns': ['account_number']}],
    )
}}

-- Partitioned by business_date, the Jakarta calendar date of the account's last change
-- (opened, renamed, closed...). See silver_customer for how the partitioning works.

with source as (
    select
        *,
        (updated_at at time zone 'Asia/Jakarta')::date as business_date
    from {{ ref('bronze_account') }}
)

select
    business_date,
    account_number,
    cif,
    upper(account_type) as account_type,
    account_type like 'POCKET_%' as is_pocket,
    trim(account_name) as account_name,
    currency,
    upper(status) as status,
    opened_at,
    updated_at
from source
{% if is_incremental() %}
where business_date >= (select max(business_date) from {{ this }}) - {{ var('silver_lookback_days') }}
{% endif %}
