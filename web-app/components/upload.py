from dash import html, dcc


class Upload:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id

    def create(self, id: str):
        upload = html.Div([
            html.Div([
                html.Img(src="assets/attach-icon.svg", height=20, style={'marginLeft': '5px'}),
                html.Span("Cargar archivo", className="attach-file"),
            ], className="attach-file-container"),
            dcc.Upload(
                id=f'upload-data-{id}',
                children=html.Div([
                    html.A(
                        children=[
                            html.Img(
                                src="assets/upload-icon.svg",
                                className="upload-icon",
                                style={
                                    "marginTop": "3rem"
                                }
                            ),
                            html.H5("Selecciona un archivo", className="select-file-link")
                        ],
                    )
                ]),
                style={
                    'width': '100%',
                    'height': '250px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Don't allow multiple files to be uploaded
                multiple=False,
            ),
        ])

        return upload
