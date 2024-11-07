import pandas as pd
import json
import psycopg2
from datetime import datetime
import time
from pymongo import MongoClient

BASE = "/home/ouaillaamiri/Development/lsi_3/airflow/data/store"


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

# Extract data from PostgreSQL and load to MongoDB
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

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['olap-store']

    # Insert data into MongoDB collections
    insert_data_into_mongodb(products, db['products'])
    insert_data_into_mongodb(transactions, db['transactions'])
    insert_data_into_mongodb(users, db['users'])

# Initialize MongoDB connection
def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    return client['olap-store']

# Function to insert data into MongoDB
def insert_data_into_mongodb(data, collection):
    # Convert rows to dictionaries and insert them into the collection
    collection.insert_many(data.to_dict('records'))

# Load CSV Data
def load_csv_data():
    db = connect_to_mongodb()

    # Load CSV files
    products = pd.read_csv(f'{BASE}/products.csv')
    transactions = pd.read_csv(f'{BASE}/transactions.csv')
    users = pd.read_csv(f'{BASE}/users.csv')

    # Insert data into MongoDB collections
    insert_data_into_mongodb(products, db['products'])
    insert_data_into_mongodb(transactions, db['transactions'])
    insert_data_into_mongodb(users, db['users'])

load_csv_data()