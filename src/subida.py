from cmd import Cmd
import os
import shutil
import pandas as pd
import numpy as np
from datetime import datetime, date
import traceback

from driver_email import enviar_mail_con_adjuntos
from constants.constants import (
    ACCOUNT_PREP_COL,
    CR_FILE_PATH,
    DATA_PREP_COLUMNS,
    EMERIX_FILE_PATH,
    PASSWORD,
    PROGRAMMER,
    PROVINCES,
    ROOT_PATH,
    USER,
    UTIL_COLS_COMAFI,
)
from risk_data import risk_data
from data_info import GenerateDataInfo
from write_data_osiris import Escribir_Datos_Osiris


def limpiar_numeros(df_num):
    con_doble_guion = df_num['telefono'].str.contains('--')
    sin_doble_guion = ~ con_doble_guion
    con_054 = df_num['telefono'].str.contains('(054)', regex=False)
    con_guion_1 = df_num['telefono'].str.contains('-1-', regex=False)

    df_num['telefono_2'] = np.nan
    # limpiando los que tienen 11 011 y 0
    numeros_concatenar = df_num[sin_doble_guion & con_054 & ~con_guion_1]['telefono'].str.split('-', expand=True)
    df_num.loc[sin_doble_guion & con_054 & ~con_guion_1, 'telefono_2'] = (
        numeros_concatenar[1] + numeros_concatenar[2]
        )\
        .str.replace(r'^[0]+', '', regex=True)\
        .str.replace(r'^[54]+', '', regex=True)\
        .str.replace(r'^[0]+', '', regex=True)

    # limpieza de los que tiene -1- en medio
    con_1_medio = sin_doble_guion & con_054 & con_guion_1
    df_num.loc[con_1_medio, 'telefono_2'] = df_num[con_1_medio]['telefono'].str.split('-', expand=True)[2]\
        .str.replace(r'^[0]+', '', regex=True)\
        .str.replace(r'^[54]+', '', regex=True)\
        .str.replace(r'^[0]+', '', regex=True)

    # limpieza numeros CON DOBLE GUION
    df_num.loc[con_doble_guion, 'telefono_2'] = df_num[con_doble_guion]['telefono'].str.split('--', expand=True)[1]\
        .str.replace(r'^[0]+', '', regex=True)\
        .str.replace(r'^[54]+', '', regex=True)\
        .str.replace(r'^[0]+', '', regex=True)

    # resto de los numeros que quedaron vacios
    vacios = df_num['telefono_2'].isna()
    df_num.loc[vacios, 'telefono_2'] = df_num[vacios]['telefono']\
        .str.replace(r'[^\d]+', '').str.replace(r'^[0]+', '', regex=True)\
            .str.replace(r'^[54]+', '', regex=True).str.replace(r'^[0] + ', '', regex=True)

    return df_num


def Preparacion_Cuentas(cr_file_path=CR_FILE_PATH) -> list:

    "Condiciones"

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
    df_os['Importe Asignado (11)'] = cr['DEUDA_ACTUALIZADA'].str.replace(', ', '.')
    df_os['Fecha de Ingreso (12)'] = date_1
    df_os['Fecha de Deuda dd/mm/aaaa (13)'] = cr['INICIOMORA']
    df_os['Importe Historico (14)'] = cr['CAPITAL'].str.replace(', ', '.')
    df_os['Observaciones (15)'] = (
        'Gestor anterior: ' + cr['GESTOR_ANTERIOR'] + ' - ' + 'Score: ' +
        cr['SCORE'].str.replace(', ', '.').str.replace(',', '.').astype(float).round(2).astype(str)
    )
    df_os['Fecha Fin de Gestion (16)'] = date_2
    df_os['IDSucursal(17)'] = '1'
    df_os['riesgo'] = cr['RIESGO']

    all_result_file_path = list()
    for name, df_sub in df_os.groupby('riesgo'):

        print(f'Ecribiendo: subida_cartera_{name}.csv')
        df_sub = df_sub.drop('riesgo', inplace=False, axis=1)

        result_file_path = (
            ROOT_PATH / f'Subida Osiris/{datetime.now().strftime("(%H.%M hs) -")} subida_cartera_{name}.csv'
        )

        try:
            df_sub.to_csv(
                result_file_path,
                sep=';',
                encoding='latin_1',
                index=False
            )
        except Exception:
            df_sub.to_csv(
                result_file_path,
                sep=';',
                encoding='ANSI',
                index=False
            )
        all_result_file_path.append(result_file_path)
    return all_result_file_path


def Preparacion_Cuentas_Comafi(emerix_file_path=EMERIX_FILE_PATH):

    nombre_cartera = input('\nIngrese el nombre de la cartera que desea:  ')

    print('Iniciando preparacion')
    # lectura planilla modelo
    try:
        df_os = pd.read_csv('modelos/modelo_cuentas.csv', encoding='latin_1', sep=';')
    except Exception:
        df_os = pd.read_csv('modelos/modelo_cuentas.csv', encoding='ANSI', sep=';')
    df = pd.read_excel(emerix_file_path, dtype=str)
    col_utiles = UTIL_COLS_COMAFI
    provincias = PROVINCES

    df = df[list(col_utiles.keys())]
    df = df.rename(columns=col_utiles)

    # reemplazo de valores nulos
    df.loc[df['provincia'].isna(), 'provincia'] = '0'
    # reemplazo de 'ñ' en nombres
    caracteres = ['#', 'Ð', 'ð', '&']
    for car in caracteres:
        n = df['nombre'].str.contains(car).sum()
        df['nombre'] = df['nombre'].str.replace(car, 'ñ').str.title()
        # n = df['nombre'].str.contains(car).sum()
        print(f'Caracter {car}: se remplazaron {n}')
    print('\n')
    print('\nComenzando escritura de archivos..\n\n')

    date_now = date.today()
    years_to_add = date_now.year + 3

    date_1 = date_now.strftime('%d/%m/%Y')
    date_2 = date_now.replace(year=years_to_add).strftime('%d/%m/%Y')

    df_os['Nº de Asignacion (0)'] = df['dni']
    df_os['Razon social (1)'] = df['nombre']
    df_os['ID Tipo de Documento (2)'] = '1'
    df_os['DNI (3)'] = df['dni']

    df_os['Domicilio (4)'] = df['direccion'] + ' - ' + df['localidad']
    df_os['ID Localidad (5)'] = '0'

    df_os['ID Provincia (6)'] = df['provincia'].apply(lambda fila: provincias[fila])
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

    name_folder = ROOT_PATH / f'Subida Osiris/{datetime.now().strftime("(%H.%M hs) -")} {nombre_cartera}'
    if os.path.isdir(name_folder):
        shutil.rmtree(name_folder)
    os.mkdir(name_folder)
    # iterear un loop por los subcliente a traves de un grouby
    for name, df_sub in df_os.groupby('subcliente'):
        print(f'Ecribiendo: {name}.csv')
        df_sub = df_sub.drop('subcliente', inplace=False, axis=1)
        try:
            df_sub.to_csv(f'{name_folder}/{name}.csv', sep=';', encoding='latin_1', index=False)
        except Exception:
            df_sub.to_csv(f'{name_folder}/{name}.csv', sep=';', encoding='ANSI', index=False)

    return name_folder


def Preparacion_Datos():
    ' Necesita que este en la carpeta'
    print('Preparando planillas de datos...')
    try:
        cr = pd.read_csv('cr.csv', sep=';', encoding='latin_1', dtype=str)
        cuentas_subidas = pd.read_csv('cuentas.csv', encoding='latin_1', sep=';', dtype=str)
    except Exception:
        cr = pd.read_csv('cr.csv', sep=';', encoding='ANSI', dtype=str)
        cuentas_subidas = pd.read_csv('cuentas.csv', encoding='ANSI', sep=';', dtype=str)

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
    df_tels.to_csv('prueba_2.csv', index=False, sep=';')
    df_tels = df_tels.astype({'TEL': 'Int64'})
    df_tels = df_tels.astype({'TEL': 'str'})
    df_tels.drop(df_tels[df_tels.TEL == '0'].index, inplace=True)

    Escribir_Datos_Osiris(
        df_tels,
        'DATOS_CR_subida_telefonos.csv',
        ['Cuenta', 'ID_FONO', 'TEL'],
        ['ID Cuenta o Nro. de Asig. (0)', "ID Tipo de Teléfono (17)", "Nro. de Teléfono (18)"]
    )
    print(f'{len(df_tels)} TELEFONOS se guardaron en archivo: subida_telefono.csv')
    # reemplazar cualquier caractaer alfabetico que este dentro del numero para evitar roblema en futuro
    # borrar numero cero
    df_cr.loc[df_cr['EMAIL'].notnull(), 'EMAIL'] = df_cr.loc[df_cr['EMAIL'].notnull(), 'EMAIL'].str.replace(' ', '')
    df_mail = df_cr.loc[df_cr['EMAIL'].notnull(), ['Cuenta', 'EMAIL']].copy()
    Escribir_Datos_Osiris(
        df_mail,
        'DATOS_CR_subida_mail.csv',
        ['Cuenta', 'EMAIL'],
        ['ID Cuenta o Nro. de Asig. (0)', "Email (16)"]
    )
    print(f'{len(df_mail)} MAILS se guardaron en archivo: subida_mail.csv\n\n')


def Preparacion_Datos_Comafi():

    print('Preparando planillas de datos para comafi...')
    try:
        df_subida = pd.read_csv('modelos/modelo_datos.csv', encoding='latin_1', sep=';')
    except Exception:
        df_subida = pd.read_csv('modelos/modelo_datos.csv', encoding='ANSI', sep=';')

    df_num = pd.read_excel('emerix.xlsx', dtype=str)
    col_utiles = UTIL_COLS_COMAFI
    df_num = df_num[list(col_utiles.keys())]
    df_num = df_num.rename(columns=col_utiles)
    df_num = df_num[df_num['telefono'].notna()]
    df_num = limpiar_numeros(df_num)
    df_num = df_num[['dni', 'telefono', 'telefono_2']]
    df_num['telefono_2'] = df_num[df_num['telefono_2'].apply(len) >= 6]['telefono_2']
    df_num = df_num[df_num['telefono_2'].notna()]

    try:
        df_cuentas_subidas = pd.read_csv('cuentas.csv', encoding='latin_1', sep=';', dtype=str)
    except Exception:
        df_cuentas_subidas = pd.read_csv('cuentas.csv', encoding='ANSI', sep=';', dtype=str)

    df_cuentas_subidas = df_cuentas_subidas[['Cuenta', 'Mat. Unica']]\
        .rename(columns={'Mat. Unica': 'dni'}, inplace=False)

    df_numeros_cuentas = pd.merge(df_cuentas_subidas, df_num, how='inner', on='dni')
    try:
        df_numeros_cuentas.to_csv('verificacion.csv', sep=';', encoding='latin_1', index=False)
    except Exception:
        df_numeros_cuentas.to_csv('verificacion.csv', sep=';', encoding='ANSI', index=False)
    df_subida[
        ['ID Cuenta o Nro. de Asig. (0)', "Nro. de Teléfono (18)"]] = df_numeros_cuentas[['Cuenta', 'telefono_2']]
    df_subida["ID Tipo de Teléfono (17)"] = 1
    print('Guardando planilla subida...')
    try:
        df_subida.to_csv(
            f'Subida Osiris/{datetime.now().strftime("(%H.%M hs) -")}DATOS_EMERIX_subida_telefono.csv',
            sep=';',
            index=False,
            encoding='ANSI'
        )
    except Exception:
        df_subida.to_csv(
            f'Subida Osiris/{datetime.now().strftime("(%H.%M hs) -")}DATOS_EMERIX_subida_telefono.csv',
            sep=';',
            index=False,
            encoding='ANSI'
        )
    print('Guardado exitoso!')


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
