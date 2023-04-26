import numpy as np
import pandas as pd

from constants.constants import (
    DATA_INFO_COLUMNS,
    DATA_INFO_COLUMNS_RENAME,
    OSIRIS_ACCOUNTS_FILE_PATH,
)
from risk_data import (
    get_phones,
    read_osiris_accounts,
)
from write_data_osiris import Escribir_Datos_Osiris


class GenerateDataInfo:

    info_experto_file_path = 'info.xlsx'
    osiris_accounts_file_path = OSIRIS_ACCOUNTS_FILE_PATH

    @classmethod
    def get_data_info(cls) -> pd.DataFrame:
        'NECESARIO cuentas de osiris como cuentas.csv, cuentas deinfo exporto como info.xlsx'
        uploaded_accounts = read_osiris_accounts(cls.osiris_accounts_file_path)

        info = pd.read_excel(cls.info_experto_file_path, dtype=str, skiprows=1)
        df_info = info[DATA_INFO_COLUMNS]
        df_info = df_info.rename(columns=DATA_INFO_COLUMNS_RENAME, inplace=False).copy()
        df_info['q_vehiculos'] = df_info['q_vehiculos'].fillna('0')

        df_info = pd.merge(uploaded_accounts, df_info, how="inner", on="DNI")
        return df_info

    @classmethod
    def write_phone_template(cls, df: pd.DataFrame) -> None:
        df_phones = get_phones(
            df=df,
            stop=3,
            colum_name='INFO'
        )

        file_path = Escribir_Datos_Osiris(
            df_phones[['Cuenta', 'ID_FONO', 'TEL', 'OBS']],
            'info_telefonos.csv',
            ['Cuenta', 'ID_FONO', 'TEL', 'OBS'],
            [
                "ID Cuenta o Nro. de Asig. (0)",
                "ID Tipo de Teléfono (17)",
                "Nro. de Teléfono (18)",
                "Obs. de Teléfono (19)"
            ]
        )

        print('Planilla de TELEFONOS de INFO escrita')
        return file_path

    @classmethod
    def write_salary_template(cls, df: pd.DataFrame) -> None:

        file_path = Escribir_Datos_Osiris(
            df.loc[df['sueldo_info'].notnull(), ['Cuenta', 'sueldo_info']],
            'info_sueldo.csv',
            ['Cuenta', 'sueldo_info'],
            ["ID Cuenta o Nro. de Asig. (0)", "Sueldo (40)"]
        )
        print('Planilla de SUELDOS de INFO escrita')
        return file_path

    @classmethod
    def write_email_template(cls, df: pd.DataFrame) -> None:
        emails = cls.get_emails(df=df)

        file_path = Escribir_Datos_Osiris(
            emails,
            'info_mail.csv',
            ['Cuenta', 'MAIL_info'],
            ["ID Cuenta o Nro. de Asig. (0)", "Email (16)"]
        )
        print('Planilla de MAIL de INFO escrita')
        return file_path

    @classmethod
    def write_q_vehicles_template(cls, df: pd.DataFrame) -> None:

        file_path = Escribir_Datos_Osiris(
            df.loc[df['q_vehiculos'] != '0', ['Cuenta', 'q_vehiculos']],
            'info_q_vehiculos.csv',
            ['Cuenta', 'q_vehiculos'],
            ["ID Cuenta o Nro. de Asig. (0)", "Cantidad de Vehiculos (41)"]
        )

        print('Planilla de Q VEHICULOS de INFO escrita')
        return file_path

    @classmethod
    def write_patrimonial_data_template(cls, df: pd.DataFrame) -> None:

        df = cls.apply_salary_template(df=df)

        # borrando sueldo 0
        df.loc[df['sueldo_info'].isnull(), 'primonial'] = df.loc[
            df['sueldo_info'].isnull(), 'primonial'].str.replace('Sueldo: $nan ', '', regex=False)
        df.loc[df['empleador_info'].isnull(), 'primonial'] = df.loc[
            df['empleador_info'].isnull(), 'primonial'].str.replace('Empleador: nan - ', '', regex=False)
        df.loc[df['q_vehiculos'] == '0', 'primonial'] = df.loc[
            df['q_vehiculos'] == '0', 'primonial'].str.replace('Cantidad de Vehículos: 0 ', '', regex=False)
        df.loc[df['detalle_veh'].isnull(), 'primonial'] = df.loc[
            df['detalle_veh'].isnull(), 'primonial'].str.replace('Detalle: nan - ', '', regex=False)
        df.loc[df['NSE_info'].isnull(), 'primonial'] = df.loc[df['NSE_info'].isnull(), 'primonial']\
            .str.replace(' - Nivel Socioeconómico: nan', '', regex=False)
        df.loc[df['NSE_info'].isnull(), 'primonial'] = df.loc[df['NSE_info'].isnull(), 'primonial']\
            .str.replace('Nivel Socioeconómico: nan', '', regex=False)

        df.loc[
            (df['sueldo_info'].isnull()) &
            (df['empleador_info'].isnull()) &
            (df['q_vehiculos'] == '0') &
            (df['detalle_veh'].isnull()) &
            (df['NSE_info'].isnull()), 'primonial'
        ] = np.nan
        df[['Cuenta', 'q_vehiculos', 'detalle_veh', 'primonial']].iloc[10]

        file_path = Escribir_Datos_Osiris(
            df.loc[df['primonial'].notnull(), ['Cuenta', 'primonial']],
            'info_patrimoniales.csv',
            ['Cuenta', 'primonial'],
            ["ID Cuenta o Nro. de Asig. (0)", "Datos Patrimoniales (42)"]
        )
        print('Planilla de DATOS PATRIMONIALES de INFO escrita')
        return file_path

    @classmethod
    def apply_salary_template(cls, df: pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()

        plantilla = (
            'Sueldo: ${sueldo_info_str} Empleador: {empleador_info} - '
            'Cantidad de Vehículos: {q_vehiculos} Detalle: {detalle_veh} - Nivel Socioeconómico: {NSE_info}'
        )
        df_copy['sueldo_info_float'] = df_copy['sueldo_info'].astype({'sueldo_info':  'float'})
        df_copy.loc[df_copy['sueldo_info'].notnull(), 'sueldo_info_int'] = df_copy.loc[
            df_copy['sueldo_info'].notnull(), 'sueldo_info_float'
            ].astype({'sueldo_info_float': 'int32'})

        df_copy['sueldo_info_str'] = df_copy['sueldo_info_int']\
            .apply(lambda row: "{:,}".format(row).replace(", ", "@").replace('.', ', ').replace('@', '.'))

        df_copy['primonial'] = df_copy.apply(lambda row: plantilla.format(**row.to_dict()), axis=1)

        return df_copy

    @classmethod
    def get_emails(cls, df: pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()
        mails = df_copy.loc[df_copy['MAIL_info'].notnull(), 'MAIL_info'].str.split(', ', expand=True)
        rename = {x: f'mail_{i+1}' for i, x in enumerate(list(mails.columns), 0)}
        mails = mails.rename(columns=rename)
        name_mails = list(rename.values())
        df_copy[name_mails] = mails[name_mails]
        concat_mails = list()
        for name in name_mails:
            concat_mails.append(df_copy.loc[df_copy[name].notnull(), ['Cuenta', name]].rename(
                columns={name: 'MAIL_info'}
                ))
        return pd.concat(concat_mails)

    @classmethod
    def process(cls) -> list:
        df = cls.get_data_info()
        phone_result_path_file = cls.write_phone_template(df=df)
        salary_result_path_file = cls.write_salary_template(df=df)
        email_result_path_file = cls.write_email_template(df=df)
        q_vehicles_result_path_file = cls.write_q_vehicles_template(df=df)
        patrimonial_result_path_file = cls.write_patrimonial_data_template(df=df)

        all_result_file_paths = [
            phone_result_path_file,
            salary_result_path_file,
            email_result_path_file,
            q_vehicles_result_path_file,
            patrimonial_result_path_file
        ]
        return all_result_file_paths
