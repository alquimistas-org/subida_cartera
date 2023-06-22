import io


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
    display_modal_error,
    get_id_and_value_from_context,
    process_external_provider_data,
    process_client,
)
from components import (
    CompleteStepBtn,
    DownloadButtonsArea,
    FilenameUploaded,
    StepTitle,
    Upload,
    )
from ids import (
    external_providers,
    osiris_accounts,
)
from web_constants import (
    NARANJA_DATA,
    )


@app.callback(Output('preparacion-cuentas', 'style'),
              Input('client-store', 'data'),)
def show_first_step_accounts(selected_client):
    client = selected_client.get('selected_client')
    return {'display': 'none'} if client == '-' else {'display': 'block'}


@app.callback(Output('external-provider-div', 'style'),
              Input('external_data_providers_dropdown', 'value'),)
def show_data_provider_processor(selected_provider):
    return {'display': 'none'} if selected_provider == '-' else {'display': 'block'}


@app.callback(
    Output(DownloadButtonsArea.get_id("prepare"), 'children'),
    Output('stored-dfs', 'data'),
    Output(CompleteStepBtn.get_btn_id('client-first'), 'style'),
    Output('exception-storage', 'data'),
    Input(Upload.get_upload_id('prepare-accounts'), 'contents'),
    Input('client-store', 'data'),
    prevent_initial_call=True,
    allow_duplicate=True,
)
def upload_csv(list_of_contents, client_selected):

    if list_of_contents and client_selected.get('selected_client'):
        content_type, content_string = list_of_contents.split(',')
        decoded = base64.b64decode(content_string)
        dash_dataframe_saver = DashDataFrameSaver()
        download_buttons = []
        data_dict = {}

        download_buttons, data_dict, message = process_client(
            client_selected['selected_client'],
            dash_dataframe_saver=dash_dataframe_saver,
            cr_decoded=decoded,
            cr_content_string=content_string,
            )

        if message:
            return None, None, None, message

        return download_buttons, data_dict, {'display': 'block', 'textTransform': 'lowercase'}, None

    else:
        raise PreventUpdate


@app.callback(Output(DownloadButtonsArea.get_id("prepare-data-btn"), 'children'),
              Output('data-store', 'data'),
              Input('data-client-store', 'data'),
              Input('stored-dfs', 'data'),
              Input(Upload.get_upload_id('prepare-data'), 'contents'),
              prevent_initial_call=True,
              allow_duplicate=True,
              )
def upload_data_csv(
    client_selected,
    store_dfs_data,
    list_of_contents,
                    ):

    if list_of_contents:

        client = client_selected.get('selected_client')

        stored_cr = store_dfs_data.get('cr') if client == NARANJA_DATA else store_dfs_data.get('emerix')
        decoded_stored_cr = base64.b64decode(stored_cr)

        data_content_string = list_of_contents.split(',')[-1]
        decoded_data_content_string = base64.b64decode(data_content_string)

        dash_dataframe_saver = DashDataFrameSaver()

        download_buttons = []
        data_dict = {}

        download_buttons, data_dict = process_client(
            client=client,
            dash_dataframe_saver=dash_dataframe_saver,
            cr_decoded=decoded_stored_cr,
            decoded_data_content_string=decoded_data_content_string,
            )
        return download_buttons, data_dict

    else:
        raise PreventUpdate


@app.callback(
    Output({"type": "download-csv-accounts", "id": MATCH}, "data"),
    Input({"type": "btn-download-accounts", "id": MATCH}, "n_clicks"),
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
    Output({"type": "download-csv-data", "id": MATCH}, "data"),
    Input({"type": "btn-download-data", "id": MATCH}, "n_clicks"),
    Input('data-store', 'data'),
    prevent_initial_call=True,
    allow_duplicate=True,
)
def download_csv_data(n_clicks, dfs):
    if not n_clicks:
        raise PreventUpdate
    df_id = ctx.triggered_id["id"]
    df = dfs[df_id]
    return dcc.send_string(df, f"{df_id}.csv")


@app.callback(
    Output(Upload.get_collapse_id('prepare-accounts'), "is_open"),
    Output(FilenameUploaded.get_id('client-first-step'), "children"),
    Output(FilenameUploaded.get_id('client-first-step'), "style"),
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
    Output(Upload.get_collapse_id('prepare-data'), "is_open"),
    Output("filename-uploaded-second-step", "children"),
    Output("filename-uploaded-second-step", "style"),
    Input(Upload.get_upload_id('prepare-data'), "filename"),
    State(Upload.get_collapse_id('prepare-data'), "is_open"),
    Input('data-client-store', 'data'),
    Input('data-client-store', 'data'),
)
def collapse_upload_data(filename, is_open, client_selected, data):
    if filename and client_selected and data:
        return not is_open, html.Div([
            filename,
        ]), {'display': 'block'}
    else:
        raise PreventUpdate


@app.callback(
    Output('client-store', 'data'),
    Output('data-client-store', 'data'),
    Input('clients_dropdown', 'value'),
    prevent_initial_call=True,
)
def get_client(client):
    return {'selected_client': client}, {'selected_client': client + '_data'}


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
              Input('exception-storage', 'data'),
              State("error-client-filename", "is_open"),
              prevent_initial_call=True,
              suppress_callback_exceptions=True)
def process_modal_error(
    list_of_contents, client_selected, filename, n_clicks,
    stored_data, exception_storage, is_open
):

    if not list_of_contents and not client_selected:
        raise PreventUpdate

    if ctx.triggered_id == Upload.get_upload_id('prepare-accounts'):
        if exception_storage or not stored_data:
            return display_modal_error(client_selected, filename, exception_storage)
        raise PreventUpdate

    elif ctx.triggered_id == 'accept-btn-error':
        return not is_open, html.Div(id="accept-btn-error")

    else:
        raise PreventUpdate


@app.callback(
    Output(StepTitle.get_step_id('client-first'), 'children'),
    Output('first-step-container', 'style'),
    Output('preparacion-datos', 'style'),
    Input(CompleteStepBtn.get_btn_id('client-first'), 'n_clicks'),
    prevent_initial_call=True,
    allow_duplicate=True,
)
def mark_first_step_as_completed(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    return (
        html.Img(
            src="assets/check-icon.svg",
            height=30,
            style={'marginLeft': '10px', 'marginBottom': '10px'}
        ),
        {'display': 'none'},
        {'display': 'block'},
        )


@app.callback(
    Output('store-data-provider', 'data', allow_duplicate=True),
    Input(Upload.get_all_upload_id(), 'contents'),
    State(Upload.get_all_upload_id(), 'filename'),
    State('store-data-provider', 'data'),
    prevent_initial_call=True,
)
def upload_csv_without_process(_, __, data_store):

    triggered_input_id, triggered_file_content, triggered_file_name = get_id_and_value_from_context()
    if (
        triggered_file_content and
        (
            triggered_input_id == Upload.get_upload_id(external_providers) or
            triggered_input_id == Upload.get_upload_id(osiris_accounts)
        )
    ):

        if triggered_input_id == Upload.get_upload_id(external_providers):
            data_name = external_providers
        else:
            data_name = osiris_accounts
        content_type, content_data = triggered_file_content.split(',')
        data_store.update(
            {
                data_name: {
                    'content_type': content_type,
                    'filename': triggered_file_name,
                    'data': content_data,
                }
            }
        )
        return data_store
    raise PreventUpdate


@app.callback(
    Output(DownloadButtonsArea.get_id("prepare-external-data-provider"), 'children'),
    Output('store-data-provider', 'data'),
    Input('prepare_data_provider_button', 'n_clicks'),
    State('external_data_providers_dropdown', 'value'),
    State('store-data-provider', 'data'),
)
def process_provider_data(
    click: int,
    external_provider_name: str,
    data_store: dict,
):

    osiris_accunts_data = data_store.get('osiris-accounts')
    external_provider_data = data_store.get('external-providers')

    if click and external_provider_name and osiris_accunts_data and external_provider_data:

        dash_dataframe_saver = DashDataFrameSaver()
        osiris_accunts_data = io.BytesIO(base64.b64decode(osiris_accunts_data.get('data')))
        external_provider_data = io.BytesIO(base64.b64decode(external_provider_data.get('data')))

        download_buttons, result_data = process_external_provider_data(
            dash_dataframe_saver,
            osiris_accunts_data,
            external_provider_data,
            external_provider_name,
        )
        data_store.update({
            'results': result_data,
        })
        return download_buttons, data_store
    raise PreventUpdate


@app.callback(
    Output({"type": "download-csv", "id": MATCH}, "data", allow_duplicate=True),
    Input({"type": "btn-download", "id": MATCH}, "n_clicks"),
    Input('store-data-provider', 'data'),
    prevent_initial_call=True,
    allow_duplicate=True,
)
def download_csv_data_provider(n_clicks, dfs):
    if not n_clicks:
        raise PreventUpdate
    df_id = ctx.triggered_id["id"]
    df = dfs.get('results')[df_id]
    return dcc.send_string(df, df_id)
