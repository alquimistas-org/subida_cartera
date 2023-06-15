from dash import html


class FilenameUploaded:

    @classmethod
    def create(cls, id: str) -> html.Div:
        return html.Div(
            id=cls.get_id(id),
            style={'display': 'none'},
            className='filaname-container'
        )

    @staticmethod
    def get_id(id: str) -> dict:
        return {'type': 'filename-uploaded', 'id': id}
