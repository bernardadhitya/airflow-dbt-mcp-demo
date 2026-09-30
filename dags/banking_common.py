"""Shared building blocks for the banking DAGs: warehouse assets, schedules and the dbt task group."""

import logging
from datetime import timedelta

import pendulum
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import Asset, CronTriggerTimetable, get_current_context, task
from cosmos import DbtTaskGroup, ExecutionConfig, ProfileConfig, ProjectConfig, RenderConfig
from cosmos.constants import InvocationMode
from cosmos.profiles import PostgresUserPasswordProfileMapping

log = logging.getLogger(__name__)

WAREHOUSE_CONN_ID = "warehouse_db"
DBT_PROJECT_DIR = "/opt/airflow/dbt_projects/banking"
# dbt lives in its own virtualenv (see Dockerfile), so Cosmos shells out to it.
DBT_EXECUTABLE = "/opt/airflow/dbt_venv/bin/dbt"

START_DATE = pendulum.datetime(2026, 9, 1, tz="Asia/Jakarta")
# Bronze extracts land every day at 09:00 WIB. run_immediately makes a fresh deployment
# load today's extract straight away instead of waiting for tomorrow morning.
DAILY_9AM_WIB = CronTriggerTimetable("0 9 * * *", timezone="Asia/Jakarta", run_immediately=True)

DEFAULT_ARGS = {"retries": 2, "retry_delay": timedelta(minutes=2)}


def table_asset(schema: str, table: str) -> Asset:
    return Asset(f"postgres://postgres:5432/warehouse/{schema}/{table}")


BRONZE_CUSTOMER = table_asset("bronze", "customer")
BRONZE_ACCOUNT = table_asset("bronze", "account")
BRONZE_TRANSACTION = table_asset("bronze", "transaction")

SILVER_CUSTOMER = table_asset("silver", "customer")
SILVER_ACCOUNT = table_asset("silver", "account")
SILVER_TRANSACTION = table_asset("silver", "transaction")

GOLD_TABLES = [
    table_asset("gold", name)
    for name in (
        "customer_monthly_cashflow",
        "spending_by_category",
        "merchant_performance",
        "p2p_transfer_network",
        "high_value_transactions",
    )
]


def dbt_build(*select: str) -> DbtTaskGroup:
    """Cosmos task group that builds the selected dbt nodes, each followed by its tests."""
    return DbtTaskGroup(
        group_id="dbt",
        project_config=ProjectConfig(DBT_PROJECT_DIR, install_dbt_deps=False),
        profile_config=ProfileConfig(
            profile_name="banking",
            target_name="dev",
            profile_mapping=PostgresUserPasswordProfileMapping(
                conn_id=WAREHOUSE_CONN_ID,
                profile_args={"schema": "public"},
            ),
        ),
        execution_config=ExecutionConfig(
            dbt_executable_path=DBT_EXECUTABLE, invocation_mode=InvocationMode.SUBPROCESS
        ),
        render_config=RenderConfig(
            select=list(select),
            dbt_executable_path=DBT_EXECUTABLE,
            invocation_mode=InvocationMode.SUBPROCESS,
            # Cosmos would otherwise emit each table's asset as soon as its `run` task finishes,
            # before the tests pass. `publish` below emits it once the tests are green instead.
            emit_datasets=False,
        ),
    )


def publish(*assets: Asset, watermark: str | None = None):
    """Mark warehouse tables as updated, recording row counts (and the latest watermark) on each asset event."""

    @task(outlets=list(assets))
    def publish_assets():
        outlet_events = get_current_context()["outlet_events"]
        hook = PostgresHook(WAREHOUSE_CONN_ID)
        for asset in assets:
            schema, table = asset.uri.split("/")[-2:]
            latest = f'max("{watermark}")' if watermark else "null"
            row_count, latest_value = hook.get_first(f'select count(*), {latest} from "{schema}"."{table}"')
            extra = {"table": f"{schema}.{table}", "row_count": row_count}
            if watermark:
                extra[f"latest_{watermark}"] = str(latest_value)
            outlet_events[asset].extra = extra
            log.info("Published %s: %s", asset.uri, extra)

    return publish_assets()
