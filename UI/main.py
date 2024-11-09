import streamlit as st
import os
import sys
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd



# Configuration de la page
st.set_page_config(page_title="Dashboard - Analyse des Données", layout="wide")

# Import des fonctions MongoDB
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(parent_dir)

from data.mongodb_.__main__ import (
    get_data, sales_by_selected_year_month_location, get_collection_counts, sales_by_year,
    get_unique_values, sales_by_category, sales_by_location, sales_by_month, sales_by_year_month
)

# Fonction pour compter les utilisateurs, produits et transactions
def count_columns(st=st):
    counts = get_collection_counts()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Users")
        user_metric = st.empty()
    with col2:
        st.subheader("Products")
        product_metric = st.empty()
    with col3:
        st.subheader("Transactions")
        transaction_metric = st.empty()

    user_count = counts['user_count']
    product_count = counts['product_count']
    transaction_count = counts['transaction_count']
    transactions_added_this_month = counts['transactions_added_this_month']

    user_metric.metric(label="Total Users", value=user_count)
    product_metric.metric(label="Total Products", value=product_count)
    transaction_metric.metric(label="Total Transactions", value=transaction_count, delta=transactions_added_this_month)

# Visualisation 1 : Top 10 des Produits les Plus Vendus
def top_10_products():
    st.write("## Top 10 des Produits les Plus Vendus")
    transactions = get_data('transactions')  # Récupère les transactions
    products = get_data('products')  # Récupère les produits

    transactions_df = pd.DataFrame(transactions)
    products_df = pd.DataFrame(products)

    transactions_df['quantity'] = transactions_df['amount'] / transactions_df['product_id'].map(
        products_df.set_index('product_id')['price'])

    top_products = transactions_df.groupby('product_id')['quantity'].sum().nlargest(10)
    top_products_df = products_df[products_df['product_id'].isin(top_products.index)]

    # Ajout de la colonne 'quantity_sold' et 'product_name' dans le DataFrame des produits
    top_products_df['quantity_sold'] = top_products.loc[top_products_df['product_id']].values
    top_products_df = top_products_df[['product_id', 'product_name', 'quantity_sold']]  # Assurez-vous que 'product_name' est inclus

    # Création du graphique
    fig = px.bar(top_products_df, x='product_name', y='quantity_sold', title="Top 10 Produits les Plus Vendus")
    st.plotly_chart(fig)


# Visualisation 2 : Produits les Moins Vendus
def bottom_10_products():
    st.write("## Produits les Moins Vendus")
    transactions = get_data('transactions')  # Récupère les transactions
    products = get_data('products')  # Récupère les produits

    transactions_df = pd.DataFrame(transactions)
    products_df = pd.DataFrame(products)

    transactions_df['quantity'] = transactions_df['amount'] / transactions_df['product_id'].map(
        products_df.set_index('product_id')['price'])

    bottom_products = transactions_df.groupby('product_id')['quantity'].sum().nsmallest(10)
    bottom_products_df = products_df[products_df['product_id'].isin(bottom_products.index)]
    bottom_products_df['quantity_sold'] = bottom_products.loc[bottom_products_df['product_id']].values

    fig = px.bar(bottom_products_df, x='product_name', y='quantity_sold', title="Top 10 Produits les Moins Vendus")
    st.plotly_chart(fig)

# Visualisation 3 : Répartition des Transactions par Utilisateur

def transactions_by_user():
    st.write("## Montant Total des Transactions par Utilisateur")
    transactions = get_data('transactions')  # Récupère les transactions
    users = get_data('users')  # Récupère les utilisateurs

    transactions_df = pd.DataFrame(transactions)
    users_df = pd.DataFrame(users)

    transactions_by_user = transactions_df.groupby('user_id')['amount'].sum().nlargest(10)

    if 'user_id' in users_df.columns:
        top_users = users_df[users_df['user_id'].isin(transactions_by_user.index)]

        # Vérification des colonnes disponibles dans users_df
        print(top_users.columns)  # Cela vous aidera à identifier la colonne correcte pour le nom

        # Utilisez la bonne colonne pour les noms des utilisateurs (par exemple, 'user_name' ou autre)
        fig = px.bar(top_users, x='name', y=transactions_by_user[top_users['user_id']],  # Changez 'user_name' si nécessaire
                     title="Montant Total des Transactions par Utilisateur")
        st.plotly_chart(fig)
    else:
        st.write("La colonne 'user_id' n'existe pas dans le DataFrame 'users'.")


# Visualisation 4 : Répartition des Utilisateurs par Ville
def users_by_city():
    st.write("## Répartition des Utilisateurs par Pays")
    users = get_data('users')  # Récupère les utilisateurs
    users_df = pd.DataFrame(users)

    users_by_city = users_df['city'].value_counts()
    fig = px.pie(values=users_by_city, names=users_by_city.index, title="Répartition des Utilisateurs par Ville")
    st.plotly_chart(fig)

# Visualisation 5 : Total des Ventes par Année
def plot_sales_by_year():
    st.write("##Ventes Totales par Année")
    sales = sales_by_year()  # Récupère les données des ventes par année
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(sales['year'].astype(int), sales['total_sales'], color='skyblue')
    ax.set_title("Total Sales by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Sales")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# Organisation de la page
if __name__ == "__main__":
    st.title("Dashboard d'Analyse des Données")

    # Afficher les métriques
    count_columns()

    # Sélection des visualisations
    st.sidebar.markdown("## Sélectionnez une Visualisation")
    options = ["Top 10 Produits les Plus Vendus", "Top 10 Produits les Moins Vendus",
               "Transactions par Utilisateur", "Répartition des Utilisateurs par Ville", 
               "Ventes Totales par Année"]

    choice = st.sidebar.selectbox("Choisissez une visualisation :", options)

    if choice == "Top 10 Produits les Plus Vendus":
        top_10_products()
    elif choice == "Top 10 Produits les Moins Vendus":
        bottom_10_products()
    elif choice == "Transactions par Utilisateur":
        transactions_by_user()
    elif choice == "Répartition des Utilisateurs par Ville":
        users_by_city()
    elif choice == "Ventes Totales par Année":
        plot_sales_by_year()

    st.sidebar.info("Développé pour le mini-projet d'analyse des données 🚀")

