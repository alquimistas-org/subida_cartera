
import pandas as pd
import time
from constants.constants import DATA_UPLOADER_HEADER


def Escribir_Datos_Osiris(df, filename, cols_df, cols_osiris):

    Control_Carpeta_Subida()

    df_subida = pd.DataFrame(columns=DATA_UPLOADER_HEADER)
    df_subida[cols_osiris] = df[cols_df]
    try:
        df_subida.to_csv(
            f'Subida Osiris/{time.strftime("(%H.%M hs) -")} {filename}',
            sep=';',
            index=False,
            encoding='latin_1'
        )
    except Exception:
        df_subida.to_csv(
            f'Subida Osiris/{time.strftime("(%H.%M hs) -")} {filename}',
            sep=';',
            index=False,
            encoding='ANSI'
        )


def Control_Carpeta_Subida():
    'COntrola que exista una carpeta llamada Subida Osiris y sino la crea'
    pass
    # no la estoy usando
