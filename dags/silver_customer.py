"""
### Silver · customer

Cleans `bronze.customer` into `silver.customer`, an incremental table
partitioned by `business_date`: the Jakarta date of the customer record's last change.
Each run re-processes the latest business dates, so re-runs are idempotent.

Runs whenever `bronze.customer` is updated. Updating `silver.customer` feeds `gold_analytics`.
"""

from airflow.sdk import DAG
from banking_common import BRONZE_CUSTOMER, DEFAULT_ARGS, SILVER_CUSTOMER, START_DATE, dbt_build, publish

with DAG(
    dag_id="silver_customer",
    description="Cleans bronze.customer into silver.customer (incremental by business_date) whenever bronze.customer updates",
    schedule=[BRONZE_CUSTOMER],
    start_date=START_DATE,
    catchup=False,
    max_active_runs=1,
    default_args={**DEFAULT_ARGS, "owner": "data-engineering"},
    tags=["banking", "silver"],
    doc_md=__doc__,
):
    dbt_build("silver_customer") >> publish(SILVER_CUSTOMER, watermark="business_date")
