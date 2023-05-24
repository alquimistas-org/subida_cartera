from pathlib import Path
import tempfile
from unittest import mock

import pandas as pd

from src.adapters.file_dataframe_saver import FileDataFrameSaver
from src.risk_data import risk_data


class TestRiskData:

    @mock.patch("pandas.read_csv")
    @mock.patch("pandas.merge")
    @mock.patch("src.risk_data.read_osiris_accounts")
    @mock.patch("src.risk_data.get_phones")
    @mock.patch("src.risk_data.Escribir_Datos_Osiris")
    def test_risk_data(
        self,
        mock_Escribir_Datos_Osiris,
        mock_get_phones,
        mock_read_osiris_accounts,
        mock_merge,
        mock_read_csv,
    ):

        mock_read_csv.return_value = pd.DataFrame({
            "NÃºmero.1": "122233334",
            "NÃºmero.2": "334444556",
            "NÃºmero.3": "122233334",
            "NÃºmero.4": "122233334",
            "Cuenta": "1234",
            "DNI": "23345",
            "NSE": "",
            },
            index=[0]
        )
        mock_read_osiris_accounts.return_value = pd.DataFrame({
            "Cuenta": "1234",
            "Mat. Unica": "23345"
            },
            index=[0]
        )
        mock_merge.return_value = pd.DataFrame({
            "tel_riesgo_1": "122233334",
            "tel_riesgo_2": "334444556",
            "tel_riesgo_3": "122233334",
            "tel_riesgo_4": "122233334",
            "Cuenta": "1234",
            "DNI": "23345",
            "NSE": "",
            },
            index=[0]
        )
        mock_get_phones.return_value = pd.DataFrame({
            "Cuenta": "3333",
            "TEL": '123455678',
            "OBS": "RIESGO 1",
            "ID_FONO": "8",
            },
            index=[0]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            saver = FileDataFrameSaver(output_path=Path(tmpdir))
            risk_data(dataframe_saver=saver)

        # asserts
        mock_get_phones.assert_called_once_with(
            df=mock_merge.return_value,
            stop=5,
            colum_name='RIESGO'
        )
        mock_Escribir_Datos_Osiris.assert_called_once()
        mock_Escribir_Datos_Osiris.assert_called_once_with(
            mock_get_phones.return_value,
            'RIESGO_telefonos.csv',
            ['Cuenta', 'ID_FONO', 'TEL', 'OBS'],
            [
                "ID Cuenta o Nro. de Asig. (0)",
                "ID Tipo de Teléfono (17)",
                "Nro. de Teléfono (18)",
                "Obs. de Teléfono (19)"
            ],
            dataframe_saver=saver,
        )
