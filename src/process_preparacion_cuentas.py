from constants.constants import PROVINCES

NARANJA_FIELDS = {
    'Nº de Asignacion (0)': lambda cr: cr['NRODOC'],
    'Razon social (1)': lambda cr: cr['NOMBRECOMPLETO'].str.title(),
    'ID Tipo de Documento (2)': '1',
    'DNI (3)': lambda cr: cr['NRODOC'],
    'Domicilio (4)': lambda cr: (
                                cr['CALLE'] + ' '
                                + cr['NUMERO'] + ' - '
                                + cr['PISO'] + ' '
                                + cr['DEPTO'] + ' - '
                                + cr['BARRIO'] + ' - '
                                + cr['LOCALIDAD']
                                ),
    'ID Localidad (5)': '0',
    'ID Provincia (6)': lambda cr: cr['PROVINCIA'].apply(lambda fila: PROVINCES[fila]),
    'Código Postal (7)': lambda cr: cr['POSTAL'],
    'Importe Asignado (11)': lambda cr: cr['DEUDA_ACTUALIZADA'].str.replace(', ', '.'),
    'Fecha de Deuda dd/mm/aaaa (13)': lambda cr: cr['INICIOMORA'],
    'Importe Historico (14)': lambda cr: cr['CAPITAL'].str.replace(', ', '.'),
    'Observaciones (15)': lambda cr: (
                                'Gestor anterior: '
                                + cr['GESTOR_ANTERIOR'] + ' - '
                                + 'Score: '
                                + cr['SCORE']
                                .str.replace(', ', '.')
                                .str.replace(',', '.')
                                .astype(float).round(2).astype(str)
                                ),
    'IDSucursal(17)': '1',
    'riesgo': lambda cr: cr['RIESGO']
}
