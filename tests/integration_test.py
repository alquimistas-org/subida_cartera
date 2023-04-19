import os
from pathlib import Path
from unittest import mock

from freezegun import freeze_time
import pandas as pd

from src.subida import (
    Preparacion_Cuentas,
    risk_data,
    Preparacion_Cuentas_Comafi,
)

integration_test_file_path = Path('./tests/integration_tests_data/')


@freeze_time('2023-04-12')
def test_integration_preparacion_cuentas_naranja():
    naranja_file_path = integration_test_file_path / 'cuentas_naranja/'

    cr_test_file_path = naranja_file_path / 'cr_test.csv'

    result_nar_bajo_path = naranja_file_path / 'subida_cartera_NAR-BAJO.csv'
    result_nar_medio_path = naranja_file_path / 'subida_cartera_NAR-MEDIO.csv'
    result_nar_alto_path = naranja_file_path / 'subida_cartera_NAR-ALTO.csv'

    expected_df_result_nar_bajo = pd.read_csv(result_nar_bajo_path, encoding='latin-1', sep=';')
    expected_df_result_nar_medio = pd.read_csv(result_nar_medio_path, encoding='latin-1', sep=';')
    expected_df_result_nar_alto = pd.read_csv(result_nar_alto_path, encoding='latin-1', sep=';')

    all_result_file_path = Preparacion_Cuentas(cr_file_path=cr_test_file_path)

    for risk in ['BAJO', 'MEDIO', 'ALTO']:
        match_files_path = [result
                            for result in all_result_file_path
                            if f'subida_cartera_NAR-{risk}.csv' in result.name]
        assert len(match_files_path) == 1

    for result_path in all_result_file_path:
        if 'BAJO' in result_path.name:
            df_result_nar_bajo = pd.read_csv(result_path, encoding='latin-1', sep=';')
        elif 'MEDIO' in result_path.name:
            df_result_nar_medio = pd.read_csv(result_path, encoding='latin-1', sep=';')
        elif 'ALTO' in result_path.name:
            df_result_nar_alto = pd.read_csv(result_path, encoding='latin-1', sep=';')

    pd.testing.assert_frame_equal(df_result_nar_bajo, expected_df_result_nar_bajo)
    pd.testing.assert_frame_equal(df_result_nar_medio, expected_df_result_nar_medio)
    pd.testing.assert_frame_equal(df_result_nar_alto, expected_df_result_nar_alto)
    print('hola')


def test_integration_prepararion_riesgo_online_data():

    risk_data_directory_path = integration_test_file_path / 'datos_riesgo/'

    risk_df_filepath = risk_data_directory_path / 'riesgo_test.csv'
    osiris_accounts_df = risk_data_directory_path / 'cuentas_test.csv'
    expected_result_file_path = risk_data_directory_path / 'resultado_riesgo_test.csv'

    expected_result_df = pd.read_csv(expected_result_file_path, encoding='latin-1', sep=';')

    result_file_path = risk_data(risk_df_filepath, osiris_accounts_df)
    result_df = pd.read_csv(result_file_path, encoding='latin-1', sep=';')

    pd.testing.assert_frame_equal(result_df, expected_result_df)


@freeze_time('2023-04-17')
def test_integration_comafi_accounts_preparation():

    emerix_test_file_path = integration_test_file_path / 'comafi_accounts' / 'emerix_test.xlsx'
    result_directory_path = integration_test_file_path / 'comafi_accounts' / 'results'

    expected_files_in_result_directory = [
        'fake_subcliente_0.csv',
        'fake_subcliente_1.csv',
        'fake_subcliente_2.csv',
        'fake_subcliente_3.csv',
        'fake_subcliente_4.csv',
        'fake_subcliente_5.csv',
        'fake_subcliente_6.csv',
        'fake_subcliente_7.csv',
        'fake_subcliente_8.csv',
        'fake_subcliente_9.csv',
        'fake_subcliente_10.csv',
    ]
    expected_df_result_0 = pd.read_csv(result_directory_path / 'fake_subcliente_0.csv', encoding='latin-1', sep=';')
    expected_df_result_1 = pd.read_csv(result_directory_path / 'fake_subcliente_1.csv', encoding='latin-1', sep=';')
    expected_df_result_2 = pd.read_csv(result_directory_path / 'fake_subcliente_2.csv', encoding='latin-1', sep=';')
    expected_df_result_3 = pd.read_csv(result_directory_path / 'fake_subcliente_3.csv', encoding='latin-1', sep=';')
    expected_df_result_4 = pd.read_csv(result_directory_path / 'fake_subcliente_4.csv', encoding='latin-1', sep=';')
    expected_df_result_5 = pd.read_csv(result_directory_path / 'fake_subcliente_5.csv', encoding='latin-1', sep=';')
    expected_df_result_6 = pd.read_csv(result_directory_path / 'fake_subcliente_6.csv', encoding='latin-1', sep=';')
    expected_df_result_7 = pd.read_csv(result_directory_path / 'fake_subcliente_7.csv', encoding='latin-1', sep=';')
    expected_df_result_8 = pd.read_csv(result_directory_path / 'fake_subcliente_8.csv', encoding='latin-1', sep=';')
    expected_df_result_9 = pd.read_csv(result_directory_path / 'fake_subcliente_9.csv', encoding='latin-1', sep=';')
    expected_df_result_10 = pd.read_csv(result_directory_path / 'fake_subcliente_10.csv', encoding='latin-1', sep=';')

    with mock.patch('builtins.input', return_value='fake'):
        result_directory_path = Preparacion_Cuentas_Comafi(emerix_file_path=emerix_test_file_path)

    files_in_directory_result = os.listdir(result_directory_path)

    assert sorted(expected_files_in_result_directory) == sorted(files_in_directory_result)

    for result_path in files_in_directory_result:
        if 'fake_subcliente_0.csv' in result_path:
            df_result_0 = pd.read_csv(result_directory_path / result_path, encoding='latin-1', sep=';')
        elif 'fake_subcliente_1.csv' in result_path:
            df_result_1 = pd.read_csv(result_directory_path / result_path, encoding='latin-1', sep=';')
        elif 'fake_subcliente_2.csv' in result_path:
            df_result_2 = pd.read_csv(result_directory_path / result_path, encoding='latin-1', sep=';')
        elif 'fake_subcliente_3.csv' in result_path:
            df_result_3 = pd.read_csv(result_directory_path / result_path, encoding='latin-1', sep=';')
        elif 'fake_subcliente_4.csv' in result_path:
            df_result_4 = pd.read_csv(result_directory_path / result_path, encoding='latin-1', sep=';')
        elif 'fake_subcliente_5.csv' in result_path:
            df_result_5 = pd.read_csv(result_directory_path / result_path, encoding='latin-1', sep=';')
        elif 'fake_subcliente_6.csv' in result_path:
            df_result_6 = pd.read_csv(result_directory_path / result_path, encoding='latin-1', sep=';')
        elif 'fake_subcliente_7.csv' in result_path:
            df_result_7 = pd.read_csv(result_directory_path / result_path, encoding='latin-1', sep=';')
        elif 'fake_subcliente_8.csv' in result_path:
            df_result_8 = pd.read_csv(result_directory_path / result_path, encoding='latin-1', sep=';')
        elif 'fake_subcliente_9.csv' in result_path:
            df_result_9 = pd.read_csv(result_directory_path / result_path, encoding='latin-1', sep=';')
        elif 'fake_subcliente_10.csv' in result_path:
            df_result_10 = pd.read_csv(result_directory_path / result_path, encoding='latin-1', sep=';')

    pd.testing.assert_frame_equal(df_result_0, expected_df_result_0)
    pd.testing.assert_frame_equal(df_result_1, expected_df_result_1)
    pd.testing.assert_frame_equal(df_result_2, expected_df_result_2)
    pd.testing.assert_frame_equal(df_result_3, expected_df_result_3)
    pd.testing.assert_frame_equal(df_result_4, expected_df_result_4)
    pd.testing.assert_frame_equal(df_result_5, expected_df_result_5)
    pd.testing.assert_frame_equal(df_result_6, expected_df_result_6)
    pd.testing.assert_frame_equal(df_result_7, expected_df_result_7)
    pd.testing.assert_frame_equal(df_result_8, expected_df_result_8)
    pd.testing.assert_frame_equal(df_result_9, expected_df_result_9)
    pd.testing.assert_frame_equal(df_result_10, expected_df_result_10)
