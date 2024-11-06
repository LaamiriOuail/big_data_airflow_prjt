from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# 1. Generate User Data
def generate_users(num_users=8000):
    users = []
    for _ in range(num_users):
        users.append({
            "user_id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "city": fake.city(),
            "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=80)
        })
    return pd.DataFrame(users)

# 2. Generate Product Data
def generate_products(num_products=10000):
    categories = ["Electronics", "Clothing", "Home", "Sports", "Books"]
    products = []
    for _ in range(num_products):
        products.append({
            "product_id": fake.uuid4(),
            "product_name": fake.word(),
            "category": random.choice(categories),
            "price": round(random.uniform(5.0, 500.0), 2)
        })
    return pd.DataFrame(products)

# 3. Generate Transaction Data
def generate_transactions(users_df, products_df, num_transactions=50000):
    transactions = []
    for _ in range(num_transactions):
        transaction_date = fake.date_time_between(start_date='-1y', end_date='now')
        transactions.append({
            "transaction_id": fake.uuid4(),
            "user_id": random.choice(users_df['user_id']),
            "product_id": random.choice(products_df['product_id']),
            "amount": random.choice(products_df['price']),
            "transaction_date": transaction_date
        })
    return pd.DataFrame(transactions)

if __name__=="__main__":
    # Generate Data
    users_df = generate_users()
    products_df = generate_products()
    transactions_df = generate_transactions(users_df, products_df)

    # Svae the data

    users_df.to_csv("data/store/users.csv", index=False)
    products_df.to_csv("data/store/products.csv", index=False)
    transactions_df.to_csv("data/store/transactions.csv", index=False)

