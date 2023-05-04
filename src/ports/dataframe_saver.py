from typing import Protocol
import pandas as pd


class DataFrameSaver(Protocol):

    def save_df(self, name: str, df: pd.DataFrame) -> None:
        ...

    def get_saved_dfs(self) -> dict[str, pd.DataFrame]:
        ...
