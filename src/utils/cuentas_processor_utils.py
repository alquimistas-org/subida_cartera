from datetime import date
import logging
import pandas as pd
from pathlib import Path
from typing import Union
from constants.constants import YEARS_TO_ADD
from ports.dataframe_saver import DataFrameSaver


# TODO considerer to rename it to wirte_df instead of write_csv
def write_csv(df_os: pd.DataFrame, dataframe_saver: DataFrameSaver) -> None:
    for name, df_sub in df_os.groupby('riesgo'):
        df_sub = df_sub.drop('riesgo', inplace=False, axis=1)
        dataframe_saver.save_df(name=name, df=df_sub)


def read_data(file_path: Union[str, Path]) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path, sep=';', encoding='latin_1', dtype=str)
    except Exception:
        logging.exception("Failed to read csv")
        return pd.read_csv(file_path, sep=';', encoding='ANSI', dtype=str)


def create_date(year_to_add: int = 0) -> date:
    if year_to_add < 0:
        raise ValueError
    date_now = date.today()
    return date_now.replace(year=date_now.year + year_to_add).strftime('%d/%m/%Y')


def process_cuentas(
        cr: pd.DataFrame,
        fields_processor: dict,
        df_columns: list[str],
        ) -> pd.DataFrame:

    df_os = pd.DataFrame(columns=df_columns)

    df_os['Nº de Asignacion (0)'] = fields_processor['Nº de Asignacion (0)'](cr)
    df_os['Razon social (1)'] = fields_processor['Razon social (1)'](cr)
    df_os['ID Tipo de Documento (2)'] = fields_processor['ID Tipo de Documento (2)']
    df_os['DNI (3)'] = fields_processor['DNI (3)'](cr)
    df_os['Domicilio (4)'] = fields_processor['Domicilio (4)'](cr)
    df_os['ID Localidad (5)'] = fields_processor['ID Localidad (5)']
    df_os['ID Provincia (6)'] = fields_processor['ID Provincia (6)'](cr)
    df_os['Código Postal (7)'] = fields_processor['Código Postal (7)'](cr)
    df_os['Importe Asignado (11)'] = fields_processor['Importe Asignado (11)'](cr)
    df_os['Fecha de Ingreso (12)'] = create_date()
    df_os['Fecha de Deuda dd/mm/aaaa (13)'] = fields_processor['Fecha de Deuda dd/mm/aaaa (13)'](cr)
    df_os['Importe Historico (14)'] = fields_processor['Importe Historico (14)'](cr)
    df_os['Observaciones (15)'] = fields_processor['Observaciones (15)'](cr)
    df_os['Fecha Fin de Gestion (16)'] = create_date(YEARS_TO_ADD)
    df_os['IDSucursal(17)'] = fields_processor['IDSucursal(17)']
    df_os['riesgo'] = fields_processor['riesgo'](cr)

    return df_os
