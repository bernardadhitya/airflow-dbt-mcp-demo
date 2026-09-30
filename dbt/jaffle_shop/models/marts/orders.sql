{% set payment_methods = ['credit_card', 'bank_transfer', 'e_wallet', 'gift_card'] %}

with orders as (
    select * from {{ ref('stg_orders') }}
),

payments as (
    select * from {{ ref('stg_payments') }}
),

order_payments as (
    select
        order_id,
        {% for method in payment_methods -%}
        sum(case when payment_method = '{{ method }}' then amount else 0 end) as {{ method }}_amount,
        {% endfor -%}
        sum(amount) as total_amount
    from payments
    group by order_id
)

select
    orders.order_id,
    orders.customer_id,
    orders.order_date,
    orders.status,
    {% for method in payment_methods -%}
    coalesce(order_payments.{{ method }}_amount, 0) as {{ method }}_amount,
    {% endfor -%}
    coalesce(order_payments.total_amount, 0) as amount
from orders
left join order_payments using (order_id)
