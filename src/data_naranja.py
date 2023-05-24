import numpy as np
import pandas as pd

from constants.constants import (
    CR_FILE_PATH,
    OSIRIS_ACCOUNTS_FILE_PATH,
)
from helpers import (
    read_cr_data,
    read_osiris_accounts,
)
from src.ports.dataframe_saver import DataFrameSaver
from write_data_osiris import Escribir_Datos_Osiris


class GenerateDataNaranja:

    osiris_accounts_file_path = OSIRIS_ACCOUNTS_FILE_PATH
    cr_file_path = CR_FILE_PATH

    @classmethod
    def process(cls, dataframe_saver: DataFrameSaver) -> None:
        print('Preparando planillas de datos...')
        cr = cls._get_cr_data()
        cls._get_and_wirte_all_phones_from_cr(cr, dataframe_saver)
        cls._get_and_write_mails_from_cr(cr, dataframe_saver)

    @classmethod
    def _get_cr_data(cls) -> pd.DataFrame:
        cr = read_cr_data(cr_file_path=cls.cr_file_path)
        osiris_accounts = read_osiris_accounts(cls.osiris_accounts_file_path)
        cr_accounts_that_are_in_osiris_df = pd.merge(osiris_accounts, cr, how="inner", on="DNI")
        return cr_accounts_that_are_in_osiris_df

    @classmethod
    def _get_and_wirte_all_phones_from_cr(cls, cr: pd.DataFrame, dataframe_saver: DataFrameSaver) -> None:
        phones = cls._get_all_phones_from_cr(cr)
        cleaned_phones = cls._clean_phone_numbers(phones)
        cls._write_phones_data_result(cleaned_phones, dataframe_saver)

    @classmethod
    def _get_all_phones_from_cr(cls, cr_df: pd.DataFrame) -> pd.DataFrame:

        print('Getting phone numbers from cr.csv...\n')

        all_phones_df_to_concatenate = [

            df_phone_getter_from_cr(cr_df)

            for df_phone_getter_from_cr in [
                cls._get_main_personal_phones_from_cr,
                cls._get_secondary_personal_phones_from_cr_where_main_phones_was_empty,
                cls._get_landlines_phones_from_cr,
                cls._get_work_phones_from_cr,
                cls._get_other_phones_df,
            ]
        ]

        return pd.concat(all_phones_df_to_concatenate)

    @staticmethod
    def _get_main_personal_phones_from_cr(cr: pd.DataFrame) -> pd.DataFrame:

        df = cr.loc[cr['TEL_ALTERNATIVO'].notnull(), ['Cuenta', 'TEL_ALTERNATIVO']].copy()
        df.rename(columns={'TEL_ALTERNATIVO': 'TEL'}, inplace=True)
        df['ID_FONO'] = '1'
        print(f'{len(df)} Telefonos ALTERNATIVOS cargados como MASIVOS')
        return df

    @staticmethod
    def _get_secondary_personal_phones_from_cr_where_main_phones_was_empty(cr: pd.DataFrame) -> pd.DataFrame:
        main_phone_is_empty_and_secondary_is_not = cr['TEL_ALTERNATIVO'].isnull() & cr['TEL_PARTICULAR'].notnull()
        df = cr.loc[main_phone_is_empty_and_secondary_is_not, ['Cuenta', 'TEL_PARTICULAR']].copy()
        df.rename(columns={'TEL_PARTICULAR': 'TEL'}, inplace=True)
        df['ID_FONO'] = '1'

        cr.loc[cr['TEL_ALTERNATIVO'].isnull() & cr['TEL_PARTICULAR'].notnull(), 'TEL_PARTICULAR'] = np.nan
        print(f'{len(df)} Telefonos PARTICULAR cargados com MASIVOS en cuentas que no poseen ALTERNATIVO')
        return df

    @staticmethod
    def _get_landlines_phones_from_cr(cr: pd.DataFrame) -> pd.DataFrame:
        df = cr.loc[cr['TEL_PARTICULAR'].notnull(), ['Cuenta', 'TEL_PARTICULAR']]\
            .rename(columns={'TEL_PARTICULAR': 'TEL'}, inplace=False).copy()
        df['ID_FONO'] = '2'
        print(f'{len(df)} Telefonos ALTERNATIVOS cargados como FIJOS')
        return df

    @staticmethod
    def _get_work_phones_from_cr(cr: pd.DataFrame) -> pd.DataFrame:
        df = cr.loc[cr['TEL_LABORAL'].notnull(), ['Cuenta', 'TEL_LABORAL']].copy()
        df.rename(columns={'TEL_LABORAL': 'TEL'}, inplace=True)
        df['ID_FONO'] = '3'
        print(f'{len(df)} Telefonos LABORALES cargados como LABORALES')
        return df

    @staticmethod
    def _get_other_phones_df(cr: pd.DataFrame) -> pd.DataFrame:
        df = cr.melt(
            id_vars=['Cuenta'], value_vars=['TEL_CR_PARTICULAR', 'TEL_CR_LABORAL', 'TEL_CR_ALTERNATIVO']
            ).dropna().copy()
        df = df[['Cuenta', 'value']].rename(columns={'value': 'TEL'}, inplace=False)
        df['ID_FONO'] = '8'
        print(f'{len(df)} Telefonos OTROS_CR cargados como OTROS')
        return df

    @staticmethod
    def _clean_phone_numbers(phones_df: pd.DataFrame) -> pd.DataFrame:

        phones_df['TEL'] = phones_df['TEL'].str.replace(r'[^0-9]+', '', regex=True)
        phones_df['TEL'] = phones_df['TEL'].str.replace(' ', '')
        phones_df['TEL'] = phones_df['TEL'].replace('', np.nan)
        phones_df['TEL'].fillna(0)
        phones_df = phones_df.astype({'TEL': 'Int64'})
        phones_df = phones_df.astype({'TEL': 'str'})
        phones_df.drop(phones_df[phones_df.TEL == '0'].index, inplace=True)
        return phones_df

    @staticmethod
    def _write_phones_data_result(cleaned_phones_df: pd.DataFrame, dataframe_saver: DataFrameSaver) -> None:
        Escribir_Datos_Osiris(
            cleaned_phones_df,
            'datos_cr_subida_telefonos.csv',
            ['Cuenta', 'ID_FONO', 'TEL'],
            ['ID Cuenta o Nro. de Asig. (0)', "ID Tipo de Teléfono (17)", "Nro. de Teléfono (18)"],
            dataframe_saver,
        )
        print(f'{len(cleaned_phones_df)} TELEFONOS se guardaron en archivo: subida_telefono.csv')

    @classmethod
    def _get_and_write_mails_from_cr(cls, cr: pd.DataFrame, dataframe_saver: DataFrameSaver) -> None:
        mails = cls._get_mails_from_cr(cr)
        cls._write_mail_data_results(mails, dataframe_saver)

    @staticmethod
    def _get_mails_from_cr(cr: pd.DataFrame) -> pd.DataFrame:
        cr.loc[cr['EMAIL'].notnull(), 'EMAIL'] = cr.loc[cr['EMAIL'].notnull(), 'EMAIL'].str.replace(' ', '')
        mails = cr.loc[cr['EMAIL'].notnull(), ['Cuenta', 'EMAIL']].copy()
        return mails

    @staticmethod
    def _write_mail_data_results(mails: pd.DataFrame, dataframe_saver: DataFrameSaver) -> None:
        Escribir_Datos_Osiris(
            mails,
            'datos_cr_subida_mail.csv',
            ['Cuenta', 'EMAIL'],
            ['ID Cuenta o Nro. de Asig. (0)', "Email (16)"],
            dataframe_saver,
        )
        print(f'{len(mails)} MAILS se guardaron en archivo: subida_mail.csv\n\n')
