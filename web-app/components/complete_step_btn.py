from dash import html


class CompleteStepBtn:

    @classmethod
    def create(self, id: str):

        btn = html.Div(
            [
                html.Span("Completar este paso", className="completed-step-btn", style={"fontSize": "x-large"}),
                html.I(
                    className="fa-regular fa-circle-check",
                    style={"color": "#24c927", 'marginLeft': '0.7rem', 'fontSize': 'x-large'},
                    id="check-step-icon"
                ),
            ],
            id=id,
            style={'display': 'none'}
        )

        return btn
