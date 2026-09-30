-- Monthly money in / money out per retail customer, and how much they moved into savings pockets.

with customers as (
    select distinct on (cif) cif, full_name, segment
    from {{ ref('silver_customer') }}
    where customer_type = 'INDIVIDUAL'
    order by cif, business_date desc
),

accounts as (
    select distinct on (account_number) account_number, account_type
    from {{ ref('silver_account') }}
    order by account_number, business_date desc
),

transactions as (
    select * from {{ ref('silver_transaction') }}
    where status = 'SUCCESS'
),

movements as (
    -- Money received from someone else
    select beneficiary_cif as cif, business_date, amount as money_in, 0 as money_out, 0 as moved_to_savings
    from transactions
    where not is_own_account_transfer

    union all

    -- Money paid or sent to someone else
    select source_cif, business_date, 0, amount, 0
    from transactions
    where not is_own_account_transfer

    union all

    -- Moves between the customer's own accounts: + into a savings pocket, - out of one
    select
        t.source_cif,
        t.business_date,
        0,
        0,
        case when dst.account_type = 'POCKET_SAVINGS' then t.amount else 0 end
        - case when src.account_type = 'POCKET_SAVINGS' then t.amount else 0 end
    from transactions t
    join accounts src on src.account_number = t.source_account
    join accounts dst on dst.account_number = t.beneficiary_account
    where t.is_own_account_transfer
)

select
    date_trunc('month', m.business_date)::date as month,
    c.cif,
    c.full_name,
    c.segment,
    sum(m.money_in) as money_in,
    sum(m.money_out) as money_out,
    sum(m.money_in) - sum(m.money_out) as net_cashflow,
    sum(m.moved_to_savings) as net_moved_to_savings,
    round(100.0 * sum(m.moved_to_savings) / nullif(sum(m.money_in), 0), 1) as savings_rate_pct
from movements m
join customers c on c.cif = m.cif
group by 1, 2, 3, 4
