from app import app
from dash import Output, Input, State, html, dcc, MATCH, ctx
import base64
from dash.exceptions import PreventUpdate
from src.adapters.dash_dataframe_saver import DashDataFrameSaver
from callbacks_helpers import process_naranja_client, process_comafi_client


@app.callback(Output('div-download', 'children'),
              Output('stored-dfs', 'data'),
              Input('upload-data-cr', 'contents'),
              Input('client-selected-value', 'children'),
              prevent_initial_call=True,
              allow_duplicate=True,)
def upload_csv(list_of_contents, client_selected):

    if list_of_contents and client_selected:
        content_type, content_string = list_of_contents.split(',')
        decoded = base64.b64decode(content_string)
        dash_dataframe_saver = DashDataFrameSaver()

        if client_selected == 'naranja':
            download_buttons, data_dict = process_naranja_client(dash_dataframe_saver, decoded, content_string)

        elif client_selected == 'comafi':
            download_buttons, data_dict = process_comafi_client(dash_dataframe_saver, decoded, content_string)

        return download_buttons, data_dict

    else:
        raise PreventUpdate


@app.callback(
    Output({"type": "download-csv", "id": MATCH}, "data"),
    Input({"type": "btn-download", "id": MATCH}, "n_clicks"),
    Input('stored-dfs', 'data'),
    prevent_initial_call=True,
    allow_duplicate=True,
)
def download_csv(n_clicks, dfs):
    if not n_clicks:
        raise PreventUpdate
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


@app.callback(
    Output('client-selected-value', 'children'),
    Output('naranja', 'style'),
    Output('comafi', 'style'),
    Input('naranja', 'n_clicks'),
    Input('comafi', 'n_clicks'),
    prevent_initial_call=True,
)
def get_client(btn_1, btn_2):
    client_id = ctx.triggered_id

    white_button_style = {
        'background-color': 'white'
    }

    red_button_style = {
        'background-color': '#1d8ab6',
        'border-color': '#1d8ab6',
        'color': 'white',
     }

    if client_id == 'naranja':
        style_naranja = red_button_style
        style_comafi = white_button_style
    elif client_id == 'comafi':
        style_comafi = red_button_style
        style_naranja = white_button_style

    return client_id, style_naranja, style_comafi
