"""
### Partner API sync

Pulls the promo feed from a (simulated) partner API and publishes it for marketing.

The partner endpoint is unreliable: roughly a third of calls time out, and the feed
occasionally contains invalid discounts. Retries recover most timeouts, but some runs
still fail, which makes this DAG useful for practicing failure diagnosis.
"""

import logging
import random
from datetime import datetime, timedelta

from airflow.sdk import dag, task

log = logging.getLogger(__name__)


@dag(
    schedule="*/15 * * * *",
    start_date=datetime(2026, 9, 1),
    catchup=False,
    max_active_runs=1,
    default_args={"owner": "data-platform", "retries": 1, "retry_delay": timedelta(seconds=30)},
    tags=["partner", "ingestion"],
    doc_md=__doc__,
)
def partner_api_sync():
    @task
    def fetch_promos():
        if random.random() < 0.35:
            raise TimeoutError("partner-api.example.com did not respond within 30s (GET /v1/promos)")
        promos = [
            {"code": f"PROMO{i:03d}", "discount_pct": random.choice([5, 10, 15, 20, 25])}
            for i in range(random.randint(3, 8))
        ]
        if random.random() < 0.1:
            promos.append({"code": "PROMO999", "discount_pct": 120})
        log.info("Fetched %d promos from partner API", len(promos))
        return promos

    @task(retries=0)
    def validate_promos(promos):
        invalid = [p for p in promos if not 0 < p["discount_pct"] <= 100]
        if invalid:
            raise ValueError(f"Partner feed has invalid discounts (must be 1-100%): {invalid}")
        return promos

    @task
    def publish_promos(promos):
        log.info("Published %d promos: %s", len(promos), ", ".join(p["code"] for p in promos))

    publish_promos(validate_promos(fetch_promos()))


partner_api_sync()
