import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H2("Transactions Page"),
    html.P("This is the Transactions page.")
])
