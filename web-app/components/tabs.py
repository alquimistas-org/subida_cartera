import dash_bootstrap_components as dbc
from .tab_contents import TabsContent
from dash import html, dcc


class Tabs:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id

    def create(self) -> dbc.Tabs:
        naranja_tab_content = TabsContent("naranja")
        comafi_tab_content = TabsContent("comafi")

        tabs = html.Div([
            dcc.Tabs(id="tabs-example-graph", value='naranja', children=[
                dcc.Tab(
                    label="Naranja",
                    value='naranja',
                    children=naranja_tab_content.create("naranja"),
                ),
                dcc.Tab(
                    label='Comafi',
                    value='comafi',
                    children=comafi_tab_content.create("comafi"),
                ),
                ]
            ),
        ])

        return tabs
