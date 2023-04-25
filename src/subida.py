from cmd import Cmd
import pandas as pd
import numpy as np
from datetime import datetime, date
import traceback
from typing import Union
import io

from driver_email import enviar_mail_con_adjuntos
from constants.constants import (
    ACCOUNT_PREP_COL,
    CR_FILE_PATH,
    DATA_PREP_COLUMNS,
    EMERIX_FILE_PATH,
    OSIRIS_ACCOUNTS_FILE_PATH,
    PASSWORD,
    PROGRAMMER,
    PROVINCES,
    ROOT_PATH,
    USER,
    UTIL_COLS_COMAFI,
)
from risk_data import risk_data
from clean_numbers import clean_numbers
from data_info import GenerateDataInfo
from prepare_comafi_accounts import prepare_comafi_accounts
from adapters.file_dataframe_saver import FileDataFrameSaver
from write_data_osiris import Escribir_Datos_Osiris
from ports.dataframe_saver import DataFrameSaver


def limpiar_numeros(df_num):
    con_doble_guion = df_num['telefono'].str.contains('--')
    sin_doble_guion = ~ con_doble_guion
    con_054 = df_num['telefono'].str.contains('(054)', regex=False)
    con_guion_1 = df_num['telefono'].str.contains('-1-', regex=False)

    df_num['telefono_2'] = np.nan
    # limpiando los que tienen 11 011 y 0
    numeros_concatenar = df_num[sin_doble_guion & con_054 & ~con_guion_1]['telefono'].str.split('-', expand=True)
    if not numeros_concatenar.empty:
        df_num.loc[sin_doble_guion & con_054 & ~con_guion_1, 'telefono_2'] = (
            numeros_concatenar[1] + numeros_concatenar[2]
            )\
            .str.replace(r'^[0]+', '', regex=True)\
            .str.replace(r'^[54]+', '', regex=True)\
            .str.replace(r'^[0]+', '', regex=True)

    # limpieza de los que tiene -1- en medio
    con_1_medio = sin_doble_guion & con_054 & con_guion_1
    numeros_concatenar = df_num[con_1_medio]['telefono'].str.split('-', expand=True)
    if not numeros_concatenar.empty:
        df_num.loc[con_1_medio, 'telefono_2'] = numeros_concatenar[2]\
            .str.replace(r'^[0]+', '', regex=True)\
            .str.replace(r'^[54]+', '', regex=True)\
            .str.replace(r'^[0]+', '', regex=True)

    # limpieza numeros CON DOBLE GUION
    con_doble_guion = df_num[con_doble_guion]['telefono'].str.split('--', expand=True)
    if not numeros_concatenar.empty:
        df_num.loc[con_doble_guion, 'telefono_2'] = con_doble_guion[1]\
            .str.replace(r'^[0]+', '', regex=True)\
            .str.replace(r'^[54]+', '', regex=True)\
            .str.replace(r'^[0]+', '', regex=True)

    # resto de los numeros que quedaron vacios
    vacios = df_num['telefono_2'].isna()
    df_num.loc[vacios, 'telefono_2'] = df_num[vacios]['telefono']\
        .str.replace(r'[^\d]+', '', regex=True)\
        .str.replace(r'^[0]+', '', regex=True)\
        .str.replace(r'^[54]+', '', regex=True)\
        .str.replace(r'^[0]+', '', regex=True)

    return df_num


def Preparacion_Cuentas(
    cr_file_path: Union[str, io.BytesIO, io.StringIO] = CR_FILE_PATH,
    dataframe_saver: DataFrameSaver = None,
) -> None:

    "Condiciones"

    if not dataframe_saver:
        dataframe_saver = FileDataFrameSaver(output_path=ROOT_PATH / 'Subida Osiris/')

    try:
        cr = pd.read_csv(cr_file_path, sep=';', encoding='latin_1', dtype=str)
    except Exception:
        cr = pd.read_csv(cr_file_path, sep=';', encoding='ANSI', dtype=str)

    columnas = ACCOUNT_PREP_COL
    df_os = pd.DataFrame(columns=columnas)

    provincias = PROVINCES

    date_now = date.today()
    years_to_add = date_now.year + 3

    date_1 = date_now.strftime('%d/%m/%Y')
    date_2 = date_now.replace(year=years_to_add).strftime('%d/%m/%Y')

    df_os['Nº de Asignacion (0)'] = cr['NRODOC']
    df_os['Razon social (1)'] = cr['NOMBRECOMPLETO'].str.title()
    df_os['ID Tipo de Documento (2)'] = '1'
    df_os['DNI (3)'] = cr['NRODOC']

    df_os['Domicilio (4)'] = (
        cr['CALLE'] + ' ' + cr['NUMERO'] + ' - ' + cr['PISO'] + ' ' +
        cr['DEPTO'] + ' - ' + cr['BARRIO'] + ' - ' + cr['LOCALIDAD']
    )

    df_os['ID Localidad (5)'] = '0'

    df_os['ID Provincia (6)'] = cr['PROVINCIA'].apply(lambda fila: provincias[fila])
    df_os['Código Postal (7)'] = cr['POSTAL']
    df_os['Importe Asignado (11)'] = cr['DEUDA_ACTUALIZADA'].str.replace(',', '.').str.replace(',', '.')
    df_os['Fecha de Ingreso (12)'] = date_1
    df_os['Fecha de Deuda dd/mm/aaaa (13)'] = cr['INICIOMORA']
    df_os['Importe Historico (14)'] = cr['CAPITAL'].str.replace(',', '.').str.replace(',', '.')
    df_os['Observaciones (15)'] = (
        'Gestor anterior: ' + cr['GESTOR_ANTERIOR'] + ' - ' + 'Score: ' +
        cr['SCORE'].str.replace(',', '.').astype(float).round(2).astype(str)
    )
    df_os['Fecha Fin de Gestion (16)'] = date_2
    df_os['IDSucursal(17)'] = '1'
    df_os['riesgo'] = cr['RIESGO']

    for name, df_sub in df_os.groupby('riesgo'):
        dataframe_saver.save_df(name=name, df=df_sub)


def Preparacion_Cuentas_Comafi(emerix_file_path=EMERIX_FILE_PATH):

    nombre_cartera = input('\nIngrese el nombre de la cartera que desea:  ')
    result_directory_path = prepare_comafi_accounts(nombre_cartera, emerix_file_path=emerix_file_path)
    return result_directory_path


def Preparacion_Datos(cr_file_path=CR_FILE_PATH, osiris_accounts_file_path=OSIRIS_ACCOUNTS_FILE_PATH):
    ' Necesita que este en la carpeta'
    print('Preparando planillas de datos...')
    try:
        cr = pd.read_csv(cr_file_path, sep=';', encoding='latin_1', dtype=str)
        cuentas_subidas = pd.read_csv(osiris_accounts_file_path, encoding='latin_1', sep=';', dtype=str)
    except Exception:
        cr = pd.read_csv(cr_file_path, sep=';', encoding='ANSI', dtype=str)
        cuentas_subidas = pd.read_csv(osiris_accounts_file_path, encoding='ANSI', sep=';', dtype=str)

    cuentas_subidas = cuentas_subidas[['Cuenta', 'Mat. Unica']].rename(columns={'Mat. Unica': 'DNI'}, inplace=False)

    df_cr = cr[DATA_PREP_COLUMNS].rename(columns={'NRODOC': 'DNI'}, inplace=False).copy()
    df_cr = pd.merge(cuentas_subidas, df_cr, how="inner", on="DNI")

    frames = list()
    print('Subiendo numeros...\n')
    print('----------------------')

    # MASIVOS

    # paso TEL_ALTERNATIVO esta vacio
    df = df_cr.loc[
        df_cr['TEL_ALTERNATIVO'].notnull(), ['Cuenta', 'TEL_ALTERNATIVO']
    ].rename(columns={'TEL_ALTERNATIVO': 'TEL'}, inplace=False).copy()
    df['ID_FONO'] = '1'
    print(f'{len(df)} Telefonos ALTERNATIVOS cargados com MASIVOS')
    frames.append(df)

    # paso TEL_PARTICULAR como masivo.
    df = df_cr.loc[
        df_cr['TEL_ALTERNATIVO'].isnull() & df_cr['TEL_PARTICULAR'].notnull(), ['Cuenta', 'TEL_PARTICULAR']
    ].rename(columns={'TEL_PARTICULAR': 'TEL'}, inplace=False).copy()
    df_cr.loc[df_cr['TEL_ALTERNATIVO'].isnull() & df_cr['TEL_PARTICULAR'].notnull(), 'TEL_PARTICULAR'] = np.nan
    df['ID_FONO'] = '1'
    print(f'{len(df)} Telefonos PARTICULAR cargados com MASIVOS en cuentas que no poseen ALTERNATIVO')
    frames.append(df)

    # FIJOS
    df = df_cr.loc[df_cr['TEL_PARTICULAR'].notnull(), ['Cuenta', 'TEL_PARTICULAR']]\
        .rename(columns={'TEL_PARTICULAR': 'TEL'}, inplace=False).copy()
    df['ID_FONO'] = '2'
    print(f'{len(df)} Telefonos ALTERNATIVOS cargados como FIJOS')
    frames.append(df)

    # LABORALES
    df = df_cr.loc[
        df_cr['TEL_LABORAL'].notnull(), ['Cuenta', 'TEL_LABORAL']
    ].rename(columns={'TEL_LABORAL': 'TEL'}, inplace=False).copy()
    df['ID_FONO'] = '3'
    print(f'{len(df)} Telefonos LABORALES cargados como LABORALES')
    frames.append(df)

    # OTROS
    df = df_cr.melt(
        id_vars=['Cuenta'], value_vars=['TEL_CR_PARTICULAR', 'TEL_CR_LABORAL', 'TEL_CR_ALTERNATIVO']
        ).dropna().copy()
    df = df[['Cuenta', 'value']].rename(columns={'value': 'TEL'}, inplace=False)
    df['ID_FONO'] = '8'
    print(f'{len(df)} Telefonos OTROS_CR cargados como OTROS')
    frames.append(df)
    print('----------------------\n')

    df_tels = pd.concat(frames)

    # Depuracion
    df_tels['TEL'] = df_tels['TEL'].str.replace(r'[^0-9]+', '', regex=True)   # elimina todo lo que no sea un numero
    # df_tels['TEL'] = df_tels['TEL'].str.replace('-', '')
    df_tels['TEL'] = df_tels['TEL'].str.replace(' ', '')
    df_tels['TEL'] = df_tels['TEL'].replace('', np.nan)
    df_tels['TEL'].fillna(0)
    df_tels = df_tels.astype({'TEL': 'Int64'})
    df_tels = df_tels.astype({'TEL': 'str'})
    df_tels.drop(df_tels[df_tels.TEL == '0'].index, inplace=True)

    result_df_phones_file_path = Escribir_Datos_Osiris(
        df_tels,
        'datos_cr_subida_telefonos.csv',
        ['Cuenta', 'ID_FONO', 'TEL'],
        ['ID Cuenta o Nro. de Asig. (0)', "ID Tipo de Teléfono (17)", "Nro. de Teléfono (18)"]
    )
    print(f'{len(df_tels)} TELEFONOS se guardaron en archivo: subida_telefono.csv')
    # reemplazar cualquier caractaer alfabetico que este dentro del numero para evitar roblema en futuro
    # borrar numero cero
    df_cr.loc[df_cr['EMAIL'].notnull(), 'EMAIL'] = df_cr.loc[df_cr['EMAIL'].notnull(), 'EMAIL'].str.replace(' ', '')
    df_mail = df_cr.loc[df_cr['EMAIL'].notnull(), ['Cuenta', 'EMAIL']].copy()
    result_df_mails_file_path = Escribir_Datos_Osiris(
        df_mail,
        'datos_cr_subida_mail.csv',
        ['Cuenta', 'EMAIL'],
        ['ID Cuenta o Nro. de Asig. (0)', "Email (16)"]
    )
    print(f'{len(df_mail)} MAILS se guardaron en archivo: subida_mail.csv\n\n')
    all_result_file_paths = [result_df_phones_file_path, result_df_mails_file_path]
    return all_result_file_paths


def Preparacion_Datos_Comafi(emerix_file_path=EMERIX_FILE_PATH, osiris_accounts_file_path=OSIRIS_ACCOUNTS_FILE_PATH):

    print('Preparando planillas de datos para comafi...')
    try:
        df_subida = pd.read_csv('modelos/modelo_datos.csv', encoding='latin_1', sep=';')
    except Exception:
        df_subida = pd.read_csv('modelos/modelo_datos.csv', encoding='ANSI', sep=';')

    df_num = pd.read_excel(emerix_file_path, dtype=str)
    col_utiles = UTIL_COLS_COMAFI
    df_num = df_num[list(col_utiles.keys())]
    df_num = df_num.rename(columns=col_utiles)
    df_num = df_num[df_num['telefono'].notna()]
    df_num = clean_numbers(df_num)
    df_num = df_num[['dni', 'telefono', 'telefono_2']]
    df_num['telefono_2'] = df_num[df_num['telefono_2'].apply(len) >= 6]['telefono_2']
    df_num = df_num[df_num['telefono_2'].notna()]

    try:
        df_cuentas_subidas = pd.read_csv(osiris_accounts_file_path, encoding='latin_1', sep=';', dtype=str)
    except Exception:
        df_cuentas_subidas = pd.read_csv(osiris_accounts_file_path, encoding='ANSI', sep=';', dtype=str)

    df_cuentas_subidas = df_cuentas_subidas[['Cuenta', 'Mat. Unica']]\
        .rename(columns={'Mat. Unica': 'dni'}, inplace=False)

    df_numeros_cuentas = pd.merge(df_cuentas_subidas, df_num, how='inner', on='dni')

    df_subida[
        ['ID Cuenta o Nro. de Asig. (0)', "Nro. de Teléfono (18)"]] = df_numeros_cuentas[['Cuenta', 'telefono_2']]
    df_subida["ID Tipo de Teléfono (17)"] = 1
    print('Guardando planilla subida...')
    result_file_path = (
        ROOT_PATH / "Subida Osiris" /
        f'{datetime.now().strftime("(%H.%M hs) -")}DATOS_EMERIX_subida_telefono.csv'
    )
    try:
        df_subida.to_csv(
            result_file_path,
            sep=';',
            index=False,
            encoding='latin_1'
        )
    except Exception:
        df_subida.to_csv(
            result_file_path,
            sep=';',
            index=False,
            encoding='ANSI'
        )
    print('Guardado exitoso!')
    return result_file_path


class Interfaz_Usuario(Cmd):

    def do_CUENTAS(self, args):
        "Funcion para prepara la planilla de cuentas para subir nueva cartera"
        print('\n\nCOMENZANDO ARMADO DE PLANILLA DE CUENTAS\n')
        print('Preparando...')
        try:
            Preparacion_Cuentas()
            print('PROCESO FINALIZADO.\n\n')

        except Exception:
            error = traceback.format_exc()
            print(error)
            msg = f'Error durante preparacion planilla de CUENTAS.\n\n{error}'
            enviar_mail_con_adjuntos(USER, PASSWORD, PROGRAMMER, 'ERROR PROGRAMA SUBIDA CARTERA', msg)

    def do_DATOS(self, args):
        "Funcion para prepara la planilla de DATOS telefonos y mails"
        print('\n\nCOMENZANDO ARMADO DE PLANILLA DE DATOS\n')
        print('Preparando...')
        try:
            Preparacion_Datos()
            print('PROCESO FINALIZADO.\n\n')

        except Exception:
            error = traceback.format_exc()
            print(error)
            msg = f'Error durante preparacion planilla de DATOS.\n\n{error}'
            enviar_mail_con_adjuntos(USER, PASSWORD, PROGRAMMER, 'ERROR PROGRAMA SUBIDA CARTERA', msg)

    def do_AYUDA(self, args):
        'ofrece ayuda para los requesitos de funcionamiento'

        instrucciones = ''' El programa tiene 2 OBJETIVOS: Preparar la planilla de Cuentas y de datos.\n\n
        REQUERIMIENTOS PARA QUE EL PROGRAMA FUNCIONE CORRECTAMENTE.\n
        --------------------------------------------

        1. Para Preparacion PLANILLA DE CUENTAS de subida de cartera:
            - La CARTERA descargada de CR este guardada como "cr.csv" en la misma carpeta donde este este programa\n

        2. Para Preparacion PLANILLA DATOS (Telefonos y Mails). Se necesita:
            -  El Informe de Cuentas de la cartera recien subida se guarde como "cuentas.csv"
            en la misma carptea donde este programa\n

        3. Para Preparacion datos RIESGO ONLINE:
            - Planilla de riesgo guardada como "riesgo.csv" misma ubicacion que el programa
            - Cuentas de OSIRIS guardadas como "cuentas.csv" misma ubicacion que el programa\n

        4. Para Preparacion datos de INFO EXPERTO:
            - Planilla de riesgo guardada como "info.xlsx" misma ubicacion que el programa
            - Cuentas de OSIRIS guardadas como "cuentas.csv" misma ubicacion que el programa\n

        5. Para Preparacion SUBIDA CUENTAS COMAFI :
            - La CARTERA de emerix preparada por el pelado este guardada como "emerix.xlsx" (es un archivo excel)
            en la misma carpeta donde este este programa
            - Se pedira que INGRESE EL NOMBRE DE LA CARTERA  para guardado\n

        6. Para Preparacion PLANILLA DATOS (Telefonos y Mails). Se necesita:
            - La CARTERA de emerix preparada por el pelado este guardada como "emerix.xlsx" (es un archivo excel)
            en la misma carpeta donde este este programa
            - El Informe de Cuentas de la cartera recien subida
            se guarde como "cuentas.csv" en la misma carpeta donde este programa\n
        --------------------------------------------

        '''
        print(instrucciones)

    def do_INFO(self, args):
        "Funcion para prepara la planilla de DATOS telefonos y mails"
        print('\n\nCOMENZANDO PREPARACION DATOS INFO EXPERTO\n')
        print('Preparando...')

        try:
            GenerateDataInfo.process()
            print('PROCESO FINALIZADO.\n\n')
        except Exception:
            error = traceback.format_exc()
            print(error)
            msg = f'Error durante preparacion planilla de INFO EXPERTO.\n\n{error}'
            enviar_mail_con_adjuntos(USER, PASSWORD, PROGRAMMER, 'ERROR PROGRAMA SUBIDA CARTERA', msg)

    def do_RIESGO(self, args):
        "Funcion para prepara la planilla de DATOS telefonos y mails"
        print('\n\nCOMENZANDO PREPARACION DATOS RIESGO ONLINE\n')
        print('Preparando...')
        try:
            risk_data()
            print('PROCESO FINALIZADO.\n\n')

        except Exception:
            error = traceback.format_exc()
            print(error)
            msg = f'Error durante preparacion planilla de RIESGO ONLINE.\n\n{error}'
            enviar_mail_con_adjuntos(USER, PASSWORD, PROGRAMMER, 'ERROR PROGRAMA SUBIDA CARTERA', msg)

    def do_CUENTAS_COMAFI(self, args):
        try:
            Preparacion_Cuentas_Comafi()
            print('PROCESO FINALIZADO.\n\n')
        except Exception:
            error = traceback.format_exc()
            print(error)
            msg = f'Error durante preparacion planilla de SUBIDA CUENTAS COMAFI.\n\n{error}'
            enviar_mail_con_adjuntos(USER, PASSWORD, PROGRAMMER, 'ERROR PROGRAMA SUBIDA CARTERA CUENTAS COMAFI', msg)

    def do_DATOS_COMAFI(self, args):
        try:
            Preparacion_Datos_Comafi()
            print('PROCESO FINALIZADO.\n\n')
        except Exception:
            error = traceback.format_exc()
            print(error)
            msg = f'Error durante preparacion planilla de DATOS COMAFI.\n\n{error}'
            enviar_mail_con_adjuntos(USER, PASSWORD, PROGRAMMER, 'ERROR PROGRAMA SUBIDA DATOS COMAFI', msg)

    def default(self, args):
        print("Error. El comando \'" + args + "\' no existe")

    def precmd(self, args):

        if args.lower() == 'help':
            return args.lower()
        else:
            return args.upper()

    def do_EXIT(self, args):
        """Sale del programa"""
        print(''.center(70, '='))
        print("\n\nFINALIZANDO SISTEMA...")
        print(''.center(70, '-'))

        raise SystemExit


if __name__ == '__main__':

    # print(LOGO)
    interfaz = Interfaz_Usuario()
    interfaz.prompt = '>> '
    print(''.center(70, '-'))
    print('\n\t\tSUBIDA DE CARTERA\n')
    print(''.center(70, '='))
    comando = '''
        COMANDOS:
            - help : ver funciones disponibles (solo minuscula)
            - AYUDA: Requermientos para usar programa
            - EXIT: Salir del programa.
        \n(Se aceptan minusculas)
    '''
    print(comando)
    interfaz.cmdloop("\nIniciando consola de comandos...\n")
