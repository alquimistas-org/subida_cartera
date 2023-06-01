from dash import html, dcc
import dash_bootstrap_components as dbc

from components.clear_data import ClearData
from components.client_button import ClientButton
from components.upload import Upload
from components.step_title import StepTitle
from components.complete_step_btn import CompleteStepBtn
from components.external_data_providers_dropdown import ExternalDataProvidersDropDown
from ids import (
    osiris_accounts,
    external_providers,
)


client_button = ClientButton()
clear_data = ClearData()
first_step_title = StepTitle()
complete_first_step = CompleteStepBtn(input_id='completed-first-step-btn')
selected_client_style = {
    'background-color': '#1d8ab6',
    'border-color': '#1d8ab6',
    'color': 'white',
}

app_layout = html.Div([
    html.H1(
        'Osiris',
        style={
            'fontSize': '5rem',
            'fontWeight': '800',
            'marginLeft': '10px',
            'marginTop': '10px'
        }),
    dbc.Tabs(
        [
            dbc.Tab(
                label="Cartera de Clientes",
                active_label_style=selected_client_style,
                children=[
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
                ],
                id="tab_clientes",
                tab_id="tab_clientes",
            ),
            dbc.Tab(
                label="Proveedor de Datos",
                active_label_style=selected_client_style,
                children=[

                    ExternalDataProvidersDropDown.create(),

                    dbc.Row([
                        dbc.Col([
                            "1. Archivo cuentas de osiris",
                            Upload.create(
                                id=osiris_accounts,
                                multiple_files=False,
                                upload_disabled=False,
                            ),
                        ]),
                        dbc.Col([
                            "2. Archivo datos del proveedor",
                            Upload.create(
                                id=external_providers,
                                multiple_files=False,
                                upload_disabled=False,
                            ),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col(
                            dbc.Button("Preparar datos", id="prepare_data_provider_button", color="primary"),
                        )
                    ]),
                    dbc.Row([
                        dbc.Col(
                            'Resultado',
                            id='result_prepare_data_provider',
                        ),
                    ]),
                    dcc.Store(id='store-data-provider', data={}, clear_data=False, storage_type='session'),
                ],
                id="tab_data_providers",
                tab_id="tab_data_providers",
            ),
        ],
        active_tab='tab_data_providers',

    )

])
