from dash import html, dcc
import dash_bootstrap_components as dbc

from components import (
    ClearData,
    ClientsDropdown,
    CompleteStepBtn,
    DownloadButtonsArea,
    ExternalDataProvidersDropDown,
    FilenameUploaded,
    StepTitle,
    Upload,
)
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
        'Uploader',
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
                    html.Div(
                        [
                            html.P("Selecciona un cliente", className="selec-client")
                            ]
                        ),
                    ClientsDropdown.create(),
                    html.Div(
                        id='preparacion-cuentas',
                        style={'display': 'none'},
                        children=[
                            StepTitle.create(
                                title_step="1. Subir archivo para preparación cuentas",
                                step_id='client-first',
                                ),
                            html.Div(
                                id="filename-uploaded-first-step",
                                style={'display': 'none'},
                                className='filaname-container'
                            ),
                            FilenameUploaded.create('client-first-step'),
                            html.Div(
                                [
                                    Upload.create(
                                        id="prepare-accounts",
                                        multiple_files=False,
                                        upload_disabled=False,
                                    ),
                                    DownloadButtonsArea.create("prepare"),
                                    CompleteStepBtn.create(id='client-first'),
                                    ],
                                id='first-step-container'),
                            dcc.Store(id='exception-storage', data={}, clear_data=False, storage_type='session'),
                            dbc.Modal(
                                [
                                    dbc.ModalFooter(
                                        [
                                            dbc.Button("Aceptar", id="accept-btn-error")
                                            ],
                                    ),
                                ],
                                id='error-client-filename', is_open=False),
                        ],
                    ),
                    html.Div(
                        id='preparacion-datos',
                        style={'display': 'none'},
                        children=[
                            StepTitle.create(title_step="2. Subir archivo para preparación datos", step_id='second'),
                            html.Div(
                                id="filename-uploaded-second-step",
                                style={'display': 'none'},
                                className='filaname-container'
                            ),
                            html.Div([
                                Upload.create(
                                    id="prepare-data",
                                    multiple_files=False,
                                    upload_disabled=False,
                                ),
                                DownloadButtonsArea.create("prepare-data-btn"),
                            ], id='second-step-container'),
                        ]
                    ),
                    dcc.Store(
                        id='stored-dfs',
                        clear_data=False,
                        storage_type='memory'),
                    dcc.Store(
                        id='client-store',
                        data={"selected_client": ClientsDropdown.get_default_client()},
                        clear_data=False,
                        storage_type='memory'
                    ),
                    dcc.Store(
                        id='data-store',
                        clear_data=False,
                        storage_type='memory'
                    ),
                    dcc.Store(
                        id='data-client-store',
                        data={"selected_client": ClientsDropdown.get_default_client() + '_data'},
                        clear_data=False,
                        storage_type='memory'
                    ),
                    dcc.Location(id='url', refresh=True),
                    dbc.Modal([
                        dbc.ModalFooter(
                            # FIXME repeated id so i have to add datos, but it's not a good solution
                            [dbc.Button("Aceptar", id="accept-btn-error-datos")],
                        ),
                    # FIXME repeated id so i have to add datos, but it's not a good solution
                    ], id='error-client-filename-datos', is_open=False),
                ],
                tab_id="clients_tabs"
                ),
            dbc.Tab(
                label="Proveedor de Datos",
                active_label_style=selected_client_style,
                children=[
                    html.Div([
                        html.P("Selecciona un proveedor", className="selec-client")
                    ]),
                    ExternalDataProvidersDropDown.create(),
                    html.Div(
                        id='external-provider-div',
                        style={'display': 'none'},
                        children=[
                            dbc.Row([
                                dbc.Col(
                                    [
                                        StepTitle.create(
                                            title_step="1. Archivo cuentas de osiris",
                                            step_id='external-data-provider',
                                        ),
                                        Upload.create(
                                            id=osiris_accounts,
                                            multiple_files=False,
                                            upload_disabled=False,
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        StepTitle.create(
                                            title_step="2. Archivo datos del proveedor", step_id='osiris-accounts'),
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
                            DownloadButtonsArea.create("prepare-external-data-provider"),
                            dcc.Store(id='store-data-provider', data={}, clear_data=False, storage_type='session'),
                        ]
                        ),

                ],
                id="tab_data_providers",
                tab_id="tab_data_providers",
                ),
            ],
        active_tab='clients_tabs',
            ),
    ],
)
