from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

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

if __name__=="__main__":
    # Generate Data
    users_df = generate_users()
    products_df = generate_products()
    transactions_df = generate_transactions(users_df, products_df)

    # Svae the data

    users_df.to_csv("data/store/users.csv", index=False)
    products_df.to_csv("data/store/products.csv", index=False)
    transactions_df.to_csv("data/store/transactions.csv", index=False)

    products_df = generate_products()
    transactions_df = generate_transactions(users_df, products_df)

    users_df.to_json("data/store/users.json", orient="records")
    products_df.to_json("data/store/products.json", orient="records")
    transactions_df.to_json("data/store/transactions.json", orient="records")

    users_df = generate_users()
    transactions_df = generate_transactions(users_df, products_df)

    users_df.to_excel("data/store/users.xlsx", index=False)
    products_df.to_excel("data/store/products.xlsx", index=False)
    transactions_df.to_excel("data/store/transactions.xlsx", index=False)

