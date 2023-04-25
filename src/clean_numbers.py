import numpy as np
import pandas as pd


def clean_numbers(df_num: pd.DataFrame) -> pd.DataFrame:
    with_double_dash = df_num['telefono'].str.contains('--')
    without_double_dash = ~ with_double_dash
    with_054 = df_num['telefono'].str.contains('(054)', regex=False)
    with_dash_1 = df_num['telefono'].str.contains('-1-', regex=False)

    df_num['telefono_2'] = np.nan

    # cleaning those with 11 011 y 0
    number_concatenate = df_num[without_double_dash & with_054 & ~with_dash_1]['telefono'].str.split('-', expand=True)
    if not number_concatenate.empty:
        df_num.loc[without_double_dash & with_054 & ~with_dash_1, 'telefono_2'] = (
            number_concatenate[1] + number_concatenate[2]
            )\
            .str.replace(r'^[0]+', '', regex=True)\
            .str.replace(r'^[54]+', '', regex=True)\
            .str.replace(r'^[0]+', '', regex=True)

    # cleaning those with -1- in the middle
    with_1_in_between = without_double_dash & with_054 & with_dash_1
    number_concatenate = df_num[with_1_in_between]['telefono'].str.split('-', expand=True)
    if not number_concatenate.empty:
        df_num.loc[with_1_in_between, 'telefono_2'] = number_concatenate[2]\
            .str.replace(r'^[0]+', '', regex=True)\
            .str.replace(r'^[54]+', '', regex=True)\
            .str.replace(r'^[0]+', '', regex=True)

    # cleaning double dash
    number_concatenate = df_num[with_double_dash]['telefono'].str.split('--', expand=True)
    if not number_concatenate.empty:
        df_num.loc[with_double_dash, 'telefono_2'] = number_concatenate[1]\
            .str.replace(r'^[0]+', '', regex=True)\
            .str.replace(r'^[54]+', '', regex=True)\
            .str.replace(r'^[0]+', '', regex=True)

    # remaining empty numbers
    remaining_empty = df_num['telefono_2'].isna()
    df_num.loc[remaining_empty, 'telefono_2'] = df_num[remaining_empty]['telefono']\
        .str.replace(r'[^\d]+', '').str.replace(r'^[0]+', '', regex=True)\
            .str.replace(r'^[54]+', '', regex=True).str.replace(r'^[0] + ', '', regex=True)

    return df_num
