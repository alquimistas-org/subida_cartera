import dash
import dash_bootstrap_components as dbc
import os


assets_path = os.getcwd() + '/assets'
external_stylesheets = [
    dbc.themes.MATERIA,
    dbc.icons.FONT_AWESOME,
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    prevent_initial_callbacks=True,
    assets_folder=assets_path,
)

app.title = "Cuervo Abogados"
