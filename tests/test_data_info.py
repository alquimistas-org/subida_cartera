import numpy as np
import pandas as pd
from unittest.mock import patch
import pytest
from src.data_info import GenerateDataInfo


@pytest.mark.parametrize(
    'mock_df_data_info',
    [
        (
            pd.DataFrame(
                {
                    'Cuenta': '1234',
                    'DNI': '23345',
                    'tel_info_1': '122233334',
                    'tel_info_2': '',
                    'tel_info_3': '',
                    'MAIL_info': 'mock@mail.com',
                    'sueldo_info': '10000',
                    'empleador_info': 'Super Empleador',
                    'q_vehiculos': '',
                    'detalle_veh': '',
                    'NSE_info': '',
                },
                index=[0]
            )
        )
    ]
)
class TestDataInfo:

    @patch('src.data_info.read_osiris_accounts')
    @patch('pandas.read_excel')
    def test_get_data_info(self, mock_read_excel, mock_read_osiris_accounts, mock_df_data_info):

        mock_read_excel.return_value = pd.DataFrame(
            {
                'NUMERO DOCUMENTO': '23345',
                'NUMERO 1': '122233334',
                'NUMERO 2': '',
                'NUMERO 3': '',
                'E-MAIL': 'mock@mail.com',
                'REMUNERACION': '10000',
                'RAZON SOCIAL': 'Super Empleador',
                'CANTIDAD.2': '',
                'DETALLE.1': '',
                'NSE': '',
            },
            index=[0]
        )
        mock_read_osiris_accounts.return_value = pd.DataFrame(
            {
                'Cuenta': '1234',
                'DNI': '23345',
            },
            index=[0]
        )

        df = GenerateDataInfo.get_data_info()
        expected = mock_df_data_info

        pd.testing.assert_frame_equal(df, expected)

    @patch('src.data_info.Escribir_Datos_Osiris')
    def test_write_phone_template(self, mock_write_data_osiris, mock_df_data_info):

        GenerateDataInfo.write_phone_template(df=mock_df_data_info)

        expected_df_phones = pd.DataFrame(
            {
                'Cuenta': pd.Series(['1234', '1234']),
                'ID_FONO': pd.Series(['8', '8']),
                'TEL': pd.Series(['122233334']),
                'OBS': pd.Series(['INFO 1', 'INFO 2']),
            }
        )
        expected_df_phones = expected_df_phones.fillna('')

        # asserts
        mock_write_data_osiris.assert_called_once()
        call_args = mock_write_data_osiris.call_args_list[0][0]
        pd.testing.assert_frame_equal(call_args[0], expected_df_phones)
        assert call_args[1] == 'INFO_telefonos.csv'
        assert call_args[2] == ['Cuenta', 'ID_FONO', 'TEL', 'OBS']
        assert call_args[3] == [
                "ID Cuenta o Nro. de Asig. (0)",
                "ID Tipo de Teléfono (17)",
                "Nro. de Teléfono (18)",
                "Obs. de Teléfono (19)"
            ]

    @patch('src.data_info.Escribir_Datos_Osiris')
    def test_write_salary_template(self, mock_write_data_osiris, mock_df_data_info):

        GenerateDataInfo.write_salary_template(mock_df_data_info)
        expected_df_info = pd.DataFrame(
            {
                'Cuenta': '1234',
                'sueldo_info': '10000',
            },
            index=[0]
        )

        # asserts
        mock_write_data_osiris.assert_called_once()
        call_args = mock_write_data_osiris.call_args_list[0][0]
        pd.testing.assert_frame_equal(call_args[0], expected_df_info)
        assert call_args[1] == 'INFO_sueldo.csv'
        assert call_args[2] == ['Cuenta', 'sueldo_info']
        assert call_args[3] == ["ID Cuenta o Nro. de Asig. (0)", "Sueldo (40)"]

    @patch('src.data_info.Escribir_Datos_Osiris')
    @patch.object(GenerateDataInfo, 'get_emails')
    def test_write_email_template(self, mock_get_emails, mock_write_data_osiris, mock_df_data_info):

        mock_get_emails.return_value = pd.DataFrame(
                {
                    'Cuenta': '1234',
                    'MAIL_info': 'mock@mail.com'
                },
                index=[0]
            )

        GenerateDataInfo.write_email_template(df=mock_df_data_info)

        # asserts
        mock_write_data_osiris.assert_called_once()
        call_args = mock_write_data_osiris.call_args_list[0][0]
        pd.testing.assert_frame_equal(call_args[0], mock_get_emails.return_value)
        assert call_args[1] == 'INFO_mail.csv'
        assert call_args[2] == ['Cuenta', 'MAIL_info']
        assert call_args[3] == ["ID Cuenta o Nro. de Asig. (0)", "Email (16)"]

    @patch('src.data_info.Escribir_Datos_Osiris')
    def test_write_q_vehicles_template(self, mock_write_data_osiris, mock_df_data_info):

        GenerateDataInfo.write_q_vehicles_template(df=mock_df_data_info)
        expected_df_info = pd.DataFrame(
            {
                'Cuenta': '1234',
                'q_vehiculos': '',
            },
            index=[0]
        )

        # asserts
        mock_write_data_osiris.assert_called_once()
        call_args = mock_write_data_osiris.call_args_list[0][0]
        pd.testing.assert_frame_equal(call_args[0], expected_df_info)
        assert call_args[1] == 'INFO_Qvehiculos.csv'
        assert call_args[2] == ['Cuenta', 'q_vehiculos']
        assert call_args[3] == ["ID Cuenta o Nro. de Asig. (0)", "Cantidad de Vehiculos (41)"]

    @patch('src.data_info.Escribir_Datos_Osiris')
    def test_write_patrimonial_data_template(self, mock_write_data_osiris, mock_df_data_info):

        mock_df = pd.DataFrame(
            {
                'Cuenta': pd.Series([f'{i}234' for i in range(1, 15)]),
                'DNI': pd.Series([f'{i}333222' for i in range(1, 15)]),
                'tel_info_1': pd.Series([f'{i}555777' for i in range(1, 15)]),
                'tel_info_2': pd.Series([None for i in range(1, 15)]),
                'tel_info_3': pd.Series([None for i in range(1, 15)]),
                'MAIL_info': pd.Series([[f'mock{i}@mail.com'] for i in range(1, 15)]),
                'sueldo_info': pd.Series([f'{i}0000' for i in range(1, 15)]),
                'empleador_info': pd.Series([f'Super Empleador {i}' for i in range(1, 15)]),
                'q_vehiculos': pd.Series([f'{i}' for i in range(1, 15)]),
                'detalle_veh': pd.Series([f'Auto {i}' for i in range(1, 15)]),
                'NSE_info': pd.Series([np.NaN for i in range(1, 15)]),
            }
        )
        GenerateDataInfo.write_patrimonial_data_template(df=mock_df)
        expected_df = pd.DataFrame(
            {
                'Cuenta': pd.Series(
                    [
                        '1234',
                        '2234',
                        '3234',
                        '4234',
                        '5234',
                        '6234',
                        '7234',
                        '8234',
                        '9234',
                        '10234',
                        '11234',
                        '12234',
                        '13234',
                        '14234'
                    ]
                ),
                'primonial': pd.Series(
                    [
                        'Sueldo: $10,000, 0 Empleador: Super Empleador 1 - Cantidad de Vehículos: 1 Detalle: Auto 1',
                        'Sueldo: $20,000, 0 Empleador: Super Empleador 2 - Cantidad de Vehículos: 2 Detalle: Auto 2',
                        'Sueldo: $30,000, 0 Empleador: Super Empleador 3 - Cantidad de Vehículos: 3 Detalle: Auto 3',
                        'Sueldo: $40,000, 0 Empleador: Super Empleador 4 - Cantidad de Vehículos: 4 Detalle: Auto 4',
                        'Sueldo: $50,000, 0 Empleador: Super Empleador 5 - Cantidad de Vehículos: 5 Detalle: Auto 5',
                        'Sueldo: $60,000, 0 Empleador: Super Empleador 6 - Cantidad de Vehículos: 6 Detalle: Auto 6',
                        'Sueldo: $70,000, 0 Empleador: Super Empleador 7 - Cantidad de Vehículos: 7 Detalle: Auto 7',
                        'Sueldo: $80,000, 0 Empleador: Super Empleador 8 - Cantidad de Vehículos: 8 Detalle: Auto 8',
                        'Sueldo: $90,000, 0 Empleador: Super Empleador 9 - Cantidad de Vehículos: 9 Detalle: Auto 9',
                        'Sueldo: $100,000, 0 Empleador: Super Empleador 10 - Cantidad de Vehículos: 10 Detalle: Auto 10',  # noqa
                        'Sueldo: $110,000, 0 Empleador: Super Empleador 11 - Cantidad de Vehículos: 11 Detalle: Auto 11',  # noqa                   
                        'Sueldo: $120,000, 0 Empleador: Super Empleador 12 - Cantidad de Vehículos: 12 Detalle: Auto 12',  # noqa                  
                        'Sueldo: $130,000, 0 Empleador: Super Empleador 13 - Cantidad de Vehículos: 13 Detalle: Auto 13',  # noqa                   
                        'Sueldo: $140,000, 0 Empleador: Super Empleador 14 - Cantidad de Vehículos: 14 Detalle: Auto 14',  # noqa
                    ]
                ),
            },
        )

        # asserts
        mock_write_data_osiris.assert_called_once()
        call_args = mock_write_data_osiris.call_args_list[0][0]
        pd.testing.assert_frame_equal(call_args[0], expected_df)
        assert call_args[1] == 'INFO_Patrimoniales.csv'
        assert call_args[2] == ['Cuenta', 'primonial']
        assert call_args[3] == ["ID Cuenta o Nro. de Asig. (0)", "Datos Patrimoniales (42)"]

    def test_get_emails(self, mock_df_data_info):
        result = GenerateDataInfo.get_emails(df=mock_df_data_info)
        expected = pd.DataFrame(
            {
                'Cuenta': '1234',
                'MAIL_info': 'mock@mail.com'
            },
            index=[0]
        )

        pd.testing.assert_frame_equal(result, expected)

    @patch.object(GenerateDataInfo, 'write_patrimonial_data_template')
    @patch.object(GenerateDataInfo, 'write_q_vehicles_template')
    @patch.object(GenerateDataInfo, 'write_email_template')
    @patch.object(GenerateDataInfo, 'write_salary_template')
    @patch.object(GenerateDataInfo, 'write_phone_template')
    @patch.object(GenerateDataInfo, 'get_data_info')
    def test_process(
        self,
        mock_get_data_info,
        mock_write_phone_template,
        mock_write_salary_template,
        mock_write_email_template,
        mock_write_q_vehicles_template,
        mock_write_patrimonial_data_template,
        mock_df_data_info,
    ):
        mock_get_data_info.return_value = mock_df_data_info

        GenerateDataInfo.process()

        # asserts
        mock_write_phone_template.assert_called_once()
        mock_write_salary_template.assert_called_once()
        mock_write_email_template.assert_called_once()
        mock_write_q_vehicles_template.assert_called_once()
        mock_write_patrimonial_data_template.assert_called_once()
