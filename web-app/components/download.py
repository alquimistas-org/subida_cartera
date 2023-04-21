from dash import html, dcc


class Download:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id

    def create(self, name_id: str) -> dcc.Download:
        download = html.Div([
            html.Button("Descargar planilla", id=f"btn-download-txt-{name_id}"),
            dcc.Download(id=f"download-text-{name_id}")
        ])
        return download
