from dash import html, dcc
import dash_bootstrap_components as dbc
from components.clear_data import ClearData
from components.client_button import ClientButton
from components.upload import Upload
from components.step_title import StepTitle
from components.complete_step_btn import CompleteStepBtn

client_button = ClientButton()
clear_data = ClearData()
first_step_title = StepTitle()
complete_first_step = CompleteStepBtn(input_id='completed-first-step-btn')

app_layout = html.Div([
    html.H1(
        'Osiris',
        style={
            'fontSize': '5rem',
            'fontWeight': '800',
            'marginLeft': '10px',
            'marginTop': '10px'
        }),
    clear_data.create(),
    html.Div([
        html.P("Selecciona un cliente", className="selec-client")
    ]),
    client_button.create(),
    html.Div(id='client-selected-value', style={'display': 'none'}),
    first_step_title.create(title_step="1. Subir archivo para preparación de cuentas"),
    html.Div([
        Upload.create(
            id="cr",
            multiple_files=False,
        ),
        html.Div(
            [
                html.Div([], id="div-download", className="donwload-container")
            ], id="major-div-download", className="major-donwload-container"),
        html.Div([
            complete_first_step.create()
            ], className='completed-step-bnt-container'),
        ],
        id='first-step-container', className='step-container',
    ),
    dcc.Store(id='stored-dfs', clear_data=False, storage_type='memory'),
    dcc.Location(id='url', refresh=True),
    dbc.Modal([
        dbc.ModalFooter(
            [dbc.Button("Aceptar", id="accept-btn-error")],
        ),
    ], id='error-client-filename', is_open=False),
])
