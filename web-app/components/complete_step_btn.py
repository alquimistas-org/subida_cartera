from dash import html


class CompleteStepBtn:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id

    def create(self):

        btn = html.Div(
            [
                html.Span("Completar este paso", className="completed-step-btn", style={"fontSize": "x-large"}),
                html.I(
                    className="fa-regular fa-circle-check",
                    style={"color": "#24c927", 'marginLeft': '0.7rem', 'fontSize': 'x-large'},
                    id="check-step-icon"
                ),
            ],
            id=self.input_id,
            style={'display': 'none'}
        )

        return btn
