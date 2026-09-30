"""
### Bronze · transaction

Loads the transaction extract into `bronze.transaction` every day at 09:00 WIB.
The extract is mocked by the dbt seed `bronze_transaction`.
About 450 transactions from 1 Aug to 29 Sep 2026: payroll, QRIS payments at Indomaret,
Alfamart and the warung, e-commerce, concert tickets, AI subscriptions, hotels,
restaurants, family transfers and moves into savings pockets.

Updating `bronze.transaction` triggers the `silver_transaction` DAG.
"""

from airflow.sdk import DAG
from banking_common import BRONZE_TRANSACTION, DAILY_9AM_WIB, DEFAULT_ARGS, START_DATE, dbt_build, publish

with DAG(
    dag_id="bronze_transaction",
    description="Daily 09:00 WIB (Asia/Jakarta) load of the transaction extract into bronze.transaction",
    schedule=DAILY_9AM_WIB,
    start_date=START_DATE,
    catchup=False,
    max_active_runs=1,
    default_args={**DEFAULT_ARGS, "owner": "data-engineering"},
    tags=["banking", "bronze"],
    doc_md=__doc__,
):
    dbt_build("bronze_transaction") >> publish(BRONZE_TRANSACTION, watermark="transaction_ts")
