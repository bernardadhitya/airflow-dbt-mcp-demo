FROM apache/airflow:3.3.2

# dbt lives in its own virtualenv so its pins never fight Airflow's.
RUN python -m venv /opt/airflow/dbt_venv \
 && /opt/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-core==1.12.5 dbt-postgres==1.11.0

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" astronomer-cosmos==1.15.1
