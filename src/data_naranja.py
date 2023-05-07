from pathlib import Path

import numpy as np
import pandas as pd


from .constants.constants import (
    CR_FILE_PATH,
    DATA_PREP_COLUMNS,
    OSIRIS_ACCOUNTS_FILE_PATH,
)
from .write_data_osiris import Escribir_Datos_Osiris


class GenerateDataNaranja:

    @classmethod
    def process(cls, cr_file_path=CR_FILE_PATH, osiris_accounts_file_path=OSIRIS_ACCOUNTS_FILE_PATH):
        print('Preparando planillas de datos...')

        cr = cls._get_cr_data(cr_file_path, osiris_accounts_file_path)

        phones = cls._get_all_pones_together_df_from_cr(cr)

        cleaned_phones = cls._clean_phone_numbers(phones)
        result_phones_file_path = cls._write_phones_data_result(cleaned_phones)

        mails = cls._get_mails_from_cr(cr)
        result_mails_file_path = cls._write_mail_data_results(mails)
        all_result_file_paths = [result_phones_file_path, result_mails_file_path]
        return all_result_file_paths

    @staticmethod
    def _get_cr_data(cr_file_path, osiris_accounts_file_path) -> pd.DataFrame:
        try:
            cr = pd.read_csv(cr_file_path, sep=';', encoding='latin_1', dtype=str)
            osiris_accounts = pd.read_csv(osiris_accounts_file_path, encoding='latin_1', sep=';', dtype=str)
        except Exception:
            cr = pd.read_csv(cr_file_path, sep=';', encoding='ANSI', dtype=str)
            osiris_accounts = pd.read_csv(osiris_accounts_file_path, encoding='ANSI', sep=';', dtype=str)

        osiris_accounts = osiris_accounts[['Cuenta', 'Mat. Unica']].rename(
            columns={'Mat. Unica': 'DNI'}, inplace=False
        )

        df_cr = cr[DATA_PREP_COLUMNS].rename(columns={'NRODOC': 'DNI'}, inplace=False).copy()
        df_cr = pd.merge(osiris_accounts, df_cr, how="inner", on="DNI")
        return df_cr

    @staticmethod
    def _get_all_pones_together_df_from_cr(cr_df: pd.DataFrame) -> pd.DataFrame:
        print('Subiendo numeros...\n')
        print('----------------------')

        frames = list()
        # MASIVOS

        # paso TEL_ALTERNATIVO esta vacio
        df = cr_df.loc[
            cr_df['TEL_ALTERNATIVO'].notnull(), ['Cuenta', 'TEL_ALTERNATIVO']
        ].rename(columns={'TEL_ALTERNATIVO': 'TEL'}, inplace=False).copy()
        df['ID_FONO'] = '1'
        print(f'{len(df)} Telefonos ALTERNATIVOS cargados com MASIVOS')
        frames.append(df)

        # paso TEL_PARTICULAR como masivo.
        df = cr_df.loc[
            cr_df['TEL_ALTERNATIVO'].isnull() & cr_df['TEL_PARTICULAR'].notnull(), ['Cuenta', 'TEL_PARTICULAR']
        ].rename(columns={'TEL_PARTICULAR': 'TEL'}, inplace=False).copy()

        cr_df.loc[cr_df['TEL_ALTERNATIVO'].isnull() & cr_df['TEL_PARTICULAR'].notnull(), 'TEL_PARTICULAR'] = np.nan
        df['ID_FONO'] = '1'
        print(f'{len(df)} Telefonos PARTICULAR cargados com MASIVOS en cuentas que no poseen ALTERNATIVO')
        frames.append(df)

        # FIJOS
        df = cr_df.loc[cr_df['TEL_PARTICULAR'].notnull(), ['Cuenta', 'TEL_PARTICULAR']]\
            .rename(columns={'TEL_PARTICULAR': 'TEL'}, inplace=False).copy()
        df['ID_FONO'] = '2'
        print(f'{len(df)} Telefonos ALTERNATIVOS cargados como FIJOS')
        frames.append(df)

        # LABORALES
        df = cr_df.loc[
            cr_df['TEL_LABORAL'].notnull(), ['Cuenta', 'TEL_LABORAL']
        ].rename(columns={'TEL_LABORAL': 'TEL'}, inplace=False).copy()
        df['ID_FONO'] = '3'
        print(f'{len(df)} Telefonos LABORALES cargados como LABORALES')
        frames.append(df)

        # OTROS
        df = cr_df.melt(
            id_vars=['Cuenta'], value_vars=['TEL_CR_PARTICULAR', 'TEL_CR_LABORAL', 'TEL_CR_ALTERNATIVO']
            ).dropna().copy()
        df = df[['Cuenta', 'value']].rename(columns={'value': 'TEL'}, inplace=False)
        df['ID_FONO'] = '8'
        print(f'{len(df)} Telefonos OTROS_CR cargados como OTROS')
        frames.append(df)
        print('----------------------\n')

        phones_df = pd.concat(frames)
        return phones_df

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
    def _write_phones_data_result(cleaned_phones_df: pd.DataFrame) -> Path:
        result_df_phones_file_path = Escribir_Datos_Osiris(
            cleaned_phones_df,
            'datos_cr_subida_telefonos.csv',
            ['Cuenta', 'ID_FONO', 'TEL'],
            ['ID Cuenta o Nro. de Asig. (0)', "ID Tipo de Teléfono (17)", "Nro. de Teléfono (18)"]
        )
        print(f'{len(cleaned_phones_df)} TELEFONOS se guardaron en archivo: subida_telefono.csv')
        return result_df_phones_file_path

    @staticmethod
    def _get_mails_from_cr(cr: pd.DataFrame) -> pd.DataFrame:
        cr.loc[cr['EMAIL'].notnull(), 'EMAIL'] = cr.loc[cr['EMAIL'].notnull(), 'EMAIL'].str.replace(' ', '')
        mails = cr.loc[cr['EMAIL'].notnull(), ['Cuenta', 'EMAIL']].copy()
        return mails

    @staticmethod
    def _write_mail_data_results(mails: pd.DataFrame) -> Path:
        result_df_mails_file_path = Escribir_Datos_Osiris(
            mails,
            'datos_cr_subida_mail.csv',
            ['Cuenta', 'EMAIL'],
            ['ID Cuenta o Nro. de Asig. (0)', "Email (16)"]
        )
        print(f'{len(mails)} MAILS se guardaron en archivo: subida_mail.csv\n\n')
        return result_df_mails_file_path
