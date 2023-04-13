import dash_bootstrap_components as dbc
from .upload import drag_and_drop
from .dropdown import dropdown

dbc_card_body = dbc.CardBody(
        [
            dropdown,
            drag_and_drop
        ]
    )

tab1_content = dbc.Card(
    dbc_card_body,
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc_card_body,
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Naranja"),
        dbc.Tab(tab2_content, label="Comafi"),
    ]
)
