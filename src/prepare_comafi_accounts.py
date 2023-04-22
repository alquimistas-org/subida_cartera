import os
import shutil
import pandas as pd
import numpy as np
import datetime
import time
from constants.constants import (
    EMERIX_FILE_PATH,
    INVALID_CHARACTERS,
    PROVINCES,
    ROOT_PATH,
    UTIL_COLS_COMAFI,
)

'''
Estimados, esta función está en este momento sin implementar, pero
va a reemplazar a la función con el mismo nombre en el archivo subida_cartera.py
Antes de reemplazarla, quiero probar al menos una vez el software así como está,
y para ello neces
'''


def prepare_comafi_accounts(nombre_cartera, emerix_file_path=EMERIX_FILE_PATH):

    print('Iniciando preparacion')
    # lectura planilla modelo
    try:
        df_os = pd.read_csv('modelos/modelo_cuentas.csv', encoding='latin_1', sep=';')
    except Exception:
        df_os = pd.read_csv('modelos/modelo_cuentas.csv', encoding='ANSI', sep=';')
    df = pd.read_excel(emerix_file_path, dtype=str)
    col_utiles = UTIL_COLS_COMAFI

    df = df[list(col_utiles.keys())]
    df = df.rename(columns=col_utiles)

    # reemplazo de valores nulos
    df.loc[df['provincia'].isna(), 'provincia'] = '0'
    # reemplazo de 'ñ' en nombres
    replace_invalid_chars(df)
    fill_data(df, df_os)

    new_directory = ROOT_PATH / f'Subida Osiris/{time.strftime("(%H.%M hs) -")} {nombre_cartera}'
    if os.path.isdir(new_directory):
        shutil.rmtree(new_directory)
    os.mkdir(new_directory)

    write_csv_per_subcliente(df_os, new_directory)
    return new_directory


def replace_invalid_chars(dataframe):
    for char in INVALID_CHARACTERS:
        n = dataframe['nombre'].str.contains(char).sum()
        dataframe['nombre'] = dataframe['nombre'].str.replace(char, 'ñ').str.title()
        print(f'character {char}: se remplazaron {n}')


def fill_data(df, df_os):
    '''
    Takes two dataframes, so it can fill the second df based upon
    the values of the first one.
    :param df: dataframe where we take data from
    :param df_os: dataframe to be filled
    Does not return anything.
    '''
    print('\n')
    print('\nComenzando escritura de archivos..\n\n')
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


def write_csv_per_subcliente(dataframe, folder_name):
    for name, df_sub in dataframe.groupby('subcliente'):
        print(f'Ecribiendo: {name}.csv')
        df_sub = df_sub.drop('subcliente', inplace=False, axis=1)
        try:
            df_sub.to_csv(f'{folder_name}/{name}.csv', sep=';', encoding='latin_1', index=False)
        except Exception:
            df_sub.to_csv(f'{folder_name}/{name}.csv', sep=';', encoding='ANSI', index=False)
