from dash import dcc


class ExternalDataProvidersDropDown:

    data_providers = {
        '-': '-',
        'Riesgo Online': 'riesgo-online',
        'Info Experto': 'info-experto',
    }
    id = 'external_data_providers_dropdown'

    @classmethod
    def create(cls):
        return dcc.Dropdown(
            id=cls.id,
            options=[{'label': label, 'value': value} for label, value in cls.data_providers.items()],
            value=list(cls.data_providers.values())[0],
            clearable=False,
            style={'width': '100%'},
        )
