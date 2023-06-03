import io
from dash import html, dcc
from pathlib import Path
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from src.subida import Preparacion_Cuentas
from src.prepare_comafi_accounts import prepare_comafi_accounts
from src.adapters.dash_dataframe_saver import DashDataFrameSaver
from src.constants.constants import ACCOUNTS_MODEL_CSV_PATH


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
                "type": "btn-download",
                "id": key
            }, className="download-button"),
            dcc.Download(id={"type": "download-csv", "id": key})
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
                "type": "btn-download",
                "id": key
            }, className="download-button"),
            dcc.Download(id={"type": "download-csv", "id": key})
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
