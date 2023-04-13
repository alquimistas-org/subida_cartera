import pandas as pd
from src.preparacion_cuentas_comafi import (
    replace_invalid_chars,
    fill_data,
)
from .test_utils.test_data import (
    invalid_chars_dataframe,
    expected_invalid_chars_dataframe,
    non_os_test_dataframe,
    os_test_dataframe,
)


class TestReplaceInvalidChars:

    def test_replace_invalid_chars(self):
        replace_invalid_chars(invalid_chars_dataframe)
        ## it has valid chars only now
        pd.testing.assert_frame_equal(
            invalid_chars_dataframe, 
            expected_invalid_chars_dataframe
        )


class TestFillData:



    def test_fill_data(self):
        fill_data(non_os_test_dataframe, os_test_dataframe)
        pd.testing.assert_series_equal(
            os_test_dataframe['Nº de Asignacion (0)'], 
            pd.Series(['12345678', '87654321'], name="Nº de Asignacion (0)")
        )


class TestPreparacionCuentasComafi:
    
    def test_preparacion_cuentas_comafi(self):
      return ' '
