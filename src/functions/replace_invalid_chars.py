from cmd import Cmd
import os
import shutil
import pandas as pd
import numpy as np
import datetime
import time
import traceback

from driver_email import enviar_mail_con_adjuntos
from .constants.constants import (
    PROGRAMMER,
    USER,
    PASSWORD,
    DATA_UPLOADER_HEADER,
    PROVINCES,
    UTIL_COLS_COMAFI,
    ACOUNT_PREP_COL,
)

def replace_invalid_chars(dataframe):
    characters = ['#', 'Ð', 'ð', '&']
    for char in characters:
        n = dataframe['nombre'].str.contains(char).sum()
        dataframe['nombre'] = dataframe['nombre'].str.replace(char, 'ñ').str.title()
        # n = dataframe['nombre'].str.contains(char).sum()
        print(f'character {char}: se remplazaron {n}')
