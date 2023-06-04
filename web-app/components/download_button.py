from dash import (
    html,
    dcc,
)


class DownloadButton:
    download_ico = html.I(
                    className="fa-solid fa-circle-down",
                    style={'marginRight': '10px'},
                )

    @classmethod
    def create(cls, name: str):
        return html.Div([
                html.Button(
                    [
                        cls.download_ico,
                        f"Descargar {name}"
                    ],
                    id=cls.get_button_id(name),
                    className="download-button"
                ),
                dcc.Download(id=cls.get_dcc_download_id(name))
            ])

    @staticmethod
    def get_button_id(name):
        return {
            "type": "btn-download",
            "id": name,
        }

    @staticmethod
    def get_dcc_download_id(name):
        return {
            "type": "download-csv",
            "id": name,
        }
