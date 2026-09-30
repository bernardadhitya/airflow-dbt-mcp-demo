"""
### Silver · transaction

Cleans `bronze.transaction` into `silver.transaction`, an incremental table
partitioned by `business_date`: the Jakarta date the transaction happened.
Each run re-processes the latest business dates, so re-runs are idempotent.

Runs whenever `bronze.transaction` is updated. Updating `silver.transaction` feeds `gold_analytics`.
"""

from airflow.sdk import DAG
from banking_common import BRONZE_TRANSACTION, DEFAULT_ARGS, SILVER_TRANSACTION, START_DATE, dbt_build, publish

with DAG(
    dag_id="silver_transaction",
    description="Cleans bronze.transaction into silver.transaction (incremental by business_date) whenever bronze.transaction updates",
    schedule=[BRONZE_TRANSACTION],
    start_date=START_DATE,
    catchup=False,
    max_active_runs=1,
    default_args={**DEFAULT_ARGS, "owner": "data-engineering"},
    tags=["banking", "silver"],
    doc_md=__doc__,
):
    dbt_build("silver_transaction") >> publish(SILVER_TRANSACTION, watermark="business_date")
