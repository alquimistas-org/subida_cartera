from dash import html, dcc
import dash_bootstrap_components as dbc
from components.client_button import ClientButton
from components.upload import Upload


client_button = ClientButton()
upload = Upload()

app_layout = html.Div([
    html.H1(
        'Osiris',
        style={
            'fontSize': '5rem',
            'fontWeight': '800',
            'marginLeft': '10px',
            'marginTop': '10px'
        }),
    client_button.create(),
    html.Div(id='client-selected-value', style={'display': 'none'}),
    upload.create("1. Subir archivo para preparación de cuentas", id="cr", multiple_files=False),
    html.Div([
                html.Div([], id="div-download", className="donwload-container")
            ], id="major-div-download", className="major-donwload-container"),
    dcc.Store(id='stored-dfs'),
    dbc.Modal([
        dbc.ModalFooter(
            [dbc.Button("Aceptar", id="accept-btn-error")],
        ),
    ], id='error-client-filename', is_open=False)
])
