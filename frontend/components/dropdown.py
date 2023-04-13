import dash_bootstrap_components as dbc
from dash import html

items = [
    dbc.DropdownMenuItem("Preparación cuentas",),
    dbc.DropdownMenuItem("Preparación datos",),
    dbc.DropdownMenuItem("Datos riesgos",),
    dbc.DropdownMenuItem("Datos info",),
]

dropdown = html.Div(
    [
        dbc.DropdownMenu(
            label="Selecciona una opción",
            size="lg",
            children=items,
            className="mb-3",
        ),
    ]
)
