import dash_bootstrap_components as dbc
from dash import html


class ClearData:

    @classmethod
    def create(self):

        clear_button = html.Div(
            [
                html.I(className="fa-regular fa-trash-can", id="delete-cr", style={'marginRight': '1rem'}),
                html.Span("Limpiar datos", className="clean-data-text"),
            ],
            id="btn-clear"
        )
        confirm_modal = dbc.Modal(
            [
                dbc.ModalHeader("Confirmación"),
                dbc.ModalBody("¿Querés limpiar los datos?"),
                dbc.ModalFooter(
                    [
                        dbc.Button("Cancelar", id="cancel-btn", className="mr-auto"),
                        dbc.Button("Aceptar", id="accept-btn", color="danger"),
                    ]
                ),
            ],
            id="confirm-modal",
            centered=True,
        )

        return html.Div([
            html.Div([
                clear_button,
                confirm_modal,
            ], className="clear-data-icon-span-container")
        ], className="clear-data-container")
