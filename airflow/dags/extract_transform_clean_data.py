from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import json
import psycopg2
from datetime import datetime
import os

BASE = "/home/ouaillaamiri/Development/lsi_3/airflow/data/store"
TEMP_DIR = "/home/ouaillaamiri/Development/lsi_3/airflow/data/temp"

# PostgreSQL connection setup
def connect_to_postgresql():
    conn = psycopg2.connect(
        dbname="olap-store", 
        user="airflow", 
        password="airflow", 
        host="localhost", 
        port="5432"
    )
    return conn

# Extract data from PostgreSQL
def extract_postgresql_data():
    conn = connect_to_postgresql()
    users = pd.read_sql("SELECT * FROM users", conn)
    products = pd.read_sql("SELECT * FROM products", conn)
    transactions = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    return {
        "users": users.to_json(orient="split"),
        "products": products.to_json(orient="split"),
        "transactions": transactions.to_json(orient="split"),
    }

# Extract data from CSV
def extract_csv_data():
    users = pd.read_csv(f'{BASE}/users.csv')
    products = pd.read_csv(f'{BASE}/products.csv')
    transactions = pd.read_csv(f'{BASE}/transactions.csv')
    return {
        "users": users.to_json(orient="split"),
        "products": products.to_json(orient="split"),
        "transactions": transactions.to_json(orient="split"),
    }

# Extract data from JSON files
def extract_json_data():
    with open(f'{BASE}/users.json') as file:
        users = pd.DataFrame(json.load(file))
    with open(f'{BASE}/products.json') as file:
        products = pd.DataFrame(json.load(file))
    with open(f'{BASE}/transactions.json') as file:
        transactions = pd.DataFrame(json.load(file))
    return {
        "users": users.to_json(orient="split"),
        "products": products.to_json(orient="split"),
        "transactions": transactions.to_json(orient="split"),
    }

# Extract data from Excel files
def extract_excel_data():
    users = pd.read_excel(f'{BASE}/users.xlsx')
    products = pd.read_excel(f'{BASE}/products.xlsx')
    transactions = pd.read_excel(f'{BASE}/transactions.xlsx')
    return {
        "users": users.to_json(orient="split"),
        "products": products.to_json(orient="split"),
        "transactions": transactions.to_json(orient="split"),
    }

# Remove duplicates from the extracted data
def remove_duplicates(**kwargs):
    data_sources = ["extract_postgresql_data", "extract_csv_data", "extract_json_data", "extract_excel_data"]
    cleaned_data = {}
    for source in data_sources:
        data = kwargs['ti'].xcom_pull(task_ids=source)
        for key, json_data in data.items():
            df = pd.read_json(json_data, orient="split")
            df_cleaned = df.drop_duplicates()
            cleaned_data[key] = df_cleaned.to_json(orient="split")
    return cleaned_data

# Save cleaned data to temporary files
def save_cleaned_data(**kwargs):
    cleaned_data = kwargs['ti'].xcom_pull(task_ids="remove_duplicates")
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    
    file_paths = {}
    for key, json_data in cleaned_data.items():
        df = pd.read_json(json_data, orient="split")
        file_path = f"{TEMP_DIR}/{key}_cleaned.csv"
        df.to_csv(file_path, index=False)
        file_paths[key] = file_path
    
    print("Cleaned data saved to:", file_paths)
    return file_paths

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 1),
    'retries': 1,
}

with DAG(
    'extract_transform_clean_data',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
) as dag:

    extract_postgres_task = PythonOperator(
        task_id='extract_postgresql_data',
        python_callable=extract_postgresql_data,
    )

    extract_csv_task = PythonOperator(
        task_id='extract_csv_data',
        python_callable=extract_csv_data,
    )

    extract_json_task = PythonOperator(
        task_id='extract_json_data',
        python_callable=extract_json_data,
    )

    extract_excel_task = PythonOperator(
        task_id='extract_excel_data',
        python_callable=extract_excel_data,
    )

    remove_duplicates_task = PythonOperator(
        task_id='remove_duplicates',
        python_callable=remove_duplicates,
        provide_context=True,
    )

    save_cleaned_data_task = PythonOperator(
        task_id='save_cleaned_data',
        python_callable=save_cleaned_data,
        provide_context=True,
    )

    # Task dependencies
    [extract_postgres_task, extract_csv_task, extract_json_task, extract_excel_task] >> remove_duplicates_task >> save_cleaned_data_task
