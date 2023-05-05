import io
from dash import html, dcc
from pathlib import Path
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

    download_buttons = []

    for key, _ in dfs.items():
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
        dataframe_saver=dash_dataframe_saver,
        accounts_models=Path(f'../{ACCOUNTS_MODEL_CSV_PATH}')
    )

    dfs = dash_dataframe_saver.get_saved_dfs()

    download_buttons = []
    for key, _ in dfs.items():
        download_buttons.append(html.Div([
            html.Div([
                html.P([
                    f"{key}.csv",
                ], className="p-download-csv"),
                html.I(
                    id=key,
                    className="fa-solid fa-circle-down",
                    style={
                        'marginRight': '15px',
                        'marginTop': '0.5rem',
                        'fontSize': '2rem',
                    })
            ], className="container-filename-icon-dwn p-download-csv"),
            dcc.Download(id={"type": "download-csv", "id": key}),
            ],
            className='download-csv-btn',
            id={
                "type": "btn-download",
                "id": key
            }))

    data_dict = {key: value.to_csv() for key, value in dfs.items()}
    data_dict['emerix'] = content_string

    return download_buttons, data_dict
