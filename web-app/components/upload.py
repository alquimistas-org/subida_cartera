from dash import html, dcc
import dash_bootstrap_components as dbc


class Upload:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id

    def create(self, id: str, multiple_files: bool = False):

        upload = dcc.Upload(
                id=f'upload-data-{id}',
                children=html.Div([
                    html.A(
                        children=[
                            html.Div([html.Img(
                                src="assets/upload-icon.svg",
                                className="upload-icon",
                                style={
                                    "marginTop": "3rem"
                                }
                            )], className="icon-container"),
                            html.H5("Selecciona un archivo", className="select-file-link")
                        ], className="upload-link-container",
                    )
                ]),
                style={
                    'width': '99%',
                    'height': 'auto',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Don't allow multiple files to be uploaded
                multiple=multiple_files,
                disabled=True,
            )

        collapse = dbc.Row(
            dbc.Col(
                dbc.Collapse(
                    upload,
                    id=f"collapse-{id}",
                    is_open=True,
                )
            ),
        )

        filename_div = html.Div(id=f"filename-{id}", className="filaname-container")

        return html.Div([
            collapse,
            filename_div,
        ])
