from dash import html


class StepTitle:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id

    def create(self, title_step: str):

        title = html.Div([
            html.Img(src="assets/attach-icon.svg", height=20, style={'marginLeft': '5px'}),
            html.Span(title_step, className="attach-file",),
            html.Span(id="icon-success-upload"),
            html.Hr(style={"color": "black", "marginTop": "0"})
        ], className="step-title")

        return title
