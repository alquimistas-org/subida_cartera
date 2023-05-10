import pandas as pd
from src.helpers import (
    get_phones,
    read_osiris_accounts,
)
from ..src.constants.constants import OSIRIS_ACCOUNTS_FILE_PATH
from unittest import mock


class TestHelpers:

    def test_return_df_phone(self):

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
    def test_read_osiris_account_return(self, mock_read_csv):
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
