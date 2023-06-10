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
                    id=cls.get_icon_id(id)
                ),
            ],
            id=cls.get_btn_id(id),
            style={'display': 'none'}
        )
        return html.Div(
            btn,
            className='completed-step-bnt-container'
        )

    @staticmethod
    def get_icon_id(id: str) -> str:
        return f"check-step-icon-{id}"

    @staticmethod
    def get_btn_id(id: str) -> str:
        return f"complete-step-btn-{id}"
