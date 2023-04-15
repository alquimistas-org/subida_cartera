from pathlib import Path

from freezegun import freeze_time
import pandas as pd

from src.subida import Preparacion_Cuentas


@freeze_time('2023-04-12')
def preparacion_cuentas_naranja_integration_test():
    integration_test_file_path = Path('./tests/integration_tests_data/')
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
        match_files_path = [result for result in all_result_file_path if f'subida_cartera_NAR-{risk}.csv' in result]
        assert len(match_files_path) == 1

    for result_path in all_result_file_path:
        if 'BAJO' in result_path:
            df_result_nar_bajo = pd.read_csv(result_path, encoding='latin-1', sep=';')
        elif 'MEDIO' in result_path:
            df_result_nar_medio = pd.read_csv(result_path, encoding='latin-1', sep=';')
        elif 'ALTO' in result_path:
            df_result_nar_alto = pd.read_csv(result_path, encoding='latin-1', sep=';')

    pd.testing.assert_frame_equal(df_result_nar_bajo, expected_df_result_nar_bajo)
    pd.testing.assert_frame_equal(df_result_nar_medio, expected_df_result_nar_medio)
    pd.testing.assert_frame_equal(df_result_nar_alto, expected_df_result_nar_alto)


if __name__ == '__main__':
    preparacion_cuentas_naranja_integration_test()
