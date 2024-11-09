import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
import os, sys 

# Register the page for the home route
dash.register_page(__name__, path='/products')

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from data.mongodb_.__main__ import (
    get_data, sales_by_selected_year_month_location, get_collection_counts, sales_by_year,
    get_unique_values, sales_by_category, sales_by_location, sales_by_month, sales_by_year_month,get_best_sold_products
)

# Use a dark Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

layout = html.Div([
    # Header
    dbc.Row([
        dbc.Col(html.H1("Product Sales Dashboard", className="text-center text-primary"), width=12),
    ], className="mb-4"),

    # Dropdowns with multi-select
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in sales_by_year()['year'].unique()],
            value=[sales_by_year()['year'].min()],  # Default selected value (can be empty or one)
            clearable=False,
            multi=True,  # Enable multiple selection
            style={'backgroundColor': '#333', 'color': '#fff'}  # Dark background with white text for dropdown
        ), width=4),

        dbc.Col(dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': category, 'value': category} for category in sales_by_category()['category'].unique()],
            value=[sales_by_category()['category'].unique()[0]],  # Default selected value (can be empty or one)
            clearable=False,
            multi=True,  # Enable multiple selection
            style={'backgroundColor': '#333', 'color': '#fff'}  # Dark background with white text for dropdown
        ), width=4),
    ], className='mb-4'),

    # Graphs
    dbc.Row([
        dbc.Col(dcc.Graph(id='sales-by-year', style={'height': '350px', 'backgroundColor': '#333'}), width=6),
        dbc.Col(dcc.Graph(id='sales-by-category', style={'height': '350px', 'backgroundColor': '#333'}), width=6),
    ]),

    # Sales by Location
    dbc.Row([
        dbc.Col(dcc.Graph(id='sales-by-location', style={'height': '350px', 'backgroundColor': '#333'}), width=12),
    ]),

    # New Graphs for top/bottom products and categories
    dbc.Row([
        dbc.Col(dcc.Graph(id='top-products-2023', style={'height': '350px', 'backgroundColor': '#333'}), width=6),
        dbc.Col(dcc.Graph(id='top-categories-2023', style={'height': '350px', 'backgroundColor': '#333'}), width=6),
    ]),
])

# Callbacks to update graphs based on selected inputs
@callback(
    Output('sales-by-year', 'figure'),
    Output('sales-by-category', 'figure'),
    Output('sales-by-location', 'figure'),
    Output('top-products-2023', 'figure'),
    Output('top-categories-2023', 'figure'),
    Input('year-dropdown', 'value'),
    Input('category-dropdown', 'value'),
)
def update_graphs(selected_years, selected_categories):
    # Get sales data
    sales_year = sales_by_year()
    sales_category = sales_by_category()
    sales_location = sales_by_location()

    # Filter data by selected years and categories
    sales_year_filtered = sales_year[sales_year['year'].isin(selected_years)]
    sales_category_filtered = sales_category[sales_category['category'].isin(selected_categories)]
    
    # Create figures for Year, Category, and Location
    fig_year = px.bar(sales_year_filtered, x='year', y='total_sales', title="Sales by Year")
    fig_category = px.bar(sales_category_filtered, x='category', y='total_sales', title="Sales by Category")
    fig_location = px.bar(sales_location, x='city', y='total_sales', title="Sales by Location")
    
    # Fetch top-selling products and categories for 2023/2024
    best_sold_products = get_best_sold_products()
    top_10_products = best_sold_products.head(10)
    least_10_products = best_sold_products.tail(10)

    # Create figure for top 10 products in 2023/2024
    fig_top_products = px.bar(top_10_products, x='product_name', y='total_sales', title="Top 10 Products (2023/2024)")
    
    # Create figure for top 10 categories in 2023/2024
    top_categories = sales_category.groupby('category')['total_sales'].sum().reset_index()
    top_categories = top_categories.sort_values(by='total_sales', ascending=False)
    fig_top_categories = px.bar(top_categories, x='category', y='total_sales', title="Top Categories (2023/2024)")

    # Customize the color for better comparison
    fig_year.update_layout(template="plotly_dark")
    fig_location.update_layout(template="plotly_dark")
    fig_category.update_layout(template="plotly_dark")
    fig_top_products.update_layout(template="plotly_dark")
    fig_top_categories.update_layout(template="plotly_dark")

    # Customize the color for better comparison
    fig_year.update_traces(marker_color='royalblue')
    fig_category.update_traces(marker_color='lightcoral')
    fig_location.update_traces(marker_color='seagreen')
    fig_top_products.update_traces(marker_color='orange')
    fig_top_categories.update_traces(marker_color='yellowgreen')

    return fig_year, fig_category, fig_location, fig_top_products, fig_top_categories



# --------------- 



## Top 10 products saled - no base
## Less 10 Saled Products - no base
## Top 1 by mounth 2023/2024  11-2023 .... 11-2024
## Less 1 by mounth 2023/2024  11-2023 .... 11-2024

## 2023/2024 - The top category product
## 2023/2024 - The less category product

