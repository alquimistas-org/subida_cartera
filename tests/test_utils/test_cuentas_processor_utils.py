from freezegun import freeze_time
import pytest
import pandas as pd

from src.process_preparacion_cuentas import NARANJA_FIELDS
from src.utils.cuentas_processor_utils import (
    create_date,
    process_cuentas,
    )


@freeze_time("2023-05-04 18:45:00")
class TestCuentasProcessor():

    def test_create_date_current_date_with_parameter(self):
        year_to_add = 0
        excepted = '04/05/2023'
        current_date = create_date(year_to_add)
        assert excepted == current_date

    def test_create_date_current_date_without_parameter(self):

        excepted = '04/05/2023'
        current_date = create_date()
        assert excepted == current_date

    def test_create_date_with_positive_year_to_add(self):

        year_to_add = 3
        excepted = '04/05/2026'
        current_date = create_date(year_to_add)
        assert excepted == current_date

    def test_create_date_with_negative_year_to_add_raise_ValueError(self):
        year_to_add = -1
        with pytest.raises(ValueError):
            create_date(year_to_add)


@freeze_time("2023-05-04 18:45:00")
class TestProcessCuentas():

    ACCOUNT_COL = [
        'Nº de Asignacion (0)',
        'Razon social (1)',
        'ID Tipo de Documento (2)',
        'DNI (3)',
        'Domicilio (4)',
        'ID Localidad (5)',
        'ID Provincia (6)',
        'Código Postal (7)',
        'Importe Asignado (11)',
        'Fecha de Ingreso (12)',
        'Fecha de Deuda dd/mm/aaaa (13)',
        'Importe Historico (14)',
        'Observaciones (15)',
        'Fecha Fin de Gestion (16)',
        'IDSucursal(17)',
    ]

    cr = pd.DataFrame(
        {
            'NRODOC': ['12345678', '87654321'],
            'NOMBRECOMPLETO': ['Bruno Diaz', 'Ricardo Tapia'],
            'CALLE': ['Siempre Viva', 'Fake Street'],
            'NUMERO': ['1234', '4321'],
            'PISO': ['1', '2'],
            'DEPTO': ['a', 'b'],
            'BARRIO': ['Capital', 'Lujan'],
            'LOCALIDAD': ['Capital', 'Lujan'],
            'PROVINCIA': ['SAN JUAN', 'MENDOZA'],
            'POSTAL': ['5505', '5507'],
            'DEUDA_ACTUALIZADA': ['165644,54', '165644,54'],
            'INICIOMORA': ['22/03/2023', '22/03/2023'],
            'CAPITAL': ['165644,54', '165644,54'],
            'GESTOR_ANTERIOR': [
                'SERVICIOS INTEGRALES S.R.L.',
                'SERVICIOS INTEGRALES S.R.L.',
                ],
            'SCORE': ['0,1735', '0,1735'],
            'RIESGO': ['NAR-ALTO', 'NAR-MEDIO']
        }
    )

    expected = pd.DataFrame(
        {
            'Nº de Asignacion (0)': ['12345678', '87654321'],
            'Razon social (1)': ['Bruno Diaz', 'Ricardo Tapia'],
            'ID Tipo de Documento (2)': ['1', '1'],
            'DNI (3)': ['12345678', '87654321'],
            'Domicilio (4)': [
                "Siempre Viva 1234 - 1 a - Capital - Capital",
                'Fake Street 4321 - 2 b - Lujan - Lujan'
                ],
            'ID Localidad (5)': ['0', '0'],
            'ID Provincia (6)': ['7', '12'],
            'Código Postal (7)': ['5505', '5507'],
            'Importe Asignado (11)': ['165644.54', '165644.54'],
            'Fecha de Ingreso (12)': ['04/05/2023', '04/05/2023'],
            'Fecha de Deuda dd/mm/aaaa (13)': ['22/03/2023', '22/03/2023'],
            'Importe Historico (14)': ['165644.54', '165644.54'],
            'Observaciones (15)': [
                "Gestor anterior: SERVICIOS INTEGRALES S.R.L. - Score: 0.17",
                "Gestor anterior: SERVICIOS INTEGRALES S.R.L. - Score: 0.17",
                ],
            'Fecha Fin de Gestion (16)': ['04/05/2026', '04/05/2026'],
            'IDSucursal(17)': ['1', '1'],
            'riesgo': ['NAR-ALTO', 'NAR-MEDIO']
        }
    )

    def test_process_cuentas(self):
        result = process_cuentas(self.cr, NARANJA_FIELDS, self.ACCOUNT_COL)
        pd.testing.assert_frame_equal(self.expected, result)
