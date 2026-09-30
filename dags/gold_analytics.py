"""
### Gold · analytics

Builds the analytics tables in the `gold` schema from the three silver tables:

| Table | Question it answers |
|---|---|
| `customer_monthly_cashflow` | How much money came in and went out for each customer, and how much did they save into pockets? |
| `spending_by_category` | Where does each customer spend: minimarkets, e-commerce, AI subscriptions, travel...? |
| `merchant_performance` | Which merchants do our customers use most, with what ticket size, and at what hour? |
| `p2p_transfer_network` | Who sends money to whom: allowances, split bills, family support? |
| `high_value_transactions` | Which outgoing transactions are unusually large for the customer who made them? |

Runs once all of `silver.customer`, `silver.account` and `silver.transaction` have been updated.
"""

from airflow.sdk import DAG
from banking_common import (
    DEFAULT_ARGS,
    GOLD_TABLES,
    SILVER_ACCOUNT,
    SILVER_CUSTOMER,
    SILVER_TRANSACTION,
    START_DATE,
    dbt_build,
    publish,
)

with DAG(
    dag_id="gold_analytics",
    description="Builds the 5 gold analytics tables once silver customer, account and transaction are all updated",
    schedule=(SILVER_CUSTOMER & SILVER_ACCOUNT & SILVER_TRANSACTION),
    start_date=START_DATE,
    catchup=False,
    max_active_runs=1,
    default_args={**DEFAULT_ARGS, "owner": "analytics"},
    tags=["banking", "gold"],
    doc_md=__doc__,
):
    dbt_build("path:models/gold") >> publish(*GOLD_TABLES)
