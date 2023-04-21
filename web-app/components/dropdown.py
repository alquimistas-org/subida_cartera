import dash_bootstrap_components as dbc
from dash import html, dcc


class Dropdown:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id

    def create(self, name_id: str) -> dbc.DropdownMenu:
        dropdown = html.Div([
            dcc.Dropdown([
             'Preparacion cuentas',
             'Preparacion datos',
             'Datos riesgos',
             'Datos info'],
             'Preparacion cuentas', id=f'demo-dropdown-{name_id}'),
            html.Div(id=f'dd-output-container-{name_id}')
        ])
        return dropdown
