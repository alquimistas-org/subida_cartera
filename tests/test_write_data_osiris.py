from freezegun import freeze_time
import pandas as pd
import pytest
import tempfile
from unittest import mock
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
            'RIESGO_telefonos.csv',
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

    @mock.patch('src.write_data_osiris.os.getenv')
    def test_create_file_in_existing_folder_get_by_env_variable(
        self,
        mock_get_env,
        mock_df,
        mock_filename,
        mock_cols_df,
        mock_cols_osiris,
    ):

        with tempfile.TemporaryDirectory() as tmpdirname:
            mock_get_env.return_value = tmpdirname
            Escribir_Datos_Osiris(
                df=mock_df,
                filename=mock_filename,
                cols_df=mock_cols_df,
                cols_osiris=mock_cols_osiris,
            )

    @freeze_time("2023-04-08 18:45:00")
    @mock.patch.object(pd.DataFrame, 'to_csv')
    def test_create_file_in_existing_folder_without_env_variable(
        self,
        mock_to_csv,
        mock_df,
        mock_filename,
        mock_cols_df,
        mock_cols_osiris,
    ):

        Escribir_Datos_Osiris(
            df=mock_df,
            filename=mock_filename,
            cols_df=mock_cols_df,
            cols_osiris=mock_cols_osiris,
        )

        mock_to_csv.assert_called_once()
        mock_to_csv.assert_called_once_with(
            f'{"Subida Osiris"}/(18.45 hs) - {mock_filename}',
            sep=';',
            index=False,
            encoding='latin_1'
        )

    @mock.patch('src.write_data_osiris.os.getenv')
    def test_raise_exception_folder_doesnt_exist(
        self,
        mock_get_env,
        mock_df,
        mock_filename,
        mock_cols_df,
        mock_cols_osiris,
    ):

        with pytest.raises(Exception):
            mock_get_env.return_value = "Another folder"
            Escribir_Datos_Osiris(
                df=mock_df,
                filename=mock_filename,
                cols_df=mock_cols_df,
                cols_osiris=mock_cols_osiris,
            )
