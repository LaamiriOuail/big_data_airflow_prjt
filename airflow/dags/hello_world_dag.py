from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define the function to print "Hello, World!"
def print_hello():
    print("Hello, World!")

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 1),
    'retries': 1,
}

# Define the DAG
with DAG(
    'hello_world_dag',
    default_args=default_args,
    description='A simple hello world DAG',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Define the task
    hello_task = PythonOperator(
        task_id='print_hello_task',
        python_callable=print_hello,
    )
