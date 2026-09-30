"""
### Bronze · customer

Loads the core-banking customer (CIF) extract into `bronze.customer` every day at 09:00 WIB.
The extract is mocked by the dbt seed `bronze_customer`.
Six retail personas plus the merchants and companies they transact with, which are
onboarded as business customers with settlement accounts.

Updating `bronze.customer` triggers the `silver_customer` DAG.
"""

from airflow.sdk import DAG
from banking_common import BRONZE_CUSTOMER, DAILY_9AM_WIB, DEFAULT_ARGS, START_DATE, dbt_build, publish

with DAG(
    dag_id="bronze_customer",
    description="Daily 09:00 WIB (Asia/Jakarta) load of the customer extract into bronze.customer",
    schedule=DAILY_9AM_WIB,
    start_date=START_DATE,
    catchup=False,
    max_active_runs=1,
    default_args={**DEFAULT_ARGS, "owner": "data-engineering"},
    tags=["banking", "bronze"],
    doc_md=__doc__,
):
    dbt_build("bronze_customer") >> publish(BRONZE_CUSTOMER, watermark="updated_at")
