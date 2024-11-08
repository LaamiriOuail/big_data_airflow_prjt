from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
import pytz

# Initialize MongoDB connection
def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    return client['olap-store']

# Function to count documents added this month
def count_added_this_month(collection, date_field):
    # Get the current date and the start of this month
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    
    # Convert the timestamp (in milliseconds) to a datetime object for comparison
    start_of_month_timestamp = int(start_of_month.timestamp() * 1000)  # Convert to milliseconds
    
    # Query to count documents with a transaction_date greater than or equal to the start of this month
    count = collection.count_documents({date_field: {'$gte': start_of_month_timestamp}})
    
    return count

# Function to get the count of documents in each collection
def get_collection_counts():
    db = connect_to_mongodb()
    
    # Get counts for all collections
    user_count = db['users'].count_documents({})
    product_count = db['products'].count_documents({})
    transaction_count = db['transactions'].count_documents({})
    transactions_added_this_month = count_added_this_month(db['transactions'], 'transaction_date')  # Adjust date field if needed
    # Return counts and the counts for items added this month
    return {
        'user_count': user_count,
        'product_count': product_count,
        'transaction_count': transaction_count,
        'transactions_added_this_month': transactions_added_this_month
    }


# Function to get unique years of transactions and unique values in other fields
# Function to get unique years of transactions and unique values in other fields
def get_unique_values():
    db = connect_to_mongodb()

    # Extract unique years from transaction dates
    transaction_dates = db['transactions'].distinct('transaction_date')
    
    unique_years = set()
    for date in transaction_dates:
        try:
            if isinstance(date, int):
                # Convert Unix timestamp (in milliseconds) to datetime
                year = datetime.fromtimestamp(date / 1000).year
                unique_years.add(year)
            elif isinstance(date, str):
                # Handle date if stored as string in "YYYY-MM-DD" format
                year = datetime.strptime(date, "%Y-%m-%d").year
                unique_years.add(year)
        except (ValueError, TypeError):
            print(f"Skipping invalid date format: {date}")
    
    # Get unique product categories (assuming 'category' field exists)
    unique_product_categories = db['products'].distinct('category')

    # Get unique user locations (assuming 'location' field exists)
    unique_user_locations = db['users'].distinct('city')
    return {
        "unique_years": sorted(unique_years),
        "unique_product_categories": unique_product_categories,
        "unique_user_locations": unique_user_locations
    }


# Function to retrieve and join necessary data
def get_data():
    db = connect_to_mongodb()

    # Retrieve data from MongoDB collections
    transactions = pd.DataFrame(list(db['transactions'].find({}, {'user_id': 1, 'product_id': 1, 'amount': 1, 'transaction_date': 1})))
    products = pd.DataFrame(list(db['products'].find({}, {'product_id': 1, 'category': 1})))
    users = pd.DataFrame(list(db['users'].find({}, {'user_id': 1, 'city': 1})))

    # Convert transaction_date from Unix timestamp if necessary
    if pd.api.types.is_integer_dtype(transactions['transaction_date']):
        transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'], unit='ms')

    # Extract year and month from transaction date
    transactions['year'] = transactions['transaction_date'].dt.year
    transactions['month'] = transactions['transaction_date'].dt.month

    # Join transactions with products on product_id to get the category
    df = transactions.merge(products, on='product_id', how='left')

    # Join the result with users on user_id to get the city (location)
    df = df.merge(users, on='user_id', how='left')

    return df

# Function to analyze sales by year
def sales_by_year():
    df = get_data()
    sales_by_year = df.groupby('year')['amount'].sum().reset_index(name='total_sales')
    return sales_by_year

# Function to analyze sales by month (across all years)
def sales_by_month():
    df = get_data()
    sales_by_month = df.groupby('month')['amount'].sum().reset_index(name='total_sales')
    return sales_by_month

# Function to analyze sales by product category
def sales_by_category():
    df = get_data()
    sales_by_category = df.groupby('category')['amount'].sum().reset_index(name='total_sales')
    return sales_by_category

# Function to analyze sales by location (city)
def sales_by_location():
    df = get_data()
    sales_by_location = df.groupby('city')['amount'].sum().reset_index(name='total_sales')
    return sales_by_location

# Function to analyze sales by year and month combination
def sales_by_year_month():
    df = get_data()
    sales_by_year_month = df.groupby(['year', 'month'])['amount'].sum().reset_index(name='total_sales')
    return sales_by_year_month

# Function to analyze sales by specified years, months, and locations
def sales_by_selected_year_month_location(years=None, months=None, locations=None):
    df = get_data()

    # Apply filtering based on user input
    if years:
        df = df[df['year'].isin(years)]
    if months:
        df = df[df['month'].isin(months)]
    if locations:
        df = df[df['city'].isin(locations)]

    # Group the filtered data by the specified criteria and calculate total sales
    sales = df.groupby(['year', 'month', 'city'])['amount'].sum().reset_index(name='total_sales')

    return sales


