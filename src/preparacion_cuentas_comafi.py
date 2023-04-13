import os
import shutil
import pandas as pd
import numpy as np
import datetime
import time
from .constants.constants import (
    PROVINCES,
    UTIL_COLS_COMAFI,
)

'''
Estimados, esta función está en este momento sin implementar, pero
va a reemplazar a la función con el mismo nombre en el archivo subida_cartera.py
Antes de reemplazarla, quiero probar al menos una vez el software así como está,
y para ello neces
'''

def preparacion_cuentas_comafi():
    nombre_cartera = input('\nIngrese el nombre de la cartera que desea:  ')

    print('Iniciando preparacion')
    # lectura planilla modelo
    df_os = pd.read_csv('modelos/modelo_cuentas.csv', encoding='ANSI', sep=';')
    df = pd.read_excel('emerix.xlsx', dtype=str)

    df = df[list(UTIL_COLS_COMAFI.keys())]
    df = df.rename(columns=UTIL_COLS_COMAFI)

    # reemplazo de valores nulos
    df.loc[df['provincia'].isna(), 'provincia'] = '0'
    # reemplazo de 'ñ' en nombres
    replace_invalid_chars(df)
    print('\n')
    print('\nComenzando escritura de archivos..\n\n')

    fill_data(df, df_os)

    name_folder = f'Subida Osiris/{time.strftime("(%H.%M hs) -")} {nombre_cartera}'
    if os.path.isdir(name_folder):
        shutil.rmtree(name_folder)
    os.mkdir(name_folder)
    # iterear un loop por los subcliente a traves de un grouby
    for name, df_sub in df_os.groupby('subcliente'):
        print(f'Ecribiendo: {name}.csv')
        df_sub = df_sub.drop('subcliente', inplace=False, axis=1)
        df_sub.to_csv(f'{name_folder}/{name}.csv', sep=';', encoding='ANSI', index=False)
    return ' '


def replace_invalid_chars(dataframe):
    characters = ['#', 'Ð', 'ð', '&']
    for char in characters:
        n = dataframe['nombre'].str.contains(char).sum()
        dataframe['nombre'] = dataframe['nombre'].str.replace(char, 'ñ').str.title()
        print(f'character {char}: se remplazaron {n}')


def fill_data(df, df_os):
    date_now = datetime.date.today()
    years_to_add = date_now.year + 3 

    date_1 = date_now.strftime('%d/%m/%Y')
    date_2 = date_now.replace(year=years_to_add).strftime('%d/%m/%Y')

    df_os['Nº de Asignacion (0)'] = df['dni']
    df_os['Razon social (1)'] = df['nombre']
    df_os['ID Tipo de Documento (2)'] = '1'
    df_os['DNI (3)'] = df['dni']

    df_os['Domicilio (4)'] = df['direccion'] + ' - ' + df['localidad']
    df_os['ID Localidad (5)'] = '0'

    df_os['ID Provincia (6)'] = df['provincia'].apply(lambda fila: PROVINCES[fila])
    df_os['Código Postal (7)'] = df['cod_postal']

    df_os['Importe Asignado (11)'] = df['deuda_total']\
        .astype(float).apply(np.ceil).astype(str).str.replace('.0', '', regex=False)
    df_os['Fecha de Ingreso (12)'] = date_1
    df_os['Fecha de Deuda dd/mm/aaaa (13)'] = df['fecha_inicio']
    df_os['Importe Historico (14)'] = df['deuda_capital']\
        .astype(float).apply(np.ceil).astype(str).str.replace('.0', '', regex=False)

    df_os['Observaciones (15)'] = 'Fecha ultimo pago: ' + df['fecha_ult_pago']
    df_os['Fecha Fin de Gestion (16)'] = date_2
    df_os['IDSucursal(17)'] = '1'
    df_os['subcliente'] = df['subcliente']
