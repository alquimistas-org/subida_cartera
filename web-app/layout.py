from dash import html
# import dash_bootstrap_components as dbc
from components.tabs import Tabs


tabs = Tabs()

app_layout = html.Div([
    html.H1(
        'Osiris',
        style={
            'fontSize': '5rem',
            'fontWeight': '800',
            'marginLeft': '10px',
            'marginTop': '10px'
        }),
    tabs.create(),
])
