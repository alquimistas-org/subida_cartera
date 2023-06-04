from dash import html


class DownloadButtonsArea:

    @classmethod
    def create(cls, name: str) -> html.Div:
        return html.Div(
            [
                html.Div(id=cls.get_id(name), className="donwload-container")
            ],
            id=cls.get_id_major_div(name),
            className="major-donwload-container"
        )

    @staticmethod
    def get_id(name: str) -> str:
        """principal id used in callbacks"""
        return f"div-download-{name}"

    @staticmethod
    def get_id_major_div(name: str) -> str:
        return f"major-div-download-{name}"
