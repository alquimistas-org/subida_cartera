from pathlib import Path
import pandas as pd
from constants.constants import NUMBER_OF_COLUMNS
from constants.constants import (
    OSIRIS_ACCOUNTS_FILE_PATH,
    RISK_FILE_PATH,
)
from write_data_osiris import Escribir_Datos_Osiris


def get_phones(df: pd.DataFrame, stop: int, colum_name: str) -> pd.DataFrame:
    df_copy = df.copy()
    frames = list()
    for i in range(1, stop):
        col = f'tel_{colum_name.lower()}_{i}'
        new_df = df_copy.loc[df_copy[col].notnull(), ['Cuenta', col]]\
            .rename(columns={col: 'TEL'}).copy()
        new_df['OBS'] = f'{colum_name} {i}'
        new_df['ID_FONO'] = '8'
        frames.append(new_df)
    df_phones = pd.concat(frames, ignore_index=True)
    return df_phones

# TODO: in other PR move this function to another file for helper functions or similar


def read_osiris_accounts(osiris_accounts_file_path: Path) -> pd.DataFrame:
    try:
        uploaded_accounts = pd.read_csv(osiris_accounts_file_path, encoding='latin_1', sep=';', dtype=str)
    except Exception:
        uploaded_accounts = pd.read_csv(osiris_accounts_file_path, encoding='ANSI', sep=';', dtype=str)
    uploaded_accounts = uploaded_accounts[['Cuenta', 'Mat. Unica']].rename(
        columns={
            'Mat. Unica': 'DNI'
            },
        inplace=False
        )
    return uploaded_accounts

# TODO: in other PR move this function to another file for helper functions or similar


def risk_data(risk_file_path=RISK_FILE_PATH, osiris_accounts_file_path=OSIRIS_ACCOUNTS_FILE_PATH) -> str:
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

    df_phone_risk = get_phones(df=df_risk)

    result_file_path = Escribir_Datos_Osiris(
        df_phone_risk,
        'RIESGO_telefonos.csv',
        ['Cuenta', 'ID_FONO', 'TEL', 'OBS'],
        ["ID Cuenta o Nro. de Asig. (0)", "ID Tipo de Teléfono (17)", "Nro. de Teléfono (18)", "Obs. de Teléfono (19)"]
    )
    print('Planilla de Teléfonos de RIESGO escrita')
    return result_file_path
