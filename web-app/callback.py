from app import app
from dash import Output, Input, State, html, dcc, MATCH, ctx
import base64
from dash.exceptions import PreventUpdate
from src.adapters.dash_dataframe_saver import DashDataFrameSaver
from callbacks_helpers import (
    process_naranja_client,
    process_comafi_client,
    display_modal_error,
)


@app.callback(Output('div-download', 'children'),
              Output('stored-dfs', 'data'),
              Input('upload-data-cr', 'contents'),
              Input('client-selected-value', 'children'),
              Input("upload-data-cr", "filename"),
              prevent_initial_call=True,
              allow_duplicate=True,)
def upload_csv(list_of_contents, client_selected, filename):

    if list_of_contents and client_selected:
        if (
            (client_selected == 'naranja' and 'cr' not in filename)
            or (client_selected == 'comafi' and 'emerix' not in filename)
        ):
            raise PreventUpdate

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
    Input('client-selected-value', 'children'),
)
def collapse_upload(filename, is_open, client_selected):
    if filename and client_selected:
        if (
            (client_selected == 'naranja' and 'cr' in filename)
            or (client_selected == 'comafi' and 'emerix' in filename)
        ):
            return not is_open, html.Div([
                filename,
                html.I(className="fa-regular fa-trash-can", id="delete-cr", style={'marginLeft': '1rem'})])
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


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


@app.callback(
              Output('error-client-filename', 'is_open'),
              Output('error-client-filename', 'children'),
              Input('upload-data-cr', 'contents'),
              Input('client-selected-value', 'children'),
              Input("upload-data-cr", "filename"),
              Input("accept-btn-error", "n_clicks"),
              State("error-client-filename", "is_open"),
              prevent_initial_call=True,
              suppress_callback_exceptions=True)
def process_modal_error(list_of_contents, client_selected, filename, n_clicks, is_open):

    if not list_of_contents and not client_selected:
        raise PreventUpdate

    if ctx.triggered_id == 'upload-data-cr':
        if list_of_contents and client_selected:
            return display_modal_error(client_selected, filename)
        raise PreventUpdate

    elif ctx.triggered_id == 'accept-btn-error':
        return not is_open, []

    else:
        raise PreventUpdate
