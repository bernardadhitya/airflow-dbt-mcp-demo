"""
### Bronze · account

Loads the account extract into `bronze.account` every day at 09:00 WIB.
The extract is mocked by the dbt seed `bronze_account`.
Each persona has a MAIN account plus savings and spending pockets (kantong);
merchants and companies have one settlement or operating account.

Updating `bronze.account` triggers the `silver_account` DAG.
"""

from airflow.sdk import DAG
from banking_common import BRONZE_ACCOUNT, DAILY_9AM_WIB, DEFAULT_ARGS, START_DATE, dbt_build, publish

with DAG(
    dag_id="bronze_account",
    description="Daily 09:00 WIB (Asia/Jakarta) load of the account extract into bronze.account",
    schedule=DAILY_9AM_WIB,
    start_date=START_DATE,
    catchup=False,
    max_active_runs=1,
    default_args={**DEFAULT_ARGS, "owner": "data-engineering"},
    tags=["banking", "bronze"],
    doc_md=__doc__,
):
    dbt_build("bronze_account") >> publish(BRONZE_ACCOUNT, watermark="updated_at")
