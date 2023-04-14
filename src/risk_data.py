import pandas as pd
from constants.constants import NUMBER_OF_COLUMNS
from write_data_osiris import Escribir_Datos_Osiris


def get_phone_risk(df_risk: pd.DataFrame) -> pd.DataFrame:
    frames = list()
    num_tel = len([col_name for col_name in list(df_risk.columns) if 'tel_riesgo' in col_name])
    for i in range(1, num_tel + 1):
        col_riesgo = f'tel_riesgo_{i}'
        df = df_risk.loc[df_risk[col_riesgo].notnull(), ['Cuenta', col_riesgo]]\
            .rename(columns={col_riesgo: 'TEL'}).copy()
        df['OBS'] = f'RIESGO {i}'
        df['ID_FONO'] = '8'
        frames.append(df)
    df_phone_risk = pd.concat(frames)
    return df_phone_risk


def read_osiris_accounts() -> pd.DataFrame:
    try:
        uploaded_accounts = pd.read_csv('cuentas.csv', encoding='latin_1', sep=';', dtype=str)
    except Exception:
        uploaded_accounts = pd.read_csv('cuentas.csv', encoding='ANSI', sep=';', dtype=str)
    uploaded_accounts = uploaded_accounts[['Cuenta', 'Mat. Unica']].rename(
        columns={
            'Mat. Unica': 'DNI'
            },
        inplace=False
        )
    return uploaded_accounts


def risk_data():
    'NECESARIOS: tener el archivos.csv de riesgo y el archivo de las cuentas de osiris como cuentas.csv'
    col_numbers = {
        'NÃºmero.1': 'tel_riesgo_1',
        'NÃºmero.2': 'tel_riesgo_2',
        'NÃºmero.3': 'tel_riesgo_3',
        'NÃºmero.4': 'tel_riesgo_4'
    }

    col_list = [x for x in range(NUMBER_OF_COLUMNS)]
    try:
        risk = pd.read_csv('riesgo.csv', sep=';', encoding='latin_1', dtype=str, index_col=False, usecols=col_list)
    except Exception:
        risk = pd.read_csv('riesgo.csv', sep=';', encoding='ANSI', dtype=str, index_col=False, usecols=col_list)
    df_risk = risk[['DNI'] + list(col_numbers.keys()) + ['NSE']]

    df_risk = df_risk.rename(columns=col_numbers, inplace=False)

    uploaded_accounts = read_osiris_accounts()

    df_risk = pd.merge(uploaded_accounts, df_risk, how="inner", on="DNI")

    df_phone_risk = get_phone_risk(df_risk=df_risk)

    Escribir_Datos_Osiris(
        df_phone_risk,
        'RIESGO_telefonos.csv',
        ['Cuenta', 'ID_FONO', 'TEL', 'OBS'],
        ["ID Cuenta o Nro. de Asig. (0)", "ID Tipo de Teléfono (17)", "Nro. de Teléfono (18)", "Obs. de Teléfono (19)"]
    )
    print('Planilla de Teléfonos de RIESGO escrita')
