from pathlib import Path
from unittest import mock
import tempfile
from src.adapters.file_dataframe_saver import FileDataFrameSaver

from freezegun import freeze_time
import pandas as pd
from src.data_info import GenerateDataInfo
from src.data_naranja import GenerateDataNaranja

from src.subida import (
    Preparacion_Cuentas,
    Preparacion_Datos_Comafi,
    risk_data,
)
from src.prepare_comafi_accounts import prepare_comafi_accounts

integration_test_file_path = Path('./tests/integration_tests_data/')


@freeze_time('2023-05-06')
@mock.patch('subida.DataFrameSaver')
def test_integration_preparacion_cuentas_naranja(mock_dataframe_saver):
    integration_test_file_path = Path('./tests/integration_tests_data/')
    naranja_file_path = integration_test_file_path / 'cuentas_naranja/'
    cr_test_file_path = naranja_file_path / 'cr_test.csv'

    result_nar_bajo_path = naranja_file_path / 'subida_cartera_NAR-BAJO.csv'
    result_nar_medio_path = naranja_file_path / 'subida_cartera_NAR-MEDIO.csv'
    result_nar_alto_path = naranja_file_path / 'subida_cartera_NAR-ALTO.csv'

    expected_df_result_nar_bajo = pd.read_csv(result_nar_bajo_path, encoding='latin-1', sep=';')
    expected_df_result_nar_medio = pd.read_csv(result_nar_medio_path, encoding='latin-1', sep=';')
    expected_df_result_nar_alto = pd.read_csv(result_nar_alto_path, encoding='latin-1', sep=';')

    with tempfile.TemporaryDirectory() as tmpdir:
        saver = FileDataFrameSaver(output_path=Path(tmpdir))

        Preparacion_Cuentas(cr_file_path=cr_test_file_path, dataframe_saver=saver)
        saved_files = saver.get_saved_files()

        result_naranja_bajo = pd.read_csv(saved_files['NAR-BAJO'], encoding='latin-1', sep=';')
        result_naranja_medio = pd.read_csv(saved_files['NAR-MEDIO'], encoding='latin-1', sep=';')
        result_naranja_alto = pd.read_csv(saved_files['NAR-ALTO'], encoding='latin-1', sep=';')

    pd.testing.assert_frame_equal(result_naranja_bajo, expected_df_result_nar_bajo)
    pd.testing.assert_frame_equal(result_naranja_medio, expected_df_result_nar_medio)
    pd.testing.assert_frame_equal(result_naranja_alto, expected_df_result_nar_alto)


def test_integration_prepararion_riesgo_online_data():

    risk_data_directory_path = integration_test_file_path / 'datos_riesgo/'

    risk_df_filepath = risk_data_directory_path / 'riesgo_test.csv'
    osiris_accounts_df = risk_data_directory_path / 'cuentas_test.csv'
    expected_result_file_path = risk_data_directory_path / 'resultado_riesgo_test.csv'

    expected_result_df = pd.read_csv(expected_result_file_path, encoding='latin-1', sep=';')

    result_file_path = risk_data(risk_df_filepath, osiris_accounts_df)
    result_df = pd.read_csv(result_file_path, encoding='latin-1', sep=';')

    pd.testing.assert_frame_equal(result_df, expected_result_df)


@freeze_time('2023-05-06')
def test_integration_comafi_accounts_preparation():

    emerix_test_file_path = integration_test_file_path / 'comafi_accounts' / 'emerix_test.xlsx'
    result_directory_path = integration_test_file_path / 'comafi_accounts' / 'results'

    expected_files_in_result_directory = [
        'fake_subcliente_0',
        'fake_subcliente_1',
        'fake_subcliente_2',
        'fake_subcliente_3',
        'fake_subcliente_4',
        'fake_subcliente_5',
        'fake_subcliente_6',
        'fake_subcliente_7',
        'fake_subcliente_8',
        'fake_subcliente_9',
        'fake_subcliente_10',
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
        with tempfile.TemporaryDirectory() as tmpdir:
            saver = FileDataFrameSaver(output_path=Path(tmpdir))
            prepare_comafi_accounts(emerix_file_path=emerix_test_file_path, dataframe_saver=saver)
            saved_files = saver.get_saved_files()

            for _, path in saved_files.items():
                if 'fake_subcliente_0.csv' in path.name:
                    df_result_0 = pd.read_csv(path, encoding='latin-1', sep=';')
                elif 'fake_subcliente_1.csv' in path.name:
                    df_result_1 = pd.read_csv(path, encoding='latin-1', sep=';')
                elif 'fake_subcliente_2.csv' in path.name:
                    df_result_2 = pd.read_csv(path, encoding='latin-1', sep=';')
                elif 'fake_subcliente_3.csv' in path.name:
                    df_result_3 = pd.read_csv(path, encoding='latin-1', sep=';')
                elif 'fake_subcliente_4.csv' in path.name:
                    df_result_4 = pd.read_csv(path, encoding='latin-1', sep=';')
                elif 'fake_subcliente_5.csv' in path.name:
                    df_result_5 = pd.read_csv(path, encoding='latin-1', sep=';')
                elif 'fake_subcliente_6.csv' in path.name:
                    df_result_6 = pd.read_csv(path, encoding='latin-1', sep=';')
                elif 'fake_subcliente_7.csv' in path.name:
                    df_result_7 = pd.read_csv(path, encoding='latin-1', sep=';')
                elif 'fake_subcliente_8.csv' in path.name:
                    df_result_8 = pd.read_csv(path, encoding='latin-1', sep=';')
                elif 'fake_subcliente_9.csv' in path.name:
                    df_result_9 = pd.read_csv(path, encoding='latin-1', sep=';')
                elif 'fake_subcliente_10.csv' in path.name:
                    df_result_10 = pd.read_csv(path, encoding='latin-1', sep=';')

    assert sorted(expected_files_in_result_directory) == sorted([key for key in saved_files.keys()])

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


def test_integration_comafi_data_preparation():
    comafi_data_directory_path = integration_test_file_path / 'datos_comafi/'

    emerix_df_file_path = comafi_data_directory_path / 'emerix_test.xlsx'
    osiris_accounts_df = comafi_data_directory_path / 'cuentas_comafi_test.csv'
    expected_result_file_path = comafi_data_directory_path / 'resultado_datos_emerix_subida_telefono.csv'

    expected_result_df = pd.read_csv(expected_result_file_path, encoding='latin-1', sep=';')

    result_file_path = Preparacion_Datos_Comafi(emerix_df_file_path, osiris_accounts_df)
    result_df = pd.read_csv(result_file_path, encoding='latin-1', sep=';')

    pd.testing.assert_frame_equal(result_df, expected_result_df)


def test_integration_naranja_data_preparation():
    naranja_data_file_path = integration_test_file_path / 'datos_naranja/'

    cr_test_file_path = naranja_data_file_path / 'cr_test.csv'
    osiris_accounts_df = naranja_data_file_path / 'cuentas_osiris_naranja_test.csv'

    result_mails_path = naranja_data_file_path / 'result_datos_cr_subida_mail.csv'
    result_phones_path = naranja_data_file_path / 'result_datos_cr_subida_telefonos.csv'

    expected_df_result_mails = pd.read_csv(result_mails_path, encoding='latin-1', sep=';')
    expected_df_result_phones = pd.read_csv(result_phones_path, encoding='latin-1', sep=';')

    all_result_file_path = GenerateDataNaranja.process(
        cr_file_path=cr_test_file_path,
        osiris_accounts_file_path=osiris_accounts_df
    )

    for result_path in all_result_file_path:
        if 'datos_cr_subida_mail.csv' in result_path.name:
            df_result_mails = pd.read_csv(result_path, encoding='latin-1', sep=';')
        elif 'datos_cr_subida_telefonos.csv' in result_path.name:
            df_result_phones = pd.read_csv(result_path, encoding='latin-1', sep=';')

    pd.testing.assert_frame_equal(expected_df_result_mails, df_result_mails)
    pd.testing.assert_frame_equal(expected_df_result_phones, df_result_phones)


def test_integration_info_experto_data_preparation():
    info_experto_data_directory_path = integration_test_file_path / 'datos_info_experto'

    info_df_filepath = info_experto_data_directory_path / 'info_test.xlsx'
    osiris_accounts_df = info_experto_data_directory_path / 'cuentas_test.csv'

    expected_patrimoniales_path = info_experto_data_directory_path / 'result_info_patrimoniales.csv'
    expected_info_q_vehiculos_path = info_experto_data_directory_path / 'result_info_q_vehiculos.csv'
    expected_result_info_mail_path = info_experto_data_directory_path / 'result_info_mail.csv'
    expected_result_info_sueldo_path = info_experto_data_directory_path / 'result_info_sueldo.csv'
    expected_result_info_telefonos_path = info_experto_data_directory_path / 'result_info_telefonos.csv'

    expected_result_info_patrimoniales_df = pd.read_csv(expected_patrimoniales_path, encoding='latin-1', sep=';')
    expected_result_info_q_vehiculos_df = pd.read_csv(expected_info_q_vehiculos_path, encoding='latin-1', sep=';')
    expected_result_info_mail_df = pd.read_csv(expected_result_info_mail_path, encoding='latin-1', sep=';')
    expected_result_info_sueldo_df = pd.read_csv(expected_result_info_sueldo_path, encoding='latin-1', sep=';')
    expected_result_info_telefonos_df = pd.read_csv(expected_result_info_telefonos_path, encoding='latin-1', sep=';')

    with mock.patch.object(GenerateDataInfo, 'info_experto_file_path', info_df_filepath):
        with mock.patch.object(GenerateDataInfo, 'osiris_accounts_file_path', osiris_accounts_df):

            all_result_file_paths = GenerateDataInfo.process()

    for result_path in all_result_file_paths:
        if 'info_patrimoniales' in result_path.name:
            df_result_info_patrimoniales = pd.read_csv(result_path, encoding='latin-1', sep=';')
        elif 'info_q_vehiculos' in result_path.name:
            df_result_info_q_vehiculos = pd.read_csv(result_path, encoding='latin-1', sep=';')
        elif 'info_mail' in result_path.name:
            df_result_info_mail = pd.read_csv(result_path, encoding='latin-1', sep=';')
        elif 'info_sueldo' in result_path.name:
            df_result_info_sueldo = pd.read_csv(result_path, encoding='latin-1', sep=';')
        elif 'info_telefonos' in result_path.name:
            df_result_info_telefonos = pd.read_csv(result_path, encoding='latin-1', sep=';')

    pd.testing.assert_frame_equal(expected_result_info_patrimoniales_df, df_result_info_patrimoniales)
    pd.testing.assert_frame_equal(expected_result_info_q_vehiculos_df, df_result_info_q_vehiculos)
    pd.testing.assert_frame_equal(expected_result_info_mail_df, df_result_info_mail)
    pd.testing.assert_frame_equal(expected_result_info_sueldo_df, df_result_info_sueldo)
    pd.testing.assert_frame_equal(expected_result_info_telefonos_df, df_result_info_telefonos)
