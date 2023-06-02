from dash import html, dcc
import dash_bootstrap_components as dbc

from components.clear_data import ClearData
from components.upload import Upload
from components.step_title import StepTitle
from components.complete_step_btn import CompleteStepBtn
from components.clients_dropdown import ClientsDropdown
from components.external_data_providers_dropdown import ExternalDataProvidersDropDown
from ids import (
    osiris_accounts,
    external_providers,
)

selected_client_style = {
    'background-color': '#1d8ab6',
    'border-color': '#1d8ab6',
    'color': 'white',
}

app_layout = html.Div([
    ClearData.create(),
    html.H1(
        'Osiris',
        style={
            'fontSize': '5rem',
            'fontWeight': '800',
            'marginLeft': '10px',
            'marginTop': '10px'
        }
    ),
    dbc.Tabs(
        [
                dbc.Tab(
                    label="Cartera de Clientes",
                    active_label_style=selected_client_style,
                    children=[
                        html.Div([
                            html.P("Selecciona un cliente", className="selec-client")
                        ]),
                        ClientsDropdown.create(),
                        StepTitle.create(title_step="1. Subir archivo para preparación cuentas", step_id='first'),
                        html.Div(
                            id="filename-uploaded-first-step",
                            style={'display': 'none'},
                            className='filaname-container'
                        ),
                        html.Div([
                            Upload.create(
                                id="prepare-accounts",
                                multiple_files=False,
                                upload_disabled=False,
                            ),
                            html.Div(
                                [
                                    html.Div(id="div-download", className="donwload-container")
                                ],
                                id="major-div-download",
                                className="major-donwload-container"
                            ),
                            html.Div([
                                CompleteStepBtn.create(id='complete-first-step-btn')
                                ],
                                className='completed-step-bnt-container'
                            ),
                        ], id='first-step-container'),
                        dcc.Store(id='stored-dfs', clear_data=False, storage_type='memory'),
                        dcc.Store(
                            id='client-store',
                            data={"selected_client": ClientsDropdown.get_default_client()},
                            clear_data=False,
                            storage_type='memory'
                        ),
                        dcc.Location(id='url', refresh=True),
                        dbc.Modal([
                            dbc.ModalFooter(
                                [dbc.Button("Aceptar", id="accept-btn-error")],
                            ),
                        ], id='error-client-filename', is_open=False),
                        ],
                    tab_id="clients_tabs"
                ),
                dbc.Tab(
                    label="Proveedor de Datos",
                    active_label_style=selected_client_style,
                    children=[
                        ExternalDataProvidersDropDown.create(),
                        dbc.Row([
                            dbc.Col(
                                [
                                    StepTitle.create(title_step="1. Archivo cuentas de osiris"),
                                    Upload().create(
                                        id=osiris_accounts,
                                        multiple_files=False,
                                        upload_disabled=False,
                                    )
                                ]
                            ),
                            dbc.Col(
                                [
                                    StepTitle.create(
                                        title_step="2. Archivo datos del proveedor"),
                                    Upload.create(
                                        id=external_providers,
                                        multiple_files=False,
                                        upload_disabled=False,
                                    ),
                                    ]
                                ),
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
                        dcc.Store(id='store-data-provider', data={}, clear_data=False, storage_type='session')
                    ],
                    id="tab_data_providers",
                    tab_id="tab_data_providers",
                    ),
                ],
        active_tab='clients_tabs',
        ),
    ],
)
