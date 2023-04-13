import pandas as pd
from src.risk_data import (
    get_phones,
    read_osiris_accounts,
    risk_data
)
from ..src.constants.constants import OSIRIS_ACCOUNTS_FILE_PATH
from unittest import mock


class TestRiskData:

    def test_return_df_phone(self):  # TODO: in other PR move this test to other file for helper functions tests

        df = pd.DataFrame({
            "DNI": "23456677",
            "tel_riesgo_1": '123455678',
            "Cuenta": "3333",
            "TEL": "3333",
            },
            index=[0]
            )

        num_tel = len([col_name for col_name in list(df.columns) if 'tel_riesgo' in col_name])

        df_result = get_phones(
            df=df,
            stop=num_tel+1,
            colum_name='RIESGO'
            )

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
    def test_read_osiris_account_return(self, mock_read_csv):  # TODO: in other PR move this test to other file for helper functions tests  # noqa
        mock_read_csv.return_value = pd.DataFrame({
            "Cuenta": "1234",
            "Mat. Unica": "23345"
            },
            index=[0]
        )
        df_result = read_osiris_accounts(OSIRIS_ACCOUNTS_FILE_PATH)
        expected = pd.DataFrame({
            "Cuenta": "1234",
            "DNI": "23345"
            },
            index=[0]
        )

        pd.testing.assert_frame_equal(df_result, expected)

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
        risk_data()

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
            ]
        )
