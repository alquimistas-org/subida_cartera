from dash import dcc


class ClientsDropdown:

    clients = [
        'Comafi',
        'Naranja',
    ]
    id = 'clients_dropdown'

    @classmethod
    def create(cls):
        return dcc.Dropdown(
            id=cls.id,
            options=[{'label': client, 'value': client} for client in cls.clients],
            value=cls.clients[0],
            clearable=False,
            style={'width': '100%'},
        )

    @classmethod
    def get_default_client(cls):
        return cls.clients[0]
