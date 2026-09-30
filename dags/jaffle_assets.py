"""Raw warehouse tables shared between the ingest DAG and the dbt DAG."""

from airflow.sdk import Asset

WAREHOUSE_CONN_ID = "warehouse_db"

RAW_CUSTOMERS = Asset("postgres://postgres:5432/warehouse/raw/customers")
RAW_ORDERS = Asset("postgres://postgres:5432/warehouse/raw/orders")
RAW_PAYMENTS = Asset("postgres://postgres:5432/warehouse/raw/payments")
