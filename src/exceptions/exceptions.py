import pandas as pd
from constants.error_messages import FILE_CONTAINS_INCORRECT_COLUMNS


# CLASSES

class IncorrectColumnsError(AssertionError):
    """Raised when a dataframe does not contain the required columns.
    Attributes:
    dataframe: the dataframe that results from reading a file
    required_columns: columns that need to be present in the dataframe
    """
    def __init__(self, dataframe: pd.DataFrame, required_columns):
        self.dataframe = dataframe
        self.required_columns = required_columns
        self.message = FILE_CONTAINS_INCORRECT_COLUMNS
        super().__init__(self.message)
    pass

# Validator Functions


def validate_columns(data_frame: pd.DataFrame, required_columns: list):
    """
    Checks whether the columns of a dataframe (typically the resulting Dataframe of reading
    a file) contains all the columns that are needed."""
    try:
        assert data_frame.columns.values == required_columns
    except AssertionError as e:
        print(e)
        raise IncorrectColumnsError(data_frame, required_columns)
