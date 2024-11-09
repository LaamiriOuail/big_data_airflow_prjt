import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H2("Users Page"),
    html.P("This is the Users page.")
])



## Number user by City : Bar/Circle
## The largest number of transaction by user
## The least number of transaction by user