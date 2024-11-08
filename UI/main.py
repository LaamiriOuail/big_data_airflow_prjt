import streamlit as st 
import os
import sys
import time
import matplotlib.pyplot as plt

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from data.mongodb_.__main__ import (
    get_data, sales_by_selected_year_month_location,get_collection_counts,sales_by_year,get_unique_values,
    sales_by_category,sales_by_location,sales_by_month,sales_by_year_month
)

def count_columns(st=st):
    # Get the counts and the items added this month from MongoDB
    counts = get_collection_counts()

    # Layout with columns for cards
    col1, col2, col3 = st.columns(3)

    # Create placeholders
    with col1:
        st.subheader("Users")
        user_metric = st.empty()  # Create a placeholder for the metric

    with col2:
        st.subheader("Products")
        product_metric = st.empty()  # Create a placeholder for the metric

    with col3:
        st.subheader("Transactions")
        transaction_metric = st.empty()  # Create a placeholder for the metric

    # Get the count values for each metric
    user_count = counts['user_count']
    product_count = counts['product_count']
    transaction_count = counts['transaction_count']
    transactions_added_this_month = counts['transactions_added_this_month']
    transaction_metric.metric(label="Total Transactions", value=transaction_count, delta=transactions_added_this_month)
    product_metric.metric(label="Total Products", value=product_count)
    user_metric.metric(label="Total Users", value=user_count)


# Function to plot sales by year
def plot_sales_by_year():
    sales = sales_by_year()
    
    # Create a figure for the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotting the sales by year
    ax.bar(sales['year'].astype(int), sales['total_sales'], color='skyblue')

    # Adding titles and labels
    ax.set_title("Total Sales by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Sales")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Render the plot in Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    count_columns()
    # Plot the sales by year graph
    plot_sales_by_year()