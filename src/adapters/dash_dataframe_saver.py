import pandas as pd


class DashDataFrameSaver:

    def __init__(self) -> None:
        self.saved_dfs: dict[str, pd.DataFrame] = {}

    def save_df(self, name: str, df: pd.DataFrame) -> None:
        self.saved_dfs[name] = df

    def get_saved_dfs(self) -> dict[str, pd.DataFrame]:
        return self.saved_dfs
