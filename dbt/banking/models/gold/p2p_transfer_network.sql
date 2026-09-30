-- Who sends money to whom among retail customers: family allowances, split bills, birthday gifts.

with customers as (
    select distinct on (cif) cif, full_name
    from {{ ref('silver_customer') }}
    where customer_type = 'INDIVIDUAL'
    order by cif, business_date desc
)

select
    t.source_cif as sender_cif,
    sender.full_name as sender_name,
    t.beneficiary_cif as receiver_cif,
    receiver.full_name as receiver_name,
    count(*) as transfer_count,
    sum(t.amount) as total_amount,
    min(t.business_date) as first_transfer_date,
    max(t.business_date) as last_transfer_date
from {{ ref('silver_transaction') }} t
join customers sender on sender.cif = t.source_cif
join customers receiver on receiver.cif = t.beneficiary_cif
where t.status = 'SUCCESS'
  and t.transaction_type = 'P2P_TRANSFER'
group by 1, 2, 3, 4
