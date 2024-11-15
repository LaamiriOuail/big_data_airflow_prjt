from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import os
import sys
from sqlalchemy.exc import SQLAlchemyError
import subprocess

parent_dir = os.path.abspath(os.path.join(os.getcwd(), 'data'))
sys.path.append(parent_dir)
from models import init_db
from models.product import ProductModel
from models.user import UserModel
from models.transaction import TransactionModel

session = init_db() 

# Initialize Faker
fake = Faker()

# 1. Generate User Data
def generate_users(num_users=7000):
    moroccan_male_first_names = [
        "Ahmed", "Mohamed", "Youssef", "Omar", "Rachid", "Ali", "Hassan", "Abdelkader", 
        "Mustapha", "Abdelilah", "Karim", "Tariq", "Soufiane", "Reda", "Hamza", "Noureddine", 
        "Anas", "Jamal", "Ismail", "Samir", "Said", "Abderrahmane", "Brahim", "Zakaria", "Hakim", 
        "Abdellah", "Aziz", "Mouad", "Ayoub", "El Mehdi", "Salim", "Ilyas", "Idriss", "Khalil", "Ouail"
    ]
    moroccan_female_first_names = [
        "Fatima", "Khadija", "Amina", "Salma", "Imane", "Nadia", "Asmae", "Souad", "Latifa", 
        "Zineb", "Sara", "Ilham", "Houda", "Nour", "Mariam", "Rania", "Loubna", "Yasmina", 
        "Malika", "Najwa", "Safae", "Ghita", "Leila", "Hanane", "Hajar", "Farah", "Soukaina", 
        "Aya", "Rajae", "Wafae", "Siham", "Sanaa", "Amal", "Nisrine", "Samira", "Meryem"
    ]
    moroccan_last_names = [
        "Bennani", "El Amrani", "Fassi", "Bouazza", "Essafi", "El Idrissi", "Bousfiha", "El Khouli", 
        "Jaafari", "Sbai", "Ouazzani", "Lamrabet", "Chaouki", "El Mernissi", "Berkani", "Khalfi", 
        "Tazi", "Mazouz", "Alaoui", "Bahmad", "Belhaj", "Chami", "Sekkat", "Outaleb", "Zerouali", 
        "Bourkadi", "Rachidi", "Kharbouch", "Idrissi", "Mahmoudi", "Akhannouch", "El Mokhtar", 
        "Haddadi", "Boujemaa", "Maazouzi", "Kouhen", "Faris", "Essalhi", "Bouraoui", "Ghallab"
    ]
    moroccan_last_names = [
        "Bennani", "El Amrani", "Fassi", "Bouazza", "Essafi", "El Idrissi", "Bousfiha", "El Khouli", 
        "Jaafari", "Sbai", "Ouazzani", "Lamrabet", "Chaouki", "El Mernissi", "Berkani", "Khalfi", 
        "Tazi", "Mazouz", "Alaoui", "Bahmad", "Belhaj", "Chami", "Sekkat", "Outaleb", "Zerouali", 
        "Bourkadi", "Rachidi", "Kharbouch", "Idrissi", "Mahmoudi", "Akhannouch", "El Mokhtar", 
        "Haddadi", "Boujemaa", "Maazouzi", "Kouhen", "Faris", "Essalhi", "Bouraoui", "Ghallab",
        "Laamiri", "Sadik", "Hadda", "Ziani"
    ]
    moroccan_cities = [
        "Casablanca", "Rabat", "Fes", "Marrakech", "Tangier", "Agadir", "Oujda", "Kenitra",
        "Tetouan", "Safi", "El Jadida", "Nador", "Beni Mellal", "Khouribga", "Mohammedia",
        "Ksar El Kebir", "Taza", "Settat", "Larache", "Essaouira", "Meknes", "Salé",
        "Al Hoceima", "Sidi Kacem", "Ifrane", "Taroudant", "Azrou", "Chefchaouen", 
        "Ouarzazate", "Errachidia", "Berkane", "Midelt", "Sefrou", "Boujdour", "Guelmim", 
        "Laayoune", "Dakhla","Ouazzane"
    ]

    email_domains = [
        "gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "icloud.com",
        "aol.com", "protonmail.com", "zoho.com", "mail.com", "yandex.com",
        "gmx.com", "live.com", "inbox.com", "fastmail.com", "tutanota.com",
        "me.com", "mac.com", "pm.me", "qq.com", "yahoo.co.uk",
        "hotmail.co.uk", "btinternet.com", "verizon.net", "comcast.net", "att.net"
    ]


    users = []
    for _ in range(num_users):
        firstname = random.choice(moroccan_male_first_names + moroccan_female_first_names)
        lastname = random.choice(moroccan_last_names)
        email = str.lower(lastname.replace(" ","."))+"."+str.lower(firstname.replace(" ","."))+"@"+random.choice(email_domains)
        users.append({
            "user_id": fake.uuid4(),
            "name": f"{firstname} {lastname}",
            "email": email,
            "city": random.choice(moroccan_cities),
            "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=80)
        })
    return pd.DataFrame(users)

# Enhance the product name generator
def generate_products(num_products=9000):
    categories = ["Electronics", "Clothing", "Home", "Sports", "Books"]
    descriptors = ["Authentic", "Luxury", "Traditional", "Modern", "Premium", "Eco-Friendly", "Pro", "Ultimate", "Chic", "Elegant"]
    types = {
        "Electronics": ["Phone", "Laptop", "Headphones", "Camera", "Smartwatch", "Tablet", "Speaker"],
        "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress", "Scarf", "Belt"],
        "Home": ["Blender", "Vacuum Cleaner", "Microwave", "Coffee Maker", "Sofa", "Chair", "Table"],
        "Sports": ["Tennis Racket", "Basketball", "Yoga Mat", "Running Shoes", "Dumbbells", "Football", "Badminton Racket"],
        "Books": ["Mystery Novel", "Science Fiction Book", "Cookbook", "Self-Help Guide", "Biography", "Moroccan History", "Travel Guide"]
    }
    local_influences = ["Oasis", "Atlas", "Kasbah", "Marrakech", "Fez", "Casablanca", "Rabat"]
    
    products = []
    for _ in range(num_products):
        category = random.choice(categories)
        product_name = f"{random.choice(descriptors)} {random.choice(types[category])} {random.choice(local_influences)}"
        products.append({
            "product_id": fake.uuid4(),
            "product_name": product_name,
            "category": category,
            "price": round(random.uniform(5.0, 5000.0), 2)
        })
    return pd.DataFrame(products)

# 3. Generate Transaction Data
def generate_transactions(users_df, products_df, num_transactions=30000):
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




# Function to insert data into PostgreSQL
def insert_data_into_postgresql(users_df, products_df, transactions_df):
    try:
        # Insert Users Data
        for _, row in users_df.iterrows():
            try:
                user = UserModel(
                    user_id=row['user_id'],
                    name=row['name'],
                    email=row['email'],
                    city=row['city'],
                    birthdate=row['birthdate']
                )
                session.add(user)
            except SQLAlchemyError as e:
                # Rollback if error occurs while inserting user
                session.rollback()
                print(f"Error inserting user {row['user_id']}")
                continue  # Continue with the next user

        # Insert Products Data
        for _, row in products_df.iterrows():
            try:
                product = ProductModel(
                    product_id=row['product_id'],
                    product_name=row['product_name'],
                    category=row['category'],
                    price=row['price']
                )
                session.add(product)
            except SQLAlchemyError as e:
                # Rollback if error occurs while inserting product
                session.rollback()
                print(f"Error inserting product {row['product_id']}")
                continue  # Continue with the next product

        # Insert Transactions Data
        for _, row in transactions_df.iterrows():
            try:
                transaction = TransactionModel(
                    transaction_id=row['transaction_id'],
                    user_id=row['user_id'],
                    product_id=row['product_id'],
                    amount=row['amount'],
                    transaction_date=row['transaction_date']
                )
                session.add(transaction)
            except SQLAlchemyError as e:
                # Rollback if error occurs while inserting transaction
                session.rollback()
                print(f"Error inserting transaction {row['transaction_id']}")
                continue  # Continue with the next transaction

        # Commit the transaction to the database
        session.commit()

    except Exception as e:
        # Rollback the session for any general errors
        session.rollback()
        print(f"An unexpected error occurred")
    else:
        print("Data inserted successfully")
    finally:
        # Close the session to release the connection
        session.close()


# Convert the DataFrames into SQL INSERT statements and save them to a .sql file
def save_to_sql(df, table_name, file_name):
    with open(file_name, 'w') as f:
        for index, row in df.iterrows():
            insert_statement = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join([repr(val) for val in row])});\n"
            f.write(insert_statement)

def execute_sql_file(file_path):
    try:
        result = subprocess.run(['psql', '-U', 'airflow', '-d', 'olap-store', '-f', file_path], check=True, capture_output=True, text=True)
        print(f"SQL file executed successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing SQL file: {e.stderr}")


if __name__=="__main__":
    # Generate Data
    users_df_a = generate_users()
    products_df_a = generate_products()
    transactions_df_a = generate_transactions(users_df_a, products_df_a)

    # Svae the data

    users_df_a.to_csv("data/store/users.csv", index=False)
    products_df_a.to_csv("data/store/products.csv", index=False)
    transactions_df_a.to_csv("data/store/transactions.csv", index=False)

    products_df_b = generate_products()
    transactions_df_b = generate_transactions(users_df_a, products_df_b)

    users_df_a.to_json("data/store/users.json", orient="records")
    products_df_b.to_json("data/store/products.json", orient="records")
    transactions_df_b.to_json("data/store/transactions.json", orient="records")

    users_df_c = generate_users()
    transactions_df_c = generate_transactions(users_df_c, products_df_b)

    users_df_c.to_excel("data/store/users.xlsx", index=False)
    products_df_b.to_excel("data/store/products.xlsx", index=False)
    transactions_df_c.to_excel("data/store/transactions.xlsx", index=False)

    # Generate Data
    transactions_df_d = generate_transactions(users_df_c, products_df_a,num_transactions=50000)

    # Put data in postgresql

    # insert_data_into_postgresql(users_df_c, products_df_a, transactions_df_d)

    save_to_sql(users_df_c,"users","data/store/users.sql")
    save_to_sql(products_df_a,"products","data/store/products.sql")
    save_to_sql(transactions_df_d,"transactions","data/store/transactions.sql")

    # execute_sql_file("data/store/users.sql")
    # execute_sql_file("data/store/products.sql")
    # execute_sql_file("data/store/transactions.sql")








