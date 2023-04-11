import pandas as pd
from src.functions.replace_invalid_chars import (
    replace_invalid_chars
)
from .test_utils.test_data import (
    invalid_chars_dataframe,
    expected_invalid_chars_dataframe,
)
from unittest import mock


class TestReplaceInvalidChars:

    def test_replace_invalid_chars(self):
        pd.testing.assert_frame_equal(
            invalid_chars_dataframe,
            expected_invalid_chars_dataframe
        )
