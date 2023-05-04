import pandas as pd
from datetime import datetime
from pathlib import Path


class FileDataFrameSaver:

    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.saved_dfs: dict[str, pd.DataFrame] = {}
        self.saved_files: dict[str, Path] = {}

    def save_df(self, name: str, df: pd.DataFrame) -> None:
        print(f'Ecribiendo: subida_cartera_{name}.csv')

        df = df.drop('riesgo', inplace=False, axis=1)

        result_file_path = self.output_path / f'{datetime.now().strftime("(%H.%M hs) -")} subida_cartera_{name}.csv'

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
