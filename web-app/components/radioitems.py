from dash import html, dcc


class RadioItems:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id

    def create(self: str) -> dcc.RadioItems:
        radio_items = dcc.RadioItems(
            options=[
                {
                    'label': [
                        html.Img(src="/assets/excel-icon.svg", height=20, style={'marginLeft': '5px'}),
                        html.Span("Preparación cuentas", style={'font-size': '2rem', 'padding-left': 5}),
                    ],
                    'value': 'cuentas',
                },
                {
                    'label': [
                        html.Img(src="/assets/data-icon.svg", height=20, style={'marginLeft': '5px'}),
                        html.Span("Preparación datos", style={'font-size': '2rem', 'padding-left': 5}),
                    ],
                    'value': 'datos'
                },
                {
                    'label': [
                        html.Img(src="/assets/risk-icon.svg", height=20, style={'marginLeft': '5px'}),
                        html.Span("Datos riesgos", style={'font-size': '2rem', 'padding-left': 5}),
                    ],
                    'value': 'riesgo',
                },
                {
                    'label': [
                        html.Img(src="/assets/patrimonial-icon.svg", height=20, style={'marginLeft': '5px'}),
                        html.Span("Datos info", style={'font-size': '2rem', 'padding-left': 5}),
                    ],
                    'value': 'info'
                },
            ]
        )
        return radio_items
