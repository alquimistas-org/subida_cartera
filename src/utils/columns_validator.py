import pandas as pd


def column_validator(target_dataframe: pd.DataFrame, required_columns):
    try:
        assert target_dataframe.columns.values
    except AssertionError as e:
        print(e)
