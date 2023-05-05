import io
import pandas as pd
import numpy as np
import datetime
from typing import Union
from constants.constants import (
    EMERIX_FILE_PATH,
    INVALID_CHARACTERS,
    PROVINCES,
    ROOT_PATH,
    UTIL_COLS_COMAFI,
)
from adapters.file_dataframe_saver import FileDataFrameSaver
from ports.dataframe_saver import DataFrameSaver


def prepare_comafi_accounts(
        emerix_file_path: Union[str, io.BytesIO, io.StringIO] = EMERIX_FILE_PATH,
        dataframe_saver: DataFrameSaver = None,
) -> None:

    portfolio_name = input('\nIngrese el nombre de la cartera que desea:  ')  # TODO: move this input to CMD interface

    if not dataframe_saver:
        dataframe_saver = FileDataFrameSaver(output_path=ROOT_PATH / 'Subida Osiris/', portfolio_name=portfolio_name)

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

    write_csv_per_subcliente(df_os, dataframe_saver)


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


def write_csv_per_subcliente(dataframe: pd.DataFrame, dataframe_saver: DataFrameSaver):
    for name, df_sub in dataframe.groupby('subcliente'):
        print(f'Ecribiendo: {name}.csv')
        df_sub = df_sub.drop('subcliente', inplace=False, axis=1)
        dataframe_saver.save_df(name=name, df=df_sub)
