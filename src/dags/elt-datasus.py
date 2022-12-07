import datetime

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator


dag_default_args = {
    "owner": "gleyton.dev@gmail.com",
    "retries": 1,
    "retries_delay": 0
}


@dag(
    dag_id="elt-datasus",
    start_date=datetime.datetime(2022, 11, 19),
    max_active_runs=1,
    schedule_interval="@daily",
    default_args=dag_default_args,
    catchup=False,
    tags=["datatus", "elt", "astrosdk"]
)
def load_data():
    init = EmptyOperator(task_id="init")

    end = EmptyOperator(task_id="end")

    init >> end


dag = load_data()
