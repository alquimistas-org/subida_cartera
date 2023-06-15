from dash import html


class StepTitle:

    @classmethod
    def create(cls, title_step: str, step_id: str = "") -> html.Div:

        title = html.Div([
            html.Img(src="assets/attach-icon.svg", height=20, style={'marginLeft': '5px'}),
            html.Span(title_step, className="attach-file",),
            html.Span(id=cls.get_step_id(step_id)),
            html.Hr(style={"color": "black", "marginTop": "0"})
        ], className="step-title")

        return title

    @staticmethod
    def get_step_id(step_id: str) -> str:
        return f"icon-success-upload-{step_id}"
