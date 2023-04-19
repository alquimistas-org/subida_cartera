
from datetime import datetime
import os
import pandas as pd
from constants.constants import DATA_UPLOADER_HEADER


def Escribir_Datos_Osiris(df: pd.DataFrame, filename: str, cols_df: 'list[str]', cols_osiris: 'list[str]'):

    Control_Carpeta_Subida()
    result_file_path = (
        f'{os.getenv("file_directory", "Subida Osiris")}/{datetime.now().strftime("(%H.%M hs) -")} {filename}'
    )
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


def Control_Carpeta_Subida():
    'COntrola que exista una carpeta llamada Subida Osiris y sino la crea'
    pass
    # no la estoy usando
