from airflow import DAG
from airflow.operators.python import PythonOperator
from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator
import pandas as pd
import json
import psycopg2
from datetime import datetime

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

# Extract data from PostgreSQL and load to Couchbase
def load_postgresql_data():
    # Connect to PostgreSQL
    conn = connect_to_postgresql()
    
    # Load data from PostgreSQL tables
    users_query = "SELECT * FROM users"
    products_query = "SELECT * FROM products"
    transactions_query = "SELECT * FROM transactions"
    
    users = pd.read_sql(users_query, conn)
    products = pd.read_sql(products_query, conn)
    transactions = pd.read_sql(transactions_query, conn)

    # Close the PostgreSQL connection
    conn.close()

    # Connect to Couchbase
    bucket = connect_to_couchbase()

    # Insert data into Couchbase (embedding or referencing as needed)
    insert_data_into_couchbase(users, bucket, 'user')
    insert_data_into_couchbase(products, bucket, 'product')
    insert_data_into_couchbase(transactions, bucket, 'transaction')
    
BASE = "/home/ouaillaamiri/Development/lsi_3/airflow/data/store"

# Initialize Couchbase connection
def connect_to_couchbase():
    cluster = Cluster('couchbase://localhost', ClusterOptions(PasswordAuthenticator('admin', 'admin')))
    bucket = cluster.bucket('big_data_project')
    return bucket

# Function to insert data into Couchbase (embed or reference)
def insert_data_into_couchbase(data, bucket, doc_type):
    collection = bucket.default_collection()
    
    for idx, row in data.iterrows():
        doc_id = f'{doc_type}_{idx}'
        
        # Convert row to dictionary
        document = row.to_dict()

        # Insert document
        collection.upsert(doc_id, document)

# Load CSV Data
def load_csv_data():
    bucket = connect_to_couchbase()
    
    # Load CSV files
    products = pd.read_csv(f'{BASE}/products.csv')
    transactions = pd.read_csv(f'{BASE}/transactions.csv')
    users = pd.read_csv(f'{BASE}/users.csv')

    # Insert data into Couchbase (embedding or referencing as needed)
    insert_data_into_couchbase(products, bucket, 'product')
    insert_data_into_couchbase(transactions, bucket, 'transaction')
    insert_data_into_couchbase(users, bucket, 'user')

# Load JSON Data
def load_json_data():
    bucket = connect_to_couchbase()
    
    # Load JSON files
    with open(f'{BASE}/products.json', 'r') as file:
        products = json.load(file)
    with open(f'{BASE}/transactions.json', 'r') as file:
        transactions = json.load(file)
    with open(f'{BASE}/users.json', 'r') as file:
        users = json.load(file)

    # Insert data into Couchbase (embedding or referencing as needed)
    insert_data_into_couchbase(pd.DataFrame(products), bucket, 'product')
    insert_data_into_couchbase(pd.DataFrame(transactions), bucket, 'transaction')
    insert_data_into_couchbase(pd.DataFrame(users), bucket, 'user')

# Load Excel Data
def load_excel_data():
    bucket = connect_to_couchbase()

    # Load Excel files
    products = pd.read_excel(f'{BASE}/products.xlsx')
    transactions = pd.read_excel(f'{BASE}/transactions.xlsx')
    users = pd.read_excel(f'{BASE}/users.xlsx')

    # Insert data into Couchbase (embedding or referencing as needed)
    insert_data_into_couchbase(products, bucket, 'product')
    insert_data_into_couchbase(transactions, bucket, 'transaction')
    insert_data_into_couchbase(users, bucket, 'user')

# Define the Airflow DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 1),
    'retries': 1,
}

with DAG(
    'load_data_to_couchbase',
    default_args=default_args,
    schedule_interval='@daily',  # Adjust to your needs
    catchup=False,
) as dag:

    load_csv_task = PythonOperator(
        task_id='load_csv_data',
        python_callable=load_csv_data,
    )

    load_json_task = PythonOperator(
        task_id='load_json_data',
        python_callable=load_json_data,
    )

    load_excel_task = PythonOperator(
        task_id='load_excel_data',
        python_callable=load_excel_data,
    )

    # Define task dependencies
    load_csv_task >> load_json_task >> load_excel_task
