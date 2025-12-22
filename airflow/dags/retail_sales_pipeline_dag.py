from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

PROJECT_ROOT = "/Users/srimurari/Desktop/Repos/retail-sales-analytics"

with DAG(
    dag_id="retail_sales_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    run_pipeline = BashOperator(
        task_id="run_docker_pipeline",
        bash_command=(
            f"docker run --rm "
            f"-v {PROJECT_ROOT}/data:/app/data "
            f"retail-sales-pipeline"
        ),
    )


    run_pipeline
