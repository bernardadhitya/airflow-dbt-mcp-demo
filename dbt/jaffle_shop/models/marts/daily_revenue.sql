select
    order_date::date as order_day,
    count(*) as orders,
    sum(amount) as revenue
from {{ ref('orders') }}
where status <> 'returned'
group by 1
