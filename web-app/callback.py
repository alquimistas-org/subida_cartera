from app import app
from dash import (
    Output,
    Input,
    State,
    html,
    dcc,
    MATCH,
    ctx
)
import base64
from dash.exceptions import PreventUpdate
from src.adapters.dash_dataframe_saver import DashDataFrameSaver
from callbacks_helpers import (
    process_naranja_client,
    process_comafi_client,
    display_modal_error,
)
from components.upload import Upload


@app.callback(Output('div-download', 'children'),
              Output('stored-dfs', 'data'),
              Output('complete-first-step-btn', 'style'),
              Input(Upload.get_upload_id('prepare-accounts'), 'contents'),
              Input('client-store', 'data'),
              prevent_initial_call=True,
              allow_duplicate=True,)
def upload_csv(list_of_contents, client_selected):

    if list_of_contents and client_selected.get('selected_client'):
        content_type, content_string = list_of_contents.split(',')
        decoded = base64.b64decode(content_string)
        dash_dataframe_saver = DashDataFrameSaver()
        download_buttons = []
        data_dict = {}
        if client_selected['selected_client'] == 'Naranja':
            download_buttons, data_dict = process_naranja_client(dash_dataframe_saver, decoded, content_string)

        elif client_selected['selected_client'] == 'Comafi':
            download_buttons, data_dict = process_comafi_client(dash_dataframe_saver, decoded, content_string)

        return download_buttons, data_dict, {'display': 'block'}

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
    Output(Upload.get_collapse_id('prepare-accounts'), "is_open"),
    Output("filename-uploaded-first-step", "children"),
    Output("filename-uploaded-first-step", "style"),
    Input(Upload.get_upload_id('prepare-accounts'), "filename"),
    State(Upload.get_collapse_id('prepare-accounts'), "is_open"),
    Input('client-store', 'data'),
    Input('stored-dfs', 'data'),
)
def collapse_upload(filename, is_open, client_selected, data):
    if filename and client_selected and data:
        return not is_open, html.Div([
            filename,
        ]), {'display': 'block'}
    else:
        raise PreventUpdate


@app.callback(
    Output('client-store', 'data'),
    Input('clients_dropdown', 'value'),
    prevent_initial_call=True,
)
def get_client(client):
    return {'selected_client': client}


@app.callback(
    Output("confirm-modal", "is_open"),
    Input("btn-clear", "n_clicks"),
    Input("cancel-btn", "n_clicks"),
    Input("accept-btn", "n_clicks"),
    State("confirm-modal", "is_open"),
)
def toggle_modal_clear_data(n_clicks_1, n_clicks_2, n_clicks_3, is_open):
    if n_clicks_1 or n_clicks_2 or n_clicks_3:
        return not is_open
    return is_open


@app.callback(
    Output("url", "href"),
    Input("accept-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reload_page(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    return "/"


@app.callback(
              Output('error-client-filename', 'is_open'),
              Output('error-client-filename', 'children'),
              Input(Upload.get_upload_id('prepare-accounts'), 'contents'),
              Input('client-store', 'data'),
              Input(Upload.get_upload_id('prepare-accounts'), "filename"),
              Input("accept-btn-error", "n_clicks"),
              Input('stored-dfs', 'data'),
              State("error-client-filename", "is_open"),
              prevent_initial_call=True,
              suppress_callback_exceptions=True)
def process_modal_error(list_of_contents, client_selected, filename, n_clicks, stored_data, is_open):

    if not list_of_contents and not client_selected:
        raise PreventUpdate

    if ctx.triggered_id == Upload.get_upload_id('prepare-accounts'):
        if not stored_data:
            return display_modal_error(client_selected, filename)
        raise PreventUpdate

    elif ctx.triggered_id == 'accept-btn-error':
        return not is_open, []

    else:
        raise PreventUpdate


@app.callback(Output('icon-success-uploadfirst', 'children'),
              Output('first-step-container', 'style'),
              Input('complete-first-step-btn', 'n_clicks'),
              prevent_initial_call=True,
              allow_duplicate=True,)
def mark_fist_step_as_completed(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    return (
        html.Img(
            src="assets/check-icon.svg",
            height=30,
            style={'marginLeft': '10px', 'marginBottom': '10px'}
        ),
        {'display': 'none'},
        )
