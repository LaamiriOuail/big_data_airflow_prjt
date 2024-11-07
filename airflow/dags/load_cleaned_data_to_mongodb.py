from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import os

TEMP_DIR = "/home/ouaillaamiri/Development/lsi_3/airflow/data/temp"

# Initialize MongoDB connection
def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    return client['olap-store']

# Function to insert data into MongoDB
def insert_data_into_mongodb(data, collection):
    collection.insert_many(data.to_dict('records'))

# Load cleaned data into MongoDB from temp files
def load_cleaned_data_to_mongodb(*args):
    # Read cleaned data from temporary CSV files
    users = pd.read_csv(f'{TEMP_DIR}/users_cleaned.csv')
    products = pd.read_csv(f'{TEMP_DIR}/products_cleaned.csv')
    transactions = pd.read_csv(f'{TEMP_DIR}/transactions_cleaned.csv')

    # Connect to MongoDB
    db = connect_to_mongodb()

    # Insert cleaned data into MongoDB collections
    insert_data_into_mongodb(products, db['products'])
    insert_data_into_mongodb(transactions, db['transactions'])
    insert_data_into_mongodb(users, db['users'])

# Define the Airflow DAG for loading data
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 1),
    'retries': 1,
}

with DAG(
    'load_cleaned_data_to_mongodb',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
) as dag:

    # wait_for_dag1 = ExternalTaskSensor(
    #     task_id='wait_for_extract_transform_clean_data',
    #     external_dag_id='extract_transform_clean_data',  # DAG 1's ID
    #     external_task_id='remove_duplicates',  # Last task in DAG 1
    #     mode='poke',  # Mode for checking completion, 'poke' is recommended for frequent checks
    #     timeout=600,  # Timeout period in seconds, adjust as needed
    #     retry_delay=60,  # Retry delay in seconds
    # )

    load_cleaned_data_task = PythonOperator(
        task_id='load_cleaned_data_to_mongodb',
        python_callable=load_cleaned_data_to_mongodb,
    )

    # Define task dependencies
    # wait_for_dag1 >>
    load_cleaned_data_task
