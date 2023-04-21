from dash import html
# import dash_bootstrap_components as dbc
from components.tabs import Tabs

tabs = Tabs()

app_layout = html.Div([
    tabs.createTabs(),
])
