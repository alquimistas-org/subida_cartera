
from datetime import datetime
import os

import pandas as pd
from constants.constants import (
    DATA_UPLOADER_HEADER,
    ROOT_PATH,
)


def Escribir_Datos_Osiris(df: pd.DataFrame, filename: str, cols_df: 'list[str]', cols_osiris: 'list[str]'):

    if there_is_not_saved_files_directory():
        raise Exception
    result_file_path = ROOT_PATH / "Subida Osiris" / f'{datetime.now().strftime("(%H.%M hs) -")} {filename}'
    df_subida = pd.DataFrame(columns=DATA_UPLOADER_HEADER)
    df_subida[cols_osiris] = df[cols_df]
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
    return result_file_path


def there_is_not_saved_files_directory():
    return not os.path.isdir(ROOT_PATH / "Subida Osiris")
