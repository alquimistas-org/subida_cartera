from dash import html, dcc
import dash_bootstrap_components as dbc


class Upload:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id

    def create(self, title_step: str, id: str, multiple_files: bool = False):

        title = html.Div([
            html.Img(src="assets/attach-icon.svg", height=20, style={'marginLeft': '5px'}),
            html.Span(title_step, className="attach-file",),
            html.Hr(style={"color": "black", "marginTop": "0"})
        ], className="attach-file-container")

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
                    'width': '100%',
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
            title,
            collapse,
            filename_div,
        ])
