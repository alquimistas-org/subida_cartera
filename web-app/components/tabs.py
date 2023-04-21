import dash_bootstrap_components as dbc
from .upload import Upload
from .dropdown import Dropdown
from .download import Download


class Tabs:

    def __init__(self, input_id='input', output_id='output') -> None:
        self.input_id = input_id
        self.output_id = output_id

    def createTabs(self) -> dbc.Tabs:
        upload_file = Upload()
        dropdown = Dropdown()
        download = Download()

        tab1_content = dbc.Card(
            dbc.CardBody(
                [
                    dropdown.create("naranja"),
                    upload_file.create(1),
                    download.create("naranja")
                ]
            ),
            className="mt-3",
        )

        tab2_content = dbc.Card(
            dbc.CardBody(
                [
                    dropdown.create("comafi"),
                    upload_file.create(2),
                    download.create("comafi"),

                ]
            ),
            className="mt-3",
        )

        tabs = dbc.Tabs(
            [
                dbc.Tab(
                    label="Naranja",
                    children=tab1_content,
                ),
                dbc.Tab(
                    label="Comafi",
                    children=tab2_content,
                ),
            ]
        )

        return tabs
