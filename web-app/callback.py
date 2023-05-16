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
        filaname
    ])


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

    not_selected_button_style = {
        'background-color': 'white'
    }

    selected_client_style = {
        'background-color': '#1d8ab6',
        'border-color': '#1d8ab6',
        'color': 'white',
     }

    if client_id == 'naranja':
        style_naranja = selected_client_style
        style_comafi = not_selected_button_style
    elif client_id == 'comafi':
        style_comafi = selected_client_style
        style_naranja = not_selected_button_style

    return client_id, style_naranja, style_comafi


@app.callback(
    Output("confirm-modal", "is_open"),
    Input("btn-clear", "n_clicks"),
    Input("cancel-btn", "n_clicks"),
    Input("accept-btn", "n_clicks"),
    State("confirm-modal", "is_open"),
)
def toggle_modal(n_clicks_1, n_clicks_2, n_clicks_3, is_open):
    if n_clicks_1 or n_clicks_2 or n_clicks_3:
        return not is_open
    return is_open


@app.callback(
    Output("url", "href"),
    Input("accept-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reload_page(n_clicks):
    return "/"
