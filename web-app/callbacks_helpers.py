import io
from dash import html, dcc
from src.subida import Preparacion_Cuentas
from src.prepare_comafi_accounts import prepare_comafi_accounts
from src.adapters.dash_dataframe_saver import DashDataFrameSaver


def process_naranja_client(dash_dataframe_saver: DashDataFrameSaver, decoded, content_string):
    Preparacion_Cuentas(
            cr_file_path=io.BytesIO(decoded),
            dataframe_saver=dash_dataframe_saver
        )

    dfs = dash_dataframe_saver.get_saved_dfs()

    download_buttons = []

    for key, value in dfs.items():
        download_buttons.append(html.Div([
            html.Button([
                html.I(className="fa-solid fa-circle-down", style={'marginRight': '10px'}),
                f"Descargar {key}"
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
        dataframe_saver=dash_dataframe_saver
    )

    dfs = dash_dataframe_saver.get_saved_dfs()

    download_buttons = []

    for key, value in dfs.items():
        download_buttons.append(html.Div([
            html.Button([
                html.I(className="fa-solid fa-circle-down", style={'marginRight': '10px'}),
                f"Descargar {key}"
            ], id={
                "type": "btn-download",
                "id": key
            }, className="download-button"),
            dcc.Download(id={"type": "download-csv", "id": key})
        ]))

    data_dict = {key: value.to_csv() for key, value in dfs.items()}
    data_dict['emerix'] = content_string

    return download_buttons, data_dict
