from unittest.mock import (
    patch,
    MagicMock,
)

import pandas as pd

import pytest

from src.data_naranja import GenerateDataNaranja


@pytest.fixture
def mocked_cr() -> pd.DataFrame:
    amount_of_rows = 7
    cr_columns = ['DNI', 'column_cr_a', 'column_cr_b', 'column_cr_c']
    return pd.DataFrame(
            [
                [
                    f'fake_{col}_{row}'.lower()
                    for col in cr_columns
                ]
                for row in range(amount_of_rows)
            ],
            columns=cr_columns
        )


@pytest.fixture
def mocked_osiris_accounts() -> pd.DataFrame:
    amount_of_rows = 5
    cr_columns = ['DNI', 'column_osiris_a', 'column_osiris_b']
    return pd.DataFrame(
            [
                [
                    f'fake_{col}_{row}'.lower()
                    for col in cr_columns
                ]
                for row in range(amount_of_rows)
            ],
            columns=cr_columns
        )


@pytest.fixture
def mocked_mails_result() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ['fake_account_1', 'fake_mail_1'],
            ['fake_account_2', 'fake_mail_2'],
        ],
        columns=['Cuenta', 'EMAIL']
    )


class TestGenerateDaaNarana:

    @patch.object(GenerateDataNaranja, '_get_cr_data')
    @patch.object(GenerateDataNaranja, '_get_and_wirte_all_phones_from_cr')
    @patch.object(GenerateDataNaranja, '_get_and_write_mails_from_cr')
    def test_process(
        self,
        patched_get_and_write_mails_from_cr: MagicMock,
        patched_get_and_wirte_all_phones_from_cr: MagicMock,
        pathced_get_cr_data: MagicMock,
    ):

        # arrange
        mocked_cr = 'cr'
        expected_phones_file_path = 'phones_file_path'
        expected_mails_file_path = 'mails_file_path'
        expected_result = [expected_phones_file_path, expected_mails_file_path]
        pathced_get_cr_data.return_value = mocked_cr
        patched_get_and_wirte_all_phones_from_cr.return_value = expected_phones_file_path
        patched_get_and_write_mails_from_cr.return_value = expected_mails_file_path

        # act
        result = GenerateDataNaranja.process()

        # assert

        pathced_get_cr_data.assert_called_once()
        patched_get_and_wirte_all_phones_from_cr.assert_called_once_with(mocked_cr)
        patched_get_and_write_mails_from_cr.assert_called_once_with(mocked_cr)

        assert result == expected_result

    @pytest.mark.skip(reason='TODO')
    @patch('src.data_info.read_osiris_accounts')
    @patch('src.data_info.read_cr_data')
    def test_get_cr_data(
        self,
        patched_read_cr_data: MagicMock,
        patched_read_osiris_accounts: MagicMock,
        mocked_cr: pd.DataFrame,
        mocked_osiris_accounts: pd.DataFrame,
    ):
        patched_read_cr_data.return_value = mocked_cr
        patched_read_osiris_accounts.return_value = mocked_osiris_accounts
        expetcetd_result = pd.DataFrame(
            [
                [],
            ],
            columns=['DNI', 'column_osiris_a', 'column_osiris_b', 'column_cr_a', 'column_cr_b', 'column_cr_c']
        )
        GenerateDataNaranja._get_cr_data()
        assert expetcetd_result

    @pytest.mark.skip(reason='TODO')
    def test_get_and_wirte_all_phones_from_cr(self):
        assert False

    @pytest.mark.skip(reason='TODO')
    def test_get_all_phones_from_cr(self):
        assert False

    @pytest.mark.skip(reason='TODO')
    def test_get_main_personal_phones_from_cr(self):
        assert False

    @pytest.mark.skip(reason='TODO')
    def test_get_secondary_personal_phones_from_cr_where_main_phones_was_empty(self):
        assert False

    @pytest.mark.skip(reason='TODO')
    def test_get_landlines_phones_from_cr(self):
        assert False

    @pytest.mark.skip(reason='TODO')
    def test_get_work_phones_from_cr(self):
        assert False

    @pytest.mark.skip(reason='TODO')
    def test_get_other_phones_df(self):
        assert False

    @pytest.mark.skip(reason='TODO')
    def test_clean_phone_numbers(self):
        assert False

    @pytest.mark.skip(reason='TODO')
    def test_write_phones_data_result(self):
        assert False

    @pytest.mark.skip(reason='TODO')
    def test_get_and_write_mails_from_cr(self):
        assert False

    @pytest.mark.skip(reason='TODO')
    def test_get_mails_from_cr(self):
        assert False

    @patch('src.data_naranja.Escribir_Datos_Osiris')
    def test_write_mail_data_results(
        self,
        patched_Escribir_Datos_Osiris: MagicMock,
        mocked_mails_result: pd.DataFrame,
    ):
        expected_result = 'fake_result'
        patched_Escribir_Datos_Osiris.return_value = expected_result
        result = GenerateDataNaranja._write_mail_data_results(mocked_mails_result)
        patched_Escribir_Datos_Osiris.assert_called_once_with(
            mocked_mails_result,
            'datos_cr_subida_mail.csv',
            ['Cuenta', 'EMAIL'],
            ['ID Cuenta o Nro. de Asig. (0)', "Email (16)"],
        )
        assert result == expected_result
