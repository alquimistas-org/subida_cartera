from pathlib import Path


PROGRAMMER = 'xxxxxxxxxxxxx@xxxxxxxxxxxxx.com'
USER = 'xxxxxxxxxxxxx@xxxxxxxxxxxxx.com'
PASSWORD = 'xxxxxxxxxxxxx'
DATA_UPLOADER_HEADER = [
    "ID Cuenta o Nro. de Asig. (0)",
    "ID SubCliente (1)",
    "Activa (S, N) (2)",
    "ID Supervisor (3)",
    "ID Ejecutivo (4)",
    "Nº de Asignación Nuevo (5)",
    "Fecha de Contacto (6)",
    "ID Acción (7)",
    "ID Resultado (8)",
    "Notas (9)",
    "ID Usuario (10)",
    "ID SubEstado (11)",
    "ID SubCliente (12)",
    "Importe Asignado (13)",
    "Importe Histórico (14)",
    "Observaciones (15)",
    "Email (16)",
    "ID Tipo de Teléfono (17)",
    "Nro. de Teléfono (18)",
    "Obs. de Teléfono (19)",
    "ID Tipo de Domicilio (20)",
    "Domicilio sin Formato (21)",
    "Obs. de Domicilio (22)",
    "ID Localidad (23)",
    "ID Provincia (24)",
    "Fecha de Vencimiento (25)",
    "Número de Referencia (26)",
    "Importe Factura (27)",
    "Observaciones Factura (28)",
    "ID Sucursal (29)",
    "Fecha de Pago (30)",
    "ID Concepto (31)",
    "Importe de Pago(32)",
    "ID Usuario  de Pago(33)",
    "Rendido (S, N) (34)",
    "Fecha Proximo Pago (35)",
    "Importe Proximo Pago (36)",
    "Fecha de Acuerdo (37)",
    "Días de Vencimiento (38)",
    "Importe de Acuerdo (39)",
    "Sueldo (40)",
    "Cantidad de Vehiculos (41)",
    "Datos Patrimoniales (42)",
]

PROVINCES = {
    '0': '0',
    'BUENOS AIRES':	'24',
    'CAPITAL FEDERAL': '23',
    'CATAMARCA': '22',
    'CHACO': '21',
    'CHUBUT': '20',
    'CORDOBA': '19',
    'CORRIENTES': '18',
    'ENTRE RIOS': '17',
    'FORMOSA': '16',
    'JUJUY': '15',
    'LA PAMPA': '14',
    'LA RIOJA': '13',
    'MENDOZA': '12',
    'MISIONES': '11',
    'NEUQUEN': '10',
    'RIO NEGRO': '9',
    'SALTA': '8',
    'SAN JUAN': '7',
    'SAN LUIS': '6',
    'SANTA CRUZ': '5',
    'SANTIAGO DEL ESTERO': '4',
    'TIERRA DEL FUEGO': '3',
    'SANTA FE': '2',
    'TUCUMAN': '1'
}

UTIL_COLS_COMAFI = {
    'Nº Doc': 'dni',
    'Apellido, Nombre': 'nombre',
    'Direccion': 'direccion',
    'Localidad': 'localidad',
    'Cod. Pos.': 'cod_postal',
    'Provincia': 'provincia',
    'Telefono': 'telefono',
    'Sucursal': 'sucursal',
    'Banca': 'banca',
    'Cod. Linea': 'cod_linea',
    'Linea': 'linea',
    'Deuda Vencida': 'deuda_total',
    'Cap.': 'deuda_capital',
    'Dias Mora': 'dias_mora',
    'Inicio mora': 'fecha_inicio',
    'Fecha Ult. Pago': 'fecha_ult_pago',
    'Subcliente': 'subcliente',
}

ACCOUNT_PREP_COL = [
    'Nº de Asignacion (0)',
    'Razon social (1)',
    'ID Tipo de Documento (2)',
    'DNI (3)',
    'Domicilio (4)',
    'ID Localidad (5)',
    'ID Provincia (6)',
    'Código Postal (7)',
    'Observaciones Domicilio (8)',
    'Numero Telefono (9)',
    'Observaciones Telefono (10)',
    'Importe Asignado (11)',
    'Fecha de Ingreso (12)',
    'Fecha de Deuda dd/mm/aaaa (13)',
    'Importe Historico (14)',
    'Observaciones (15)',
    'Fecha Fin de Gestion (16)',
    'IDSucursal(17)',
]

DATA_PREP_COLUMNS = [
    'NRODOC',
    'RIESGO',
    'TIPO_CUENTA',
    'TIPO_CUENTA',
    'TEL_PARTICULAR',
    'TEL_LABORAL',
    'TEL_ALTERNATIVO',
    'TEL_CR_PARTICULAR',
    'TEL_CR_LABORAL',
    'TEL_CR_ALTERNATIVO',
    'EMAIL',
    'ULTIMO_PAGO',
]

DATA_INFO_COLUMNS = [
    'NUMERO DOCUMENTO',
    'NUMERO 1',
    'NUMERO 2',
    'NUMERO 3',
    'E-MAIL',
    'REMUNERACION',
    'RAZON SOCIAL',
    'CANTIDAD.2',
    'DETALLE.1',
    'NSE',
]

DATA_INFO_COLUMNS_RENAME = {
    'NUMERO DOCUMENTO': 'DNI',
    'NUMERO 1': 'tel_info_1',
    'NUMERO 2': 'tel_info_2',
    'NUMERO 3': 'tel_info_3',
    'E-MAIL': 'MAIL_info',
    'REMUNERACION': 'sueldo_info',
    'RAZON SOCIAL': 'empleador_info',
    'CANTIDAD.2': 'q_vehiculos',
    'DETALLE.1': 'detalle_veh',
    'NSE': 'NSE_info',
}

NUMBER_OF_COLUMNS = 66

CR_FILE_PATH = Path('./cr.csv')
OSIRIS_ACCOUNTS_FILE_PATH = Path('./cuentas.csv')
RISK_FILE_PATH = Path('./risk.csv')
EMERIX_FILE_PATH = Path('./emerix.xlsx')
