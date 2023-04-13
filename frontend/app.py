from dash import Dash, html
import dash_bootstrap_components as dbc
from components import tabs


external_stylesheets = [
    dbc.themes.CERULEAN,
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        tabs.tabs,
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
