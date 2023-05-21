from dash import dcc


class ExternalDataProvidersDropDown:

    data_providers = [
        'Riesgo Online',
        'Info Experto',
    ]
    id = 'external_data_providers_dropdown'

    @classmethod
    def create(cls):
        return dcc.Dropdown(
            id=cls.id,
            options=[{'label': provider, 'value': provider} for provider in cls.data_providers],
            value=cls.data_providers[0],
            clearable=False,
            style={'width': '100%'},
        )
