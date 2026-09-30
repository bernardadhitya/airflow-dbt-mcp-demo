"""
### Jaffle shop dbt

Builds the `analytics` schema from the raw jaffle shop tables. Cosmos renders every
dbt model as a task group with a `run` task followed by its `test` task, so a failing
test points at the exact model.

Triggered when `jaffle_ingest` updates `raw.orders` and `raw.payments`.
"""

from datetime import datetime

from cosmos import DbtDag, ExecutionConfig, ProfileConfig, ProjectConfig, RenderConfig
from cosmos.constants import InvocationMode
from cosmos.profiles import PostgresUserPasswordProfileMapping
from jaffle_assets import RAW_ORDERS, RAW_PAYMENTS, WAREHOUSE_CONN_ID

DBT_PROJECT_DIR = "/opt/airflow/dbt_projects/jaffle_shop"
# dbt lives in its own virtualenv (see Dockerfile), so Cosmos shells out to it.
DBT_EXECUTABLE = "/opt/airflow/dbt_venv/bin/dbt"

jaffle_dbt = DbtDag(
    dag_id="jaffle_dbt",
    project_config=ProjectConfig(DBT_PROJECT_DIR, install_dbt_deps=False),
    profile_config=ProfileConfig(
        profile_name="jaffle_shop",
        target_name="dev",
        profile_mapping=PostgresUserPasswordProfileMapping(
            conn_id=WAREHOUSE_CONN_ID,
            profile_args={"schema": "analytics"},
        ),
    ),
    execution_config=ExecutionConfig(
        dbt_executable_path=DBT_EXECUTABLE, invocation_mode=InvocationMode.SUBPROCESS
    ),
    render_config=RenderConfig(
        dbt_executable_path=DBT_EXECUTABLE,
        invocation_mode=InvocationMode.SUBPROCESS,
        # Tests spanning two models (e.g. relationships) get their own task after both parents.
        should_detach_multiple_parents_tests=True,
    ),
    schedule=[RAW_ORDERS, RAW_PAYMENTS],
    start_date=datetime(2026, 9, 1),
    catchup=False,
    max_active_runs=1,
    default_args={"owner": "analytics-engineering", "retries": 0},
    tags=["jaffle_shop", "dbt"],
    doc_md=__doc__,
)
