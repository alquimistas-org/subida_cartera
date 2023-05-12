import pandas as pd

from constants.constants import (
    DATA_UPLOADER_HEADER,
)
from ports.dataframe_saver import DataFrameSaver


def Escribir_Datos_Osiris(
        df: pd.DataFrame,
        name: str,
        cols_df: 'list[str]',
        cols_osiris: 'list[str]',
        dataframe_saver: DataFrameSaver,
        ):

    df_subida = pd.DataFrame(columns=DATA_UPLOADER_HEADER)
    df_subida[cols_osiris] = df[cols_df]

    dataframe_saver.save_df(name=name, df=df_subida)
