from freezegun import freeze_time
import os
from pathlib import Path
import tempfile
from unittest import mock

import pandas as pd
import pytest

from src.adapters.file_dataframe_saver import FileDataFrameSaver
from src.write_data_osiris import Escribir_Datos_Osiris


@pytest.mark.parametrize("mock_df, mock_filename, mock_cols_df, mock_cols_osiris", [
        (
            pd.DataFrame(
                    {
                        "Cuenta": "3333",
                        "TEL": '123455678',
                        "OBS": "RIESGO 1",
                        "ID_FONO": "8",
                    },
                    index=[0]
                ),
            'RIESGO_telefonos',
            ['Cuenta', 'ID_FONO', 'TEL', 'OBS'],
            [
                "ID Cuenta o Nro. de Asig. (0)",
                "ID Tipo de Teléfono (17)",
                "Nro. de Teléfono (18)",
                "Obs. de Teléfono (19)"
            ]
        )
    ]
)
class TestWriteDataOsiris:

    @freeze_time("2023-04-08 18:45:00")
    def test_create_file_in_existing_folder_get_by_env_variable(
        self,
        mock_df,
        mock_filename,
        mock_cols_df,
        mock_cols_osiris,
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            saver = FileDataFrameSaver(output_path=Path(tmpdir))
            Escribir_Datos_Osiris(
                    df=mock_df,
                    filename=mock_filename,
                    cols_df=mock_cols_df,
                    cols_osiris=mock_cols_osiris,
                    dataframe_saver=saver,
                )
            filename = os.listdir(tmpdir)
            assert filename == ['(18.45 hs) - ' + mock_filename + '.csv']

    @mock.patch('src.write_data_osiris.there_is_not_saved_files_directory')
    def test_raise_exception_folder_doesnt_exist(
        self,
        mock_there_is_not_saved_files_directory,
        mock_df,
        mock_filename,
        mock_cols_df,
        mock_cols_osiris,
    ):
        mock_there_is_not_saved_files_directory.return_value = True
        with pytest.raises(Exception):
            Escribir_Datos_Osiris(
                df=mock_df,
                filename=mock_filename,
                cols_df=mock_cols_df,
                cols_osiris=mock_cols_osiris,
            )
