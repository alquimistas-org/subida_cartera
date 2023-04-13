import pandas as pd

## replace_invalid_chars ['#', 'Ð', 'ð', '&']

invalid_chars_dataframe = pd.DataFrame(
    {
        "Numbers": [30, 25, 12, 14],
        "nombre": ["JuanÐ", "Jorðe","Luca&", "Nu#ez"],
    }
)

expected_invalid_chars_dataframe = pd.DataFrame(
    {
        "Numbers": [30, 25, 12, 14],
        "nombre": ["Juanñ", "Jorñe","Lucañ", "Nuñez"],
    }
)

# Data for fill_data(), which takes "df" to fill "df_os"

non_os_test_dataframe = pd.DataFrame(
    {
        'dni': ['12345678', '87654321'],
        'nombre': ['Juan Perez', 'Jorge Fernandez'],
        'direccion': ['Calle Tal 4567', 'Calle Otra 23'],
        'localidad': ['Maipu', 'Lujan'],
        'provincia': ['MENDOZA', 'MENDOZA',],
        'cod_postal': ['1234', '1111'],
        'deuda_total': [123456, 34567634],
        'fecha_inicio': ['01/01/2023', '02/02/2023'],
        'fecha_ult_pago': ['25/01/2023', '25/02/2023'],
        'deuda_capital': [543865, 5437654],
        'subcliente' : ['Empresa1', 'Empresa2',],
    }
)

os_test_dataframe = pd.DataFrame(
    columns=[
        'Nº de Asignacion (0)',
        'Razon social (1)',
        'ID Tipo de Documento (2)',
        'DNI (3)',
        'Domicilio (4)',
        'ID Localidad (5)',
        'ID Provincia (6)',
        'Código Postal (7)',
        'Importe Asignado (11)',
        'Fecha de Ingreso (12)',
        'Fecha de Deuda dd/mm/aaaa (13)',
        'Importe Historico (14)',
        'Observaciones (15)',
        'Fecha Fin de Gestion (16)',
        'IDSucursal(17)',
        'subcliente',
    ]
)

os_test_other_dataframe = pd.DataFrame(
    columns=[
        'dni',
        'nombre',
        'direccion',
        'localidad',
        'cod_postal',
        'provincia',
        'telefono',
        'sucursal',
        'banca',
        'cod_linea',
        'linea',
        'deuda_total',
        'deuda_capital',
        'dias_mora',
        'fecha_inicio',
        'fecha_ult_pago',
        'subcliente',
    ]
)
