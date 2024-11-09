import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H2("Transactions Page"),
    html.P("This is the Transactions page.")
])


# --------------- 

## 2024-2023 mounth number/amount of transactions by mounth
## 2024-2023 mounth number/amount of transactions by year