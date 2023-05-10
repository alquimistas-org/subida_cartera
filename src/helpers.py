from pathlib import Path
import pandas as pd
from constants.constants import (
    OSIRIS_ACCOUNTS_FILE_PATH,
)


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


def read_osiris_accounts(osiris_accounts_file_path: Path = OSIRIS_ACCOUNTS_FILE_PATH) -> pd.DataFrame:
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
