import io
from pathlib import Path
from typing import List, Tuple

from dash import (
    ctx,
    dcc,
    html,
)
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from components.download_button import DownloadButton
from src.adapters.dash_dataframe_saver import DashDataFrameSaver
from src.constants.constants import ACCOUNTS_MODEL_CSV_PATH
from src.data_info import GenerateDataInfo
from src.prepare_comafi_accounts import prepare_comafi_accounts
from src.risk_data import risk_data
from src.subida import Preparacion_Cuentas
from web_constants import (
    COMAFI,
    NARANJA,
    )


def process_naranja_client(dash_dataframe_saver: DashDataFrameSaver, decoded, content_string):
    Preparacion_Cuentas(
            cr_file_path=io.BytesIO(decoded),
            dataframe_saver=dash_dataframe_saver
        )

    dfs = dash_dataframe_saver.get_saved_dfs()

    if not dfs:
        raise PreventUpdate

    download_buttons = []
    for key, _ in dfs.items():
        download_buttons.append(html.Div([
            html.Button([
                html.P(f"{key}.csv", style={'textTransform': 'lowercase', 'marginLeft': '1rem'}),
                html.I(
                    className="fa-solid fa-circle-down",
                    style={'marginRight': '0.5rem', 'fontSize': 'large', 'marginTop': '1rem'}
                ),
            ], id={
                "type": "btn-download-accounts",
                "id": key
            }, className="download-button"),
            dcc.Download(id={"type": "download-csv-accounts", "id": key})
        ]))

    data_dict = {key: value.to_csv() for key, value in dfs.items()}
    data_dict['cr'] = content_string

    return download_buttons, data_dict


def process_comafi_client(dash_dataframe_saver: DashDataFrameSaver, decoded, content_string):

    prepare_comafi_accounts(
        emerix_file_path=io.BytesIO(decoded),
        dataframe_saver=dash_dataframe_saver,
        accounts_models=Path(f'../{ACCOUNTS_MODEL_CSV_PATH}')
    )

    dfs = dash_dataframe_saver.get_saved_dfs()

    if not dfs:
        raise PreventUpdate

    download_buttons = []
    for key, _ in dfs.items():
        download_buttons.append(html.Div([
            html.Button([
                html.P(f"{key}.csv", style={'textTransform': 'lowercase', 'marginLeft': '1rem'}),
                html.I(
                    className="fa-solid fa-circle-down",
                    style={'marginRight': '0.5rem', 'fontSize': 'large', 'marginTop': '1rem'}
                ),
            ], id={
                "type": "btn-download-accounts",
                "id": key
            }, className="download-button"),
            dcc.Download(id={"type": "download-csv-accounts", "id": key})
        ]))

    data_dict = {key: value.to_csv() for key, value in dfs.items()}
    data_dict['emerix'] = content_string

    return download_buttons, data_dict


def display_modal_error(client_selected, filename):

    modal_header = dbc.ModalHeader([
        html.I(
            className="fa-solid fa-circle-exclamation",
            style={"color": "#f30010", "marginRight": "0.5rem"}
        ),
        html.Span("Error", style={"fontWeight": 400, "fontSize": "large"}),
    ])
    modal_body = dbc.ModalBody(
        [
            html.Span("No es posible procesar el archivo "),
            html.Span(filename, id="filename-error"),
            html.Span(f" para {client_selected['selected_client']}"),
        ],
        style={'fontSize': 'large', 'fontWeight': 400})
    modal_footer = dbc.ModalFooter(
        [dbc.Button("Aceptar", id="accept-btn-error")],
    )
    return True, [modal_header, modal_body, modal_footer]


def get_id_and_value_from_context():
    if not ctx.triggered:
        raise PreventUpdate
    triggered_id = ctx.triggered_id
    triggered_input_value = ctx.triggered[0]['value']
    triggered_state_value = [value for key, value in ctx.states.items() if triggered_id.get('id') in key][0]
    return triggered_id, triggered_input_value, triggered_state_value


def process_external_provider_data(
    dash_dataframe_saver: DashDataFrameSaver,
    osiris_accounts_data: dict,
    external_provider_data: dict,
    external_provider_name: str,
) -> Tuple[List[DownloadButton], dict]:
    if external_provider_name == 'riesgo-online':
        risk_data(
            risk_file_path=external_provider_data,
            osiris_accounts_file_path=osiris_accounts_data,
            dataframe_saver=dash_dataframe_saver
        )
    else:
        GenerateDataInfo.process(
            osiris_accounts_data=osiris_accounts_data,
            external_provider_data=external_provider_data,
            dataframe_saver=dash_dataframe_saver
        )

    dfs = dash_dataframe_saver.get_saved_dfs()

    if not dfs:
        raise PreventUpdate

    download_buttons = [
        DownloadButton.create(df_name)
        for df_name in dfs.keys()
    ]

    result_data = {df_name: df.to_csv(index=False) for df_name, df in dfs.items()}

    return download_buttons, result_data


CLIENT_STRATEGY = {
    COMAFI: process_comafi_client,
    NARANJA: process_naranja_client,
}


def process_client(strategy, dash_dataframe_saver: DashDataFrameSaver, decoded, content_string):
    return CLIENT_STRATEGY[strategy](dash_dataframe_saver, decoded, content_string)
