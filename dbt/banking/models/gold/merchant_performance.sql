-- Monthly performance of each merchant among our customers: volume, reach, ticket size, busiest hour.

with merchants as (
    select distinct on (cif) cif, full_name, merchant_category
    from {{ ref('silver_customer') }}
    where merchant_category is not null
    order by cif, business_date desc
),

payments as (
    select * from {{ ref('silver_transaction') }}
    where status = 'SUCCESS'
      and transaction_type in ('PAYMENT', 'BILL_PAYMENT')
)

select
    date_trunc('month', p.business_date)::date as month,
    m.cif as merchant_cif,
    m.full_name as merchant_name,
    m.merchant_category,
    count(*) as transaction_count,
    count(distinct p.source_cif) as unique_customers,
    sum(p.amount) as total_amount,
    round(avg(p.amount)) as avg_ticket_size,
    mode() within group (order by p.hour_of_day_wib) as busiest_hour_wib
from payments p
join merchants m on m.cif = p.beneficiary_cif
group by 1, 2, 3, 4
