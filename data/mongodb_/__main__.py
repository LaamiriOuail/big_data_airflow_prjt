from pymongo import MongoClient
from datetime import datetime
import pandas as pd

# Initialize MongoDB connection
def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    return client['olap-store']

# Function to get the count of documents in each collection
def get_collection_counts():
    db = connect_to_mongodb()
    user_count = db['users'].count_documents({})
    product_count = db['products'].count_documents({})
    transaction_count = db['transactions'].count_documents({})

    print(f'Users count: {user_count}')
    print(f'Products count: {product_count}')
    print(f'Transactions count: {transaction_count}')

    # Return counts (optional, useful for further processing in Airflow)
    return {
        'user_count': user_count,
        'product_count': product_count,
        'transaction_count': transaction_count
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
    
    print(f"Unique transaction years: {sorted(unique_years)}")

    # Get unique product categories (assuming 'category' field exists)
    unique_product_categories = db['products'].distinct('category')
    print(f"Unique product categories: {unique_product_categories}")

    # Get unique user locations (assuming 'location' field exists)
    unique_user_locations = db['users'].distinct('city')
    print(f"Unique user locations: {unique_user_locations}")


# Function to perform analysis on sales by year, month, category, and location
def analyze_sales_data():
    db = connect_to_mongodb()

    # Retrieve data from MongoDB
    transactions = pd.DataFrame(list(db['transactions'].find({}, {'user_id': 1, 'product_id': 1, 'amount': 1, 'transaction_date': 1})))
    products = pd.DataFrame(list(db['products'].find({}, {'product_id': 1, 'category': 1})))
    users = pd.DataFrame(list(db['users'].find({}, {'user_id': 1, 'city': 1})))

    # Check if data is available in all collections
    if transactions.empty or products.empty or users.empty:
        print("One or more collections are empty.")
        return None

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

    # Check for required columns after join and handle missing data
    if 'amount' not in df.columns:
        df['amount'] = 0
    if 'category' not in df.columns:
        df['category'] = 'Unknown'
    if 'city' not in df.columns:
        df['city'] = 'Unknown'

    # Sales analysis by year
    sales_by_year = df.groupby('year')['amount'].sum().reset_index(name='total_sales')
    print("Sales by Year:\n", sales_by_year)

    # Sales analysis by month across all years
    sales_by_month = df.groupby('month')['amount'].sum().reset_index(name='total_sales')
    print("Sales by Month (Across Years):\n", sales_by_month)

    # Sales analysis by category
    sales_by_category = df.groupby('category')['amount'].sum().reset_index(name='total_sales')
    print("Sales by Category:\n", sales_by_category)

    # Sales analysis by user location (city)
    sales_by_location = df.groupby('city')['amount'].sum().reset_index(name='total_sales')
    print("Sales by Location:\n", sales_by_location)

    # Sales analysis by year and month
    sales_by_year_month = df.groupby(['year', 'month'])['amount'].sum().reset_index(name='total_sales')
    print("Sales by Year and Month:\n", sales_by_year_month)

    # Optional: return the data as dictionaries for further use in other parts of your code
    return {
        "sales_by_year": sales_by_year,
        "sales_by_month": sales_by_month,
        "sales_by_category": sales_by_category,
        "sales_by_location": sales_by_location,
        "sales_by_year_month": sales_by_year_month,
    }



analyze_sales_data()