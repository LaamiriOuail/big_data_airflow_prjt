import dash
from dash import html, dcc , callback
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
import os, sys 

# Register the page for the home route
dash.register_page(__name__, path='/')

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from data.mongodb_.__main__ import (
    get_data, sales_by_selected_year_month_location, get_collection_counts, sales_by_year,
    get_unique_values, sales_by_category, sales_by_location, sales_by_month, sales_by_year_month
)



# Define the layout
layout = html.Div([
    dbc.Container([
        # Metrics Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Users"),
                    dbc.CardBody(html.H5(id="user-count", className="card-title", style={'fontSize': '1.5em', 'textAlign': 'center'})),
                ], color="primary", inverse=True)
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Products"),
                    dbc.CardBody(html.H5(id="product-count", className="card-title", style={'fontSize': '1.5em', 'textAlign': 'center'})),
                ], color="success", inverse=True)
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Transactions"),
                    dbc.CardBody(html.H5(id="transaction-count", className="card-title", style={'fontSize': '1.5em', 'textAlign': 'center'})),
                ], color="info", inverse=True)
            ], width=3),
        ], className="mb-4"),

        # Graphs Section
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="sales-by-year-graph", style={'height': '250px'}),
                dcc.Graph(id="sales-by-month-graph", style={'height': '250px'}),
            ], width=6),
            dbc.Col([
                dcc.Graph(id="sales-by-category-graph", style={'height': '250px'}),
                dcc.Graph(id="sales-by-location-graph", style={'height': '250px'}),
            ], width=6)
        ], className="mb-4"),

        # Sales by Year-Month Graph
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="sales-by-year-month-graph", style={'height': '350px'})
            ])
        ]),

        # Interval component to trigger updates every 5 seconds
        dcc.Interval(id="interval-component", interval=5 * 1000, n_intervals=0)
    ], fluid=True)
])

# Callbacks for updating the metrics
@callback(
    [Output("user-count", "children"),
     Output("product-count", "children"),
     Output("transaction-count", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_metrics(_):
    counts = get_collection_counts()
    transaction_text = f"{counts['transaction_count']} (+{counts['transactions_added_this_month']})" \
        if counts['transactions_added_this_month'] > 0 else f"{counts['transaction_count']}"

    return (
        counts['user_count'],
        counts['product_count'],
        transaction_text
    )

# Callback for sales by year graph
@callback(
    Output("sales-by-year-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_sales_by_year(_):
    data = sales_by_year()
    fig = px.bar(data, x='year', y='total_sales', title="Total Sales by Year", color_discrete_sequence=['#3498db'])
    fig.update_layout(template="plotly_dark")
    return fig

# Callback for sales by month graph
@callback(
    Output("sales-by-month-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_sales_by_month(_):
    data = sales_by_month()
    fig = px.line(data, x='month', y='total_sales', title="Total Sales by Month", markers=True, color_discrete_sequence=['#e74c3c'])
    fig.update_layout(template="plotly_dark")
    return fig

# Callback for sales by category graph
@callback(
    Output("sales-by-category-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_sales_by_category(_):
    data = sales_by_category()
    fig = px.pie(data, names='category', values='total_sales', title="Sales by Product Category", color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(template="plotly_dark")
    return fig

# Callback for sales by location graph
@callback(
    Output("sales-by-location-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_sales_by_location(_):
    data = sales_by_location()
    fig = px.bar(data, x='city', y='total_sales', title="Sales by Location (City)", color_discrete_sequence=['#2ecc71'])
    fig.update_layout(template="plotly_dark", xaxis_tickangle=45)
    return fig

# Callback for sales by year and month graph
@callback(
    Output("sales-by-year-month-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_sales_by_year_month(_):
    data = sales_by_year_month()
    fig = px.scatter(data, x='month', y='total_sales', color='year', title="Sales by Year-Month", size='total_sales',
                     color_continuous_scale='Viridis', labels={"month": "Month", "total_sales": "Total Sales", "year": "Year"})
    fig.update_layout(template="plotly_dark")
    return fig
