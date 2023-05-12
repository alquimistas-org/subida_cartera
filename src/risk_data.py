import pandas as pd

from adapters.file_dataframe_saver import FileDataFrameSaver
from constants.constants import (
    NUMBER_OF_COLUMNS,
    OSIRIS_ACCOUNTS_FILE_PATH,
    RISK_FILE_PATH,
    ROOT_PATH,
)
from helpers import (
    get_phones,
    read_osiris_accounts,
)
from ports.dataframe_saver import DataFrameSaver
from write_data_osiris import Escribir_Datos_Osiris


def risk_data(
        risk_file_path=RISK_FILE_PATH,
        osiris_accounts_file_path=OSIRIS_ACCOUNTS_FILE_PATH,
        dataframe_saver: DataFrameSaver = None,
        ) -> str:

    if not dataframe_saver:
        dataframe_saver = FileDataFrameSaver(output_path=ROOT_PATH / 'Subida Osiris/', portfolio_name='subida_cartera')

    'NECESARIOS: tener el archivos.csv de riesgo y el archivo de las cuentas de osiris como cuentas.csv'
    col_numbers = {
        'NÃºmero.1': 'tel_riesgo_1',
        'NÃºmero.2': 'tel_riesgo_2',
        'NÃºmero.3': 'tel_riesgo_3',
        'NÃºmero.4': 'tel_riesgo_4'
    }

    col_list = [x for x in range(NUMBER_OF_COLUMNS)]
    try:
        risk = pd.read_csv(risk_file_path, sep=';', encoding='latin_1', dtype=str, index_col=False, usecols=col_list)
    except Exception:
        risk = pd.read_csv(risk_file_path, sep=';', encoding='ANSI', dtype=str, index_col=False, usecols=col_list)
    df_risk = risk[['DNI'] + list(col_numbers.keys()) + ['NSE']]

    df_risk = df_risk.rename(columns=col_numbers, inplace=False)

    uploaded_accounts = read_osiris_accounts(osiris_accounts_file_path)

    df_risk = pd.merge(uploaded_accounts, df_risk, how="inner", on="DNI")

    num_tel = len([col_name for col_name in list(df_risk.columns) if 'tel_riesgo' in col_name])
    df_phone_risk = get_phones(
        df=df_risk,
        stop=num_tel+1,
        colum_name='RIESGO'
        )

    result_file_path = Escribir_Datos_Osiris(
        df_phone_risk,
        'RIESGO_telefonos',
        ['Cuenta', 'ID_FONO', 'TEL', 'OBS'],
        [
            "ID Cuenta o Nro. de Asig. (0)", "ID Tipo de Teléfono (17)",
            "Nro. de Teléfono (18)", "Obs. de Teléfono (19)",
        ],
        dataframe_saver,
    )
    print('Planilla de Teléfonos de RIESGO escrita')
    return result_file_path
