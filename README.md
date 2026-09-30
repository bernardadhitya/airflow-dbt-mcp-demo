# Airflow + dbt + MCP demo

A small, local-only Airflow 3 + dbt project for trying out
[astro-airflow-mcp](https://github.com/astronomer/agents/tree/main/astro-airflow-mcp),
an open-source (Apache 2.0) MCP server that works with any Apache Airflow 2.x/3.x through the REST API.

Everything runs in Docker and binds to `127.0.0.1`. Nothing is exposed to your network.

## What's inside

| Piece | What it is |
|---|---|
| Airflow 3.3.2 | LocalExecutor: api-server, scheduler, dag-processor, triggerer |
| Postgres 16 | `airflow` database (Airflow metadata) and `warehouse` database (dbt output) |
| dbt + Cosmos | `dbt/jaffle_shop`, rendered one task group per model by `astronomer-cosmos` |
| MCP server | `astro-airflow-mcp`, run on your machine over stdio, **read-only**, logged in as a Viewer-role user |

### DAGs

| DAG | Schedule | Purpose |
|---|---|---|
| `jaffle_ingest` | every 15 min | Appends fake customers, orders and payments to `warehouse.raw.*`, then updates the raw assets |
| `jaffle_dbt` | when `raw.orders` and `raw.payments` update | dbt staging views and mart tables in `warehouse.analytics`, with tests |
| `partner_api_sync` | every 15 min | Simulated flaky API: timeouts (retried) and bad-data failures, for testing failure diagnosis |

## Run it

Requires Docker with at least 4 GB of memory (8 GB recommended) and [uv](https://docs.astral.sh/uv/).

```bash
cp .env.example .env
docker compose up -d --build
```

- Airflow UI: http://localhost:8080 (admin / admin)
- Warehouse: `postgresql://airflow:airflow@localhost:5433/warehouse`

The DAGs start unpaused, so data and run history build up on their own. To get data right away, trigger `jaffle_ingest` from the UI.

Stop with `docker compose down`. Add `-v` to also wipe the databases.

## Use the MCP server

`.mcp.json` registers the server for Claude Code in this folder. Open Claude Code here, approve the `airflow` server, and ask away.

For other clients (Claude Desktop, Cursor), use the same command and environment variables:

```json
{
  "mcpServers": {
    "airflow": {
      "command": "uvx",
      "args": ["astro-airflow-mcp@0.9.1", "--transport", "stdio"],
      "env": {
        "AIRFLOW_API_URL": "http://localhost:8080",
        "AIRFLOW_USERNAME": "mcp_viewer",
        "AIRFLOW_PASSWORD": "mcp_viewer",
        "AF_READ_ONLY": "true",
        "AF_TELEMETRY_DISABLED": "true"
      }
    }
  }
}
```

Two independent guards keep it read-only: `AF_READ_ONLY=true` makes the MCP server refuse write tools, and the
`mcp_viewer` user has Airflow's Viewer role, so the API rejects writes anyway. `AF_TELEMETRY_DISABLED=true` stops the
server from sending usage telemetry to Astronomer.

### Questions to try

- What DAGs are in this Airflow, and what does each one do?
- Is the Airflow deployment healthy?
- Why did the last failed `partner_api_sync` run fail? Was it a timeout or bad data?
- How often has `partner_api_sync` failed today, and how many failures did retries recover?
- What triggers `jaffle_dbt`, and which DAG produces those assets?
- Which dbt models does `jaffle_dbt` build, and in what order?
- How long does a `jaffle_dbt` run usually take? Which task is slowest?
- Are there any DAG import errors?
