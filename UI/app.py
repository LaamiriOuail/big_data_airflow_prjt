import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import os,sys 

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)



# Initialize the app with external stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], use_pages=True)

# Register pages
import pages.home  # This will register the home page automatically if you structure it correctly
import pages.products
import pages.users
import pages.transactions

# Define the main layout with navigation and content
app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="BeSm",
        brand_href="/",
        color="dark",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Products", href="/products")),
            dbc.NavItem(dbc.NavLink("Users", href="/users")),
            dbc.NavItem(dbc.NavLink("Transactions", href="/transactions")),
        ],
        className="mb-4"
    ),
    dbc.Container(dash.page_container, fluid=True)
])

if __name__ == "__main__":
    app.run_server(debug=False)