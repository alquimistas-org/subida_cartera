import pandas as pd
from src.clean_numbers import (
    clean_numbers,
)
from .test_utils.test_data import (
    phone_numbers_dataframe,
    expected_phone_numbers_dataframe,
)


class TestCleanNumbers:

    def test_clean_numbers(self):
        result = clean_numbers(phone_numbers_dataframe)
        pd.testing.assert_frame_equal(
            result,
            expected_phone_numbers_dataframe
        )
