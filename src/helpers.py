import io
from pathlib import Path
from typing import Union

import pandas as pd

from clean_numbers import clean_numbers
from constants.constants import CR_FILE_PATH, DATA_PREP_COLUMNS


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


def read_osiris_accounts(osiris_accounts_file_path: Union[Path, io.BytesIO]) -> pd.DataFrame:
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


def read_cr_data(cr_file_path: Path = CR_FILE_PATH, columns_to_use: list = DATA_PREP_COLUMNS) -> pd.DataFrame:
    try:
        cr = pd.read_csv(cr_file_path, sep=';', encoding='latin_1', dtype=str)
    except Exception:
        cr = pd.read_csv(cr_file_path, sep=';', encoding='ANSI', dtype=str)

    df_cr = cr[columns_to_use].rename(columns={'NRODOC': 'DNI'}, inplace=False).copy()
    return df_cr


def process_phone_numbers(file_path: Path, cols: dict[str, str]) -> pd.DataFrame:
    df_num = pd.read_excel(file_path, dtype=str)
    df_num = df_num[list(cols.keys())]
    df_num = df_num.rename(columns=cols)
    df_num = df_num[df_num['telefono'].notna()]
    df_num = clean_numbers(df_num)
    df_num = df_num[['dni', 'telefono', 'telefono_2']]
    df_num['telefono_2'] = df_num[df_num['telefono_2'].apply(len) >= 6]['telefono_2']
    df_num = df_num[df_num['telefono_2'].notna()]

    return df_num
