-- Outgoing transactions that are unusually large for the customer who made them: at least
-- Rp 1,000,000 and at least 5x their median outgoing amount. A simple starting point for a
-- fraud or AML review queue.

{% set min_amount = 1000000 %}
{% set median_multiple = 5 %}

with customers as (
    select distinct on (cif) cif, full_name
    from {{ ref('silver_customer') }}
    where customer_type = 'INDIVIDUAL'
    order by cif, business_date desc
),

counterparties as (
    select distinct on (cif) cif, full_name
    from {{ ref('silver_customer') }}
    order by cif, business_date desc
),

outgoing as (
    select t.*
    from {{ ref('silver_transaction') }} t
    join customers c on c.cif = t.source_cif
    where t.status = 'SUCCESS'
      and not t.is_own_account_transfer
),

baseline as (
    select source_cif, percentile_cont(0.5) within group (order by amount)::numeric as median_amount
    from outgoing
    group by source_cif
)

select
    o.transaction_id,
    o.business_date,
    o.transaction_ts_wib,
    o.source_cif as cif,
    c.full_name,
    cp.full_name as beneficiary_name,
    o.transaction_type,
    o.channel,
    o.description,
    o.amount,
    round(b.median_amount) as customer_median_amount,
    round(o.amount / b.median_amount, 1) as times_customer_median,
    case when o.hour_of_day_wib < 5 then 'HIGH_VALUE_AT_NIGHT' else 'HIGH_VALUE' end as alert_type
from outgoing o
join baseline b on b.source_cif = o.source_cif
join customers c on c.cif = o.source_cif
left join counterparties cp on cp.cif = o.beneficiary_cif
where o.amount >= {{ min_amount }}
  and o.amount >= {{ median_multiple }} * b.median_amount
