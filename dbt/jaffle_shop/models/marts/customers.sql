with customers as (
    select * from {{ ref('stg_customers') }}
),

customer_orders as (
    select
        customer_id,
        min(order_date) as first_order_at,
        max(order_date) as most_recent_order_at,
        count(*) as number_of_orders,
        sum(amount) as lifetime_value
    from {{ ref('orders') }}
    where status <> 'returned'
    group by customer_id
)

select
    customers.customer_id,
    customers.first_name,
    customers.last_name,
    customer_orders.first_order_at,
    customer_orders.most_recent_order_at,
    coalesce(customer_orders.number_of_orders, 0) as number_of_orders,
    coalesce(customer_orders.lifetime_value, 0) as lifetime_value
from customers
left join customer_orders using (customer_id)
