from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
import pytz

# Initialize MongoDB connection
def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    return client['olap-store']  # Remplacez 'olap-store' par le nom de votre base de données

# Function to count documents added this month
def count_added_this_month(collection, date_field):
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    start_of_month_timestamp = int(start_of_month.timestamp() * 1000)  # Convert to milliseconds
    count = collection.count_documents({date_field: {'$gte': start_of_month_timestamp}})
    return count

# Function to get the count of documents in each collection
def get_collection_counts():
    db = connect_to_mongodb()
    
    user_count = db['users'].count_documents({})
    product_count = db['products'].count_documents({})
    transaction_count = db['transactions'].count_documents({})
    transactions_added_this_month = count_added_this_month(db['transactions'], 'transaction_date')
    
    return {
        'user_count': user_count,
        'product_count': product_count,
        'transaction_count': transaction_count,
        'transactions_added_this_month': transactions_added_this_month
    }

# Function to get unique values
def get_unique_values():
    db = connect_to_mongodb()

    transaction_dates = db['transactions'].distinct('transaction_date')
    
    unique_years = set()
    for date in transaction_dates:
        try:
            if isinstance(date, int):
                year = datetime.fromtimestamp(date / 1000).year
                unique_years.add(year)
            elif isinstance(date, str):
                year = datetime.strptime(date, "%Y-%m-%d").year
                unique_years.add(year)
        except (ValueError, TypeError):
            print(f"Skipping invalid date format: {date}")
    
    unique_product_categories = db['products'].distinct('category')
    unique_user_locations = db['users'].distinct('city')

    return {
        "unique_years": sorted(unique_years),
        "unique_product_categories": unique_product_categories,
        "unique_user_locations": unique_user_locations
    }

# Function to retrieve data from a specific collection
def get_data(collection_name):
    db = connect_to_mongodb()

    if collection_name == 'transactions':
        transactions = pd.DataFrame(list(db['transactions'].find({}, {'user_id': 1, 'product_id': 1, 'amount': 1, 'transaction_date': 1})))
        # Convert transaction_date from Unix timestamp if necessary
        if pd.api.types.is_integer_dtype(transactions['transaction_date']):
            transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'], unit='ms')
        transactions['year'] = transactions['transaction_date'].dt.year
        transactions['month'] = transactions['transaction_date'].dt.month
        return transactions

    elif collection_name == 'products':
        products = pd.DataFrame(list(db['products'].find({}, {'product_id': 1, 'category': 1, 'price': 1, 'product_name':1})))  # Include 'price' field
        return products

    elif collection_name == 'users':
        users = pd.DataFrame(list(db['users'].find({}, {'user_id': 1, 'city': 1, 'name': 1,})))
        return users

    else:
        return None  # Si la collection demandée n'est pas définie

# Function to analyze sales by year
def sales_by_year():
    df = get_data('transactions')
    sales_by_year = df.groupby('year')['amount'].sum().reset_index(name='total_sales')
    return sales_by_year

# Function to analyze sales by month (across all years)
def sales_by_month():
    df = get_data('transactions')
    sales_by_month = df.groupby('month')['amount'].sum().reset_index(name='total_sales')
    return sales_by_month

# Function to analyze sales by product category
def sales_by_category():
    df = get_data('transactions')
    sales_by_category = df.groupby('category')['amount'].sum().reset_index(name='total_sales')
    return sales_by_category

# Function to analyze sales by location (city)
def sales_by_location():
    df = get_data('transactions')
    sales_by_location = df.groupby('city')['amount'].sum().reset_index(name='total_sales')
    return sales_by_location

# Function to analyze sales by year and month combination
def sales_by_year_month():
    df = get_data('transactions')
    sales_by_year_month = df.groupby(['year', 'month'])['amount'].sum().reset_index(name='total_sales')
    return sales_by_year_month

# Function to analyze sales by specified years, months, and locations
def sales_by_selected_year_month_location(years=None, months=None, locations=None):
    df = get_data('transactions')

    if years:
        df = df[df['year'].isin(years)]
    if months:
        df = df[df['month'].isin(months)]
    if locations:
        df = df[df['city'].isin(locations)]

    sales = df.groupby(['year', 'month', 'city'])['amount'].sum().reset_index(name='total_sales')

    return sales



