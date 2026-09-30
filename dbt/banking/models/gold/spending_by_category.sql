-- Monthly spend per retail customer and merchant category, with each category's share of wallet.

with customers as (
    select distinct on (cif) cif, full_name, segment
    from {{ ref('silver_customer') }}
    where customer_type = 'INDIVIDUAL'
    order by cif, business_date desc
),

merchants as (
    -- Includes SME customers who accept QRIS, like Budi's warung
    select distinct on (cif) cif, merchant_category
    from {{ ref('silver_customer') }}
    where merchant_category is not null
    order by cif, business_date desc
),

spend as (
    select
        date_trunc('month', t.business_date)::date as month,
        t.source_cif as cif,
        m.merchant_category,
        t.amount
    from {{ ref('silver_transaction') }} t
    join merchants m on m.cif = t.beneficiary_cif
    where t.status = 'SUCCESS'
      and t.transaction_type in ('PAYMENT', 'BILL_PAYMENT')
)

select
    s.month,
    c.cif,
    c.full_name,
    c.segment,
    s.merchant_category,
    count(*) as transaction_count,
    sum(s.amount) as total_spend,
    round(100.0 * sum(s.amount) / sum(sum(s.amount)) over (partition by s.month, c.cif), 1) as share_of_wallet_pct
from spend s
join customers c on c.cif = s.cif
group by s.month, c.cif, c.full_name, c.segment, s.merchant_category
