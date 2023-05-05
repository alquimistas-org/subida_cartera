from constants.constants import PROVINCES
import json


ACCOUNT_COL = [
    'Nº de Asignacion (0)',
    'Razon social (1)',
    'ID Tipo de Documento (2)',
    'DNI (3)',
    'Domicilio (4)',
    'ID Localidad (5)',
    'ID Provincia (6)',
    'Código Postal (7)',
    'Importe Asignado (11)',
    'Fecha de Deuda dd/mm/aaaa (13)',
    'Importe Historico (14)',
    'Observaciones (15)',
    'IDSucursal(17)',
    'riesgo',
    ]


"""
Creo el diccionario que se va a convertir a JSON para simular la respuesta de una DB.
"""

fake_db_document = {
    'Nº de Asignacion (0)': {'lambda': 'lambda cr: cr["NRODOC"]'},
    'Razon social (1)': {'lambda': 'lambda cr: cr["NOMBRECOMPLETO"].str.title()'},
    'ID Tipo de Documento (2)': {'lambda': 'lambda: "1"'},
    'DNI (3)': {'lambda': 'lambda cr: cr["NRODOC"]'},
    'Domicilio (4)': {'lambda': 'lambda cr: (cr["CALLE"] + " " + cr["NUMERO"] + " - " + cr["PISO"] + " " + cr["DEPTO"] + " - " + cr["BARRIO"] + " - " + cr["LOCALIDAD"])'},
    'ID Localidad (5)': {'lambda': 'lambda: "0"'},
    'ID Provincia (6)': {'lambda': 'lambda cr: cr["PROVINCIA"].apply(lambda fila: PROVINCES[fila])'},
    'Código Postal (7)': {'lambda': 'lambda cr: cr["POSTAL"]'},
    'Importe Asignado (11)': {'lambda': 'lambda cr: cr["DEUDA_ACTUALIZADA"].str.replace(", ", ".")'},
    'Fecha de Deuda dd/mm/aaaa (13)': {'lambda': 'lambda cr: cr["INICIOMORA"]'},
    'Importe Historico (14)': {'lambda': 'lambda cr: cr["CAPITAL"].str.replace(", ", ".")'},
    'Observaciones (15)': {'lambda': 'lambda cr: ("Gestor anterior: "+ cr["GESTOR_ANTERIOR"] + " - " + "Score: "+ cr["SCORE"].str.replace(", ", ".").str.replace(",", ".").astype(float).round(2).astype(str))'},
    'IDSucursal(17)': {'lambda': 'lambda: "1"'},
    'riesgo': {'lambda': 'lambda cr: cr["RIESGO"]'},
    }



"""
Se convierte el diccionario a JSON
"""
fake_db_document_json = json.dumps(fake_db_document)


"""Funcion que recive el JSON lo tansforma en python Dict y genera la plantilla para porcesar datos"""

def prepare_processor(fake_db_document):

    fake_db_document_dict = json.loads(fake_db_document)

    field_processors = {}

    for col in ACCOUNT_COL:
        field_processors[col] = eval(fake_db_document_dict[col]['lambda'])

    return field_processors



"""Plantilla para porcesar datos"""
FIELDS_PROCESSORS = prepare_processor(fake_db_document_json)
