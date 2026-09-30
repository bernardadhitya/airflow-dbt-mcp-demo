{{
    config(
        alias='transaction',
        incremental_strategy='delete+insert',
        unique_key='business_date',
        indexes=[{'columns': ['business_date']}, {'columns': ['source_cif']}, {'columns': ['beneficiary_cif']}],
    )
}}

-- Partitioned by business_date, the Jakarta calendar date the transaction happened, so a
-- 00:15 GoFood order lands on the next business date. See silver_customer for how the
-- partitioning works.

with source as (
    select
        *,
        transaction_ts at time zone 'Asia/Jakarta' as transaction_ts_wib
    from {{ ref('bronze_transaction') }}
),

with_business_date as (
    select *, transaction_ts_wib::date as business_date
    from source
)

select
    business_date,
    transaction_id,
    transaction_ts,
    transaction_ts_wib,
    extract(hour from transaction_ts_wib)::int as hour_of_day_wib,
    extract(isodow from transaction_ts_wib)::int as day_of_week,  -- 1 = Monday
    source_cif,
    source_account,
    beneficiary_cif,
    beneficiary_account,
    source_cif = beneficiary_cif as is_own_account_transfer,
    amount,
    currency,
    upper(channel) as channel,
    upper(transaction_type) as transaction_type,
    trim(description) as description,
    upper(status) as status
from with_business_date
{% if is_incremental() %}
where business_date >= (select max(business_date) from {{ this }}) - {{ var('silver_lookback_days') }}
{% endif %}
