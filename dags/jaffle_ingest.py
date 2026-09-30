"""
### Jaffle shop ingest

Simulated extract from the jaffle shop's order system. Every run appends a small
batch of customers, orders and payments to the `raw` schema of the warehouse.

Updating `raw.orders` and `raw.payments` triggers the `jaffle_dbt` DAG downstream.
"""

import random
from datetime import datetime, timedelta, timezone

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import dag, task
from jaffle_assets import RAW_CUSTOMERS, RAW_ORDERS, RAW_PAYMENTS, WAREHOUSE_CONN_ID

FIRST_NAMES = ["Ayu", "Budi", "Citra", "Dewi", "Eko", "Fajar", "Gita", "Hadi", "Indah", "Joko"]
ORDER_STATUSES = ["placed", "shipped", "completed", "returned"]
PAYMENT_METHODS = ["credit_card", "bank_transfer", "e_wallet", "gift_card"]

DDL = """
create schema if not exists raw;
create table if not exists raw.customers (
    id serial primary key,
    first_name text not null,
    last_name text not null,
    created_at timestamptz not null
);
create table if not exists raw.orders (
    id serial primary key,
    customer_id int not null,
    order_date timestamptz not null,
    status text not null
);
create table if not exists raw.payments (
    id serial primary key,
    order_id int not null,
    payment_method text not null,
    amount_cents int not null
);
"""


@dag(
    schedule="*/15 * * * *",
    start_date=datetime(2026, 9, 1),
    catchup=False,
    max_active_runs=1,
    default_args={"owner": "data-platform", "retries": 1, "retry_delay": timedelta(minutes=1)},
    tags=["jaffle_shop", "ingestion"],
    doc_md=__doc__,
)
def jaffle_ingest():
    @task
    def create_raw_tables():
        PostgresHook(WAREHOUSE_CONN_ID).run(DDL)

    @task(outlets=[RAW_CUSTOMERS])
    def load_customers(run_id=None):
        rng = random.Random(f"{run_id}-customers")
        hook = PostgresHook(WAREHOUSE_CONN_ID)
        existing = hook.get_first("select count(*) from raw.customers")[0]
        n = 50 if existing == 0 else rng.randint(0, 3)
        now = datetime.now(timezone.utc)
        rows = [(rng.choice(FIRST_NAMES), f"{chr(rng.randint(65, 90))}.", now) for _ in range(n)]
        if rows:
            hook.insert_rows("raw.customers", rows, target_fields=["first_name", "last_name", "created_at"])
        return n

    @task(outlets=[RAW_ORDERS])
    def load_orders(run_id=None):
        rng = random.Random(f"{run_id}-orders")
        hook = PostgresHook(WAREHOUSE_CONN_ID)
        customer_ids = [r[0] for r in hook.get_records("select id from raw.customers")]
        now = datetime.now(timezone.utc)
        rows = [
            (
                rng.choice(customer_ids),
                now - timedelta(minutes=rng.randint(0, 15)),
                rng.choices(ORDER_STATUSES, weights=[3, 3, 10, 1])[0],
            )
            for _ in range(rng.randint(5, 20))
        ]
        hook.insert_rows("raw.orders", rows, target_fields=["customer_id", "order_date", "status"])
        return len(rows)

    @task(outlets=[RAW_PAYMENTS])
    def load_payments(run_id=None):
        rng = random.Random(f"{run_id}-payments")
        hook = PostgresHook(WAREHOUSE_CONN_ID)
        unpaid = hook.get_records(
            """
            select o.id from raw.orders o
            left join raw.payments p on p.order_id = o.id
            where p.id is null
            """
        )
        rows = [
            (order_id, rng.choice(PAYMENT_METHODS), rng.randint(1_000, 20_000))
            for (order_id,) in unpaid
            for _ in range(rng.choice([1, 1, 1, 2]))
        ]
        if rows:
            hook.insert_rows("raw.payments", rows, target_fields=["order_id", "payment_method", "amount_cents"])
        return len(rows)

    create_raw_tables() >> load_customers() >> load_orders() >> load_payments()


jaffle_ingest()
