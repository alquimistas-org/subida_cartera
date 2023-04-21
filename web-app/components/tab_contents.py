import dash_bootstrap_components as dbc
from .upload import Upload
from .radioitems import RadioItems
from .download import Download


class TabsContent:

    def __init__(self, id: str, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id
        self.id = id

    def create(self, client_id: str):
        upload_file = Upload()
        radio_items = RadioItems()
        download = Download()

        tabs_content = dbc.Card(
            dbc.CardBody(
                [
                    radio_items.create(),
                    upload_file.create(client_id),
                    download.create(self.id),
                ]
            ),
            className="mt-3",
        )

        return tabs_content
