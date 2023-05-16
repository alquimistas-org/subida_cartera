from dash import html


class ClientButton:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id
        self.selected_button = None

    def create(self):
        naranja = html.Button(
            "Naranja",
            id="naranja",
            className='btn-tab',
            n_clicks=0
        )
        comafi = html.Button(
            "Comafi",
            id="comafi",
            className='btn-tab',
            n_clicks=0
        )

        return html.Div([
            naranja,
            comafi,
        ], style={'marginBottom': '4rem', 'marginTop': '2rem'}, className='tabs-container')

    def style_button(self, button_id):
        if self.selected_button == button_id:
            return {'backgroundColor': 'gray'}
        else:
            return {'backgroundColor': 'white'}
