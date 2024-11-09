import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

import os, sys
import pandas as pd
from data.mongodb_.__main__ import get_data_with_transaction_counts

# Register the page for the home route
dash.register_page(__name__, path='/transactions')

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)


# Get the transaction counts data (assuming it's a DataFrame with 'year', 'month', and 'transaction_count' columns)
transaction_counts = get_data_with_transaction_counts()

# Create a bar graph for transactions per year and month
# Group by year and month if needed
transaction_counts['year_month'] = transaction_counts['year'].astype(str) + '-' + transaction_counts['month'].astype(str)
transaction_by_year_month = transaction_counts.groupby('year_month')['transaction_count'].sum().reset_index()
# Group data by Year for the second graph
transaction_by_year = transaction_counts.groupby('year')['transaction_count'].sum().reset_index()

# Dash app layout
layout = html.Div([
    dbc.Row([
        dbc.Col(html.H1("Transaction", className="text-center text-primary"), width=12),
    ], className="mb-4"),
    # Bar graph to display the transaction count by year and month
    dcc.Graph(
            id='transaction-graph',
            figure={
                'data': [
                    {
                        'x': transaction_by_year_month['year_month'],
                        'y': transaction_by_year_month['transaction_count'],
                        'type': 'bar',
                        'name': 'Transactions by Year-Month',
                        'marker': {'color': '#00A4A4'}  # Change bar color
                    },
                ],
                'layout': {
                    'title': "Total Transactions by Year and Month",
                    'title_font': {'color': '#FFFFFF'},  # Title font color
                    'xaxis': {'title': 'Year-Month', 'color': '#FFFFFF'},  # X-axis label color
                    'yaxis': {'title': 'Number of Transactions', 'color': '#FFFFFF'},  # Y-axis label color
                    'plot_bgcolor': '#2C2C2C',  # Background color of the plot area
                    'paper_bgcolor': '#2C2C2C',  # Background color of the entire plot
                    'font': {'color': '#FFFFFF'},  # Font color for labels and ticks
                }
            }
        ),
    # Second Graph: Bar graph for transactions by Year
        dcc.Graph(
            id='transaction-by-year',
            figure={
                'data': [
                    {
                        'x': transaction_by_year['year'],
                        'y': transaction_by_year['transaction_count'],
                        'type': 'bar',
                        'name': 'Transactions by Year',
                        'marker': {'color': '#FF7F50'}  # Change bar color to another shade
                    },
                ],
                'layout': {
                    'title': "Total Transactions by Year",
                    'title_font': {'color': '#FFFFFF'},  # Title font color
                    'xaxis': {'title': 'Year', 'color': '#FFFFFF'},  # X-axis label color
                    'yaxis': {'title': 'Number of Transactions', 'color': '#FFFFFF'},  # Y-axis label color
                    'plot_bgcolor': '#2C2C2C',  # Background color of the plot area
                    'paper_bgcolor': '#2C2C2C',  # Background color of the entire plot
                    'font': {'color': '#FFFFFF'},  # Font color for labels and ticks
                }
            }
        ),
])


