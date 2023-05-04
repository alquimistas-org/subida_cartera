import io
from app import app
from dash import Output, Input, State, html, dcc, MATCH, ctx
from src.subida import Preparacion_Cuentas
import base64
from src.adapters.dash_dataframe_saver import DashDataFrameSaver


@app.callback(Output('div-download-NAR-ALTO', 'children'),
              Output('div-download-NAR-MEDIO', 'children'),
              Output('div-download-NAR-BAJO', 'children'),
              Output('stored-dfs', 'data'),
              Input('upload-data-cr', 'contents'))
def upload_csv(list_of_contents):

    if list_of_contents is not None:
        content_type, content_string = list_of_contents.split(',')
        decoded = base64.b64decode(content_string)
        dash_dataframe_saver = DashDataFrameSaver()
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

        return download_buttons[0], download_buttons[1], download_buttons[2], data_dict


@app.callback(
    Output({"type": "download-csv", "id": MATCH}, "data"),
    Input({"type": "btn-download", "id": MATCH}, "n_clicks"),
    Input('stored-dfs', 'data'),
    prevent_initial_call=True,
)
def download_csv(n_clicks, dfs):
    if not n_clicks:
        return
    df_id = ctx.triggered_id["id"]
    df = dfs[df_id]
    return dcc.send_string(df, f"{df_id}.csv")


@app.callback(
    Output("collapse-cr", "is_open"),
    Output("filename-cr", "children"),
    Input("upload-data-cr", "filename"),
    State("collapse-cr", "is_open"),
)
def collapse_upload(filaname, is_open):
    return not is_open, html.Div([
        filaname,
        html.I(className="fa-regular fa-trash-can", id="delete-cr", style={'marginLeft': '1rem'})])
