from cmd import Cmd
import io
import traceback
from typing import Union
import logging
import pandas as pd

from adapters.file_dataframe_saver import FileDataFrameSaver
from data_info import GenerateDataInfo
from data_naranja import GenerateDataNaranja
from driver_email import enviar_mail_con_adjuntos
from constants.constants import (
    ACCOUNT_PREP_COL,
    CR_FILE_PATH,
    CR_REQUIRED_FIELDS,
    DATA_MODEL_CSV_PATH,
    EMERIX_FILE_PATH,
    OSIRIS_ACCOUNTS_FILE_PATH,
    PASSWORD,
    PROGRAMMER,
    ROOT_PATH,
    USER,
    UTIL_COLS_COMAFI,
)
from risk_data import risk_data
from helpers import process_phone_numbers
from prepare_comafi_accounts import prepare_comafi_accounts
from ports.dataframe_saver import DataFrameSaver
from process_preparacion_cuentas import NARANJA_FIELDS
from utils.cuentas_processor_utils import (
    write_csv,
    read_data,
    process_cuentas
)
from validations.validations import (
    validate_columns,
    IncorrectColumnsError,
)


def Preparacion_Cuentas(
    cr_file_path: Union[str, io.BytesIO, io.StringIO] = CR_FILE_PATH,
    dataframe_saver: DataFrameSaver = None,
) -> None:

    if not dataframe_saver:
        dataframe_saver = FileDataFrameSaver(output_path=ROOT_PATH / 'Subida Osiris/', portfolio_name='subida_cartera')

    try:
        cr = read_data(cr_file_path)
        validate_columns(cr, CR_REQUIRED_FIELDS)
        df_os = process_cuentas(cr, NARANJA_FIELDS, ACCOUNT_PREP_COL)
        write_csv(df_os, dataframe_saver)
    except IncorrectColumnsError as e:
        print(e.message)
        logging.exception(e.message)
        return e.message
    except Exception as e:
        error_message = traceback.format_exc()
        print(error_message)
        print(f"Error: {e}")
        logging.exception("Failed read csv")
        return


def Preparacion_Datos_Comafi(
        emerix_file_path: Union[str, io.BytesIO, io.StringIO] = EMERIX_FILE_PATH,
        osiris_accounts_file_path: Union[str, io.BytesIO, io.StringIO] = OSIRIS_ACCOUNTS_FILE_PATH,
        dataframe_saver: DataFrameSaver = None,
        data_models=DATA_MODEL_CSV_PATH,
        ):
    if not dataframe_saver:
        dataframe_saver = FileDataFrameSaver(output_path=ROOT_PATH / 'Subida Osiris/')

    print('Preparando planillas de datos para comafi...')  # TODO: remove print statements when deleted CMD

    df_subida = read_data(file_path=data_models)

    df_num = process_phone_numbers(file_path=emerix_file_path, cols=UTIL_COLS_COMAFI)

    df_cuentas_subidas = read_data(file_path=osiris_accounts_file_path)
    df_cuentas_subidas = df_cuentas_subidas[['Cuenta', 'Mat. Unica']]\
        .rename(columns={'Mat. Unica': 'dni'}, inplace=False)

    df_numeros_cuentas = pd.merge(df_cuentas_subidas, df_num, how='inner', on='dni')

    df_subida[
        ['ID Cuenta o Nro. de Asig. (0)', "Nro. de Teléfono (18)"]] = df_numeros_cuentas[['Cuenta', 'telefono_2']]
    df_subida["ID Tipo de Teléfono (17)"] = 1

    print('Guardando planilla subida...')

    dataframe_saver.save_df(name="DATOS_EMERIX_subida_telefono", df=df_subida)

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
            GenerateDataNaranja.process()
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
            portfolio_name = input('\nIngrese el nombre de la cartera que desea:  ')
            prepare_comafi_accounts(portfolio_name=portfolio_name)
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
