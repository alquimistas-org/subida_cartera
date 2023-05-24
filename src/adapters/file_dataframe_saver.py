import pandas as pd
from datetime import datetime
from pathlib import Path


class FileDataFrameSaver:

    def __init__(self, output_path: Path, portfolio_name: str = None) -> None:
        self.output_path = output_path
        self.saved_dfs: dict[str, pd.DataFrame] = {}
        self.saved_files: dict[str, Path] = {}
        self.portfolio_name = portfolio_name

    def save_df(self, name: str, df: pd.DataFrame) -> None:
        print(f'Ecribiendo: subida_cartera_{name}.csv')

        result_file_path = (
            self.output_path /
            f'{datetime.now().strftime("(%H.%M hs) - ")}'
            f'{ f"{self.portfolio_name}_" if self.portfolio_name else ""}'
            f'{name}{"" if name.endswith(".csv") else ".csv"}'
        )

        try:
            df.to_csv(
                result_file_path,
                sep=';',
                encoding='latin_1',
                index=False
            )
        except Exception:
            df.to_csv(
                result_file_path,
                sep=';',
                encoding='ANSI',
                index=False
            )

        self.saved_dfs[name] = df
        self.saved_files[name] = result_file_path

    def get_saved_dfs(self) -> dict[str, pd.DataFrame]:
        return self.saved_dfs

    def get_saved_files(self) -> dict[str, Path]:
        return self.saved_files
