
import os

import pandas as pd

from constants.constants import (
    DATA_UPLOADER_HEADER,
    ROOT_PATH,
)
from ports.dataframe_saver import DataFrameSaver


def Escribir_Datos_Osiris(
    df: pd.DataFrame,
    filename: str,
    cols_df: 'list[str]',
    cols_osiris: 'list[str]',
    dataframe_saver: DataFrameSaver,
) -> None:

    if there_is_not_saved_files_directory():
        raise Exception
    df_subida = pd.DataFrame(columns=DATA_UPLOADER_HEADER)
    df_subida[cols_osiris] = df[cols_df]
    dataframe_saver.save_df(filename, df_subida)


def there_is_not_saved_files_directory():
    return not os.path.isdir(ROOT_PATH / "Subida Osiris")
