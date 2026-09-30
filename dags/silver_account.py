"""
### Silver · account

Cleans `bronze.account` into `silver.account`, an incremental table
partitioned by `business_date`: the Jakarta date of the account's last change.
Each run re-processes the latest business dates, so re-runs are idempotent.

Runs whenever `bronze.account` is updated. Updating `silver.account` feeds `gold_analytics`.
"""

from airflow.sdk import DAG
from banking_common import BRONZE_ACCOUNT, DEFAULT_ARGS, SILVER_ACCOUNT, START_DATE, dbt_build, publish

with DAG(
    dag_id="silver_account",
    description="Cleans bronze.account into silver.account (incremental by business_date) whenever bronze.account updates",
    schedule=[BRONZE_ACCOUNT],
    start_date=START_DATE,
    catchup=False,
    max_active_runs=1,
    default_args={**DEFAULT_ARGS, "owner": "data-engineering"},
    tags=["banking", "silver"],
    doc_md=__doc__,
):
    dbt_build("silver_account") >> publish(SILVER_ACCOUNT, watermark="business_date")
