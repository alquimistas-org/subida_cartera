import pandas as pd
from src.validations.validations import (
    validate_columns,
    IncorrectColumnsError,
)
from ..src.constants.constants import CR_REQUIRED_FIELDS
import pytest


class TestValidators:

    cr = pd.DataFrame()

    correct_data = {
        'NRODOC': [11111111, 22222222, 33333333],
        'NOMBRECOMPLETO': ['Juan Pedro Gracía', 'Manuel Gimenez', 'Lalo Landa'],
        'CALLE': ['Fake st1', 'Calle falsa 2', 'Another St.'],
        'NUMERO': [1234, 346, 5678],
        'PISO': [1, 2, 3],
        'DEPTO': [4, 5, 6],
        'BARRIO': ['Bo. Sanidad', 'Bo. Ferroviarios', 'Bo. Santa Ana'],
        'LOCALIDAD': ['Dorrego', 'Loc2', 'Loc3'],
        'PROVINCIA': ['Mendoza', 'San Luis', 'San Jan'],
        'POSTAL': [1234, 5677, 8899],
        'DEUDA_ACTUALIZADA': [1234567, 234678, 86587976],
        'INICIOMORA': ['Fecha1', 'Fecha2', 'Fecha3'],
        'CAPITAL': [234567, 2345678, 3456789],
        'GESTOR_ANTERIOR': ['Marcos Luis', 'Pedro Sarmineto', 'Gimenez Jorge'],
        'SCORE': [1234, 23455, 567],
    }

    incorrect_data = {
        'NRODOC': [11111111, 22222222, 33333333],
        'NOMBRECOMPLETO': ['Juan Pedro Gracía', 'Manuel Gimenez', 'Lalo Landa'],
        'CALLE': ['Fake st1', 'Calle falsa 2', 'Another St.'],
        'NUMERO': [1234, 346, 5678],
        'PISO': [1, 2, 3],
        'DEPTO': [4, 5, 6],
        'BARRIO': ['Bo. Sanidad', 'Bo. Ferroviarios', 'Bo. Santa Ana'],
        'PROVINCIA': ['Mendoza', 'San Luis', 'San Jan'],
        'POSTAL': [1234, 5677, 8899],
        'DEUDA_ACTUALIZADA': [1234567, 234678, 86587976],
        'INICIOMORA': ['Fecha1', 'Fecha2', 'Fecha3'],
        'CAPITAL': [234567, 2345678, 3456789],
        'GESTOR_ANTERIOR': ['Marcos Luis', 'Pedro Sarmineto', 'Gimenez Jorge'],
        'SCORE': [1234, 23455, 567]
    }

    def test_validate_columns_raises_exception(self):

        incorrect_df = pd.DataFrame(self.incorrect_data)

        with pytest.raises(IncorrectColumnsError):
            validate_columns(incorrect_df, CR_REQUIRED_FIELDS)

    def test_validate_columns_does_not_raise_exception(self):

        correct_df = pd.DataFrame(self.correct_data)

        try:
            validate_columns(correct_df, CR_REQUIRED_FIELDS)
        except IncorrectColumnsError as exc:
            assert False, f"function validate_columns raised {exc}"
