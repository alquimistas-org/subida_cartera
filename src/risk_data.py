import io
from pathlib import Path
from typing import Union

import pandas as pd

from constants.constants import (
    NUMBER_OF_COLUMNS,
    OSIRIS_ACCOUNTS_FILE_PATH,
    RISK_FILE_PATH,
)
from helpers import (
    get_phones,
    read_osiris_accounts,
)
from src.adapters.file_dataframe_saver import FileDataFrameSaver
from src.constants.constants import ROOT_PATH
from src.ports.dataframe_saver import DataFrameSaver
from write_data_osiris import Escribir_Datos_Osiris


def risk_data(
    risk_file_path: Union[Path, io.BytesIO] = RISK_FILE_PATH,
    osiris_accounts_file_path: Union[Path, io.BytesIO] = OSIRIS_ACCOUNTS_FILE_PATH,
    dataframe_saver: DataFrameSaver = None,
) -> None:

    if not dataframe_saver:
        dataframe_saver = FileDataFrameSaver(output_path=ROOT_PATH / 'Subida Osiris/')

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

    Escribir_Datos_Osiris(
        df_phone_risk,
        'RIESGO_telefonos.csv',
        ['Cuenta', 'ID_FONO', 'TEL', 'OBS'],
        [
            "ID Cuenta o Nro. de Asig. (0)",
            "ID Tipo de Teléfono (17)",
            "Nro. de Teléfono (18)",
            "Obs. de Teléfono (19)"
        ],
        dataframe_saver=dataframe_saver
    )
    print('Planilla de Teléfonos de RIESGO escrita')
