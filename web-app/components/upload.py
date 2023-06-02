from dash import (
    html,
    dcc,
    ALL,
    MATCH,
)
import dash_bootstrap_components as dbc


class Upload:

    @classmethod
    def create(
        cls,
        id: str,
        multiple_files: bool = False,
        upload_disabled: bool = True,
    ):
        upload = dcc.Upload(
                id=cls.get_upload_id(id),
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
                disabled=upload_disabled,
            )

        collapse = dbc.Row(
            dbc.Col(
                dbc.Collapse(
                    upload,
                    id=cls.get_collapse_id(id),
                    is_open=True,
                )
            ),
        )

        filename_div = html.Div(id=cls.get_filename_div_id(id), className="filaname-container")

        return html.Div([
            collapse,
            filename_div,
        ])

    @staticmethod
    def get_upload_id(id: str) -> dict:
        return {'type': 'upload-data', 'id': id}

    @staticmethod
    def get_upload_id_that_matchs():
        return {'type': 'upload-data', 'id': MATCH}

    @staticmethod
    def get_all_upload_id():
        return {'type': 'upload-data', 'id': ALL}

    @staticmethod
    def get_collapse_id(id: str):
        return f"collapse-{id}"

    @staticmethod
    def get_filename_div_id(id: str):
        return f"filename-{id}"
