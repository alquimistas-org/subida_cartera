from dash import html


class ClientButton:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id

    def create(self):
        naranja = html.Button("Naranja", id="naranja-btn", className='btn-tab')
        comafi = html.Button("Comafi", id="comafi-btn", className='btn-tab')

        return html.Div([
            naranja,
            comafi,
        ], style={'marginBottom': '4rem', 'marginTop': '4rem'}, className='tabs-container')
