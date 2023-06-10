from dash import html


class CompleteStepBtn:

    @classmethod
    def create(cls, id: str):

        btn = html.Button(
            [
                html.Span("Completar este paso", className="completed-step-btn", style={"fontSize": "medium"}),
                html.I(
                    className="fa-regular fa-circle-check",
                    style={"color": "white", 'marginLeft': '0.7rem', 'fontSize': 'x-large'},
                    id="check-step-icon"
                ),
            ],
            id=id,
            style={'display': 'none'}
        )
        return html.Div(
            btn,
            className='completed-step-bnt-container'
        )

        return btn
