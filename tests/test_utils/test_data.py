import pandas as pd

## replace_invalid_chars ['#', 'Ð', 'ð', '&']

invalid_chars_dataframe = pd.DataFrame(
    {
        "Numbers#": [30, 25, 12],
        "NamesÐ": ["Juan", "Jorðe","Luca&"],
    }
)

expected_invalid_chars_dataframe = pd.DataFrame(
    {
        "Numbersñ": [30, 25, 12],
        "Namesñ": ["Juan", "Jorñe","Lucañ"],
    }
)