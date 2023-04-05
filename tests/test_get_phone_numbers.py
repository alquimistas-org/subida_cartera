import pandas as pd
from src.subida import (
    get_phone_risk,
    read_osiris_accounts,
    risk_data
)
from unittest import mock


class TestRiskData:

    def test_return_df_phone(self):

        df = pd.DataFrame({
            "DNI": "23456677",
            "tel_riesgo_1": '123455678',
            "Cuenta": "3333",
            "TEL": "3333",
            },
            index=[0]
            )
        df_result = get_phone_risk(df_risk=df)
        expected = pd.DataFrame({
            "Cuenta": "3333",
            "TEL": '123455678',
            "OBS": "RIESGO 1",
            "ID_FONO": "8",
            },
            index=[0]
        )

        pd.testing.assert_frame_equal(df_result, expected)

    @mock.patch("pandas.read_csv")
    def test_read_osiris_account_return(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({
            "Cuenta": "1234",
            "Mat. Unica": "23345"
            },
            index=[0]
        )
        df_result = read_osiris_accounts()
        expected = pd.DataFrame({
            "Cuenta": "1234",
            "DNI": "23345"
            },
            index=[0]
        )

        pd.testing.assert_frame_equal(df_result, expected)

    @mock.patch("pandas.read_csv")
    @mock.patch("pandas.merge")
    @mock.patch("src.subida.read_osiris_accounts")
    @mock.patch("src.subida.get_phone_risk")
    @mock.patch("src.subida.Escribir_Datos_Osiris")
    def test_risk_data(
        self,
        mock_Escribir_Datos_Osiris,
        mock_get_phone_risk,
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
        mock_get_phone_risk.return_value = pd.DataFrame({
            "Cuenta": "3333",
            "TEL": '123455678',
            "OBS": "RIESGO 1",
            "ID_FONO": "8",
            },
            index=[0]
        )
        risk_data()

        mock_Escribir_Datos_Osiris.assert_called_once()
        mock_Escribir_Datos_Osiris.assert_called_once_with(
            mock_get_phone_risk.return_value,
            'RIESGO_telefonos.csv',
            ['Cuenta', 'ID_FONO', 'TEL', 'OBS'],
            [
                "ID Cuenta o Nro. de Asig. (0)",
                "ID Tipo de Teléfono (17)",
                "Nro. de Teléfono (18)",
                "Obs. de Teléfono (19)"
            ]
        )
