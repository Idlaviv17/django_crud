from django.test import TestCase
from django.core.exceptions import ValidationError
from customs_app.forms import (
    AgenteAduanalForm,
    PedimentoForm,
    AduanaSeccionForm,
    ClavePedimentoForm
)
from customs_app.models import AgenteAduanal, Pedimento, AduanaSeccion, ClavePedimento
from datetime import date

class AgenteAduanalFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'patente': '1234',
            'nombre': 'Test Agente',
            'razon_social': 'Test Agente SA de CV',
            'rfc': 'TEST123456ABC',
            'curp': 'CURP123456HDFXXX01',
            'direccion1': 'Calle Test 123',
            'direccion2': 'Col. Test',
            'direccion3': 'Ciudad Test',
            'serie': 'A1'
        }

    def test_valid_form(self):
        """Test form with valid data"""
        form = AgenteAduanalForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_patente(self):
        """Test form with invalid patent number"""
        invalid_data = self.valid_data.copy()
        invalid_data['patente'] = '123'
        form = AgenteAduanalForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('patente', form.errors)
        self.assertEqual(
            form.errors['patente'][0],
            'El número de patente debe tener 4 caracteres.'
        )

    def test_optional_fields(self):
        """Test that most fields are optional"""
        minimal_data = {
            'patente': '1234'
        }
        form = AgenteAduanalForm(data=minimal_data)
        self.assertTrue(form.is_valid())

    def test_field_max_lengths(self):
        """Test field maximum length constraints"""
        invalid_data = self.valid_data.copy()
        invalid_data['nombre'] = 'x' * 81
        form = AgenteAduanalForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

class AduanaSeccionFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'cve_aduana': '47',
            'cve_seccion': '1',
            'descripcion': 'Test Aduana'
        }
        
    def test_valid_form(self):
        """Test form with valid data"""
        form = AduanaSeccionForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_cve_aduana(self):
        """Test invalid aduana code length"""
        invalid_data = self.valid_data.copy()
        invalid_data['cve_aduana'] = '1'
        form = AduanaSeccionForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_invalid_cve_seccion(self):
        """Test invalid section code length"""
        invalid_data = self.valid_data.copy()
        invalid_data['cve_seccion'] = '11'
        form = AduanaSeccionForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_descripcion_optional(self):
        """Test that descripcion is optional"""
        data = self.valid_data.copy()
        del data['descripcion']
        form = AduanaSeccionForm(data=data)
        self.assertTrue(form.is_valid())

class ClavePedimentoFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'cve_pedimento': 'A1',
            'descripcion': 'Test Clave',
            'importacion': True,
            'exportacion': False
        }

    def test_valid_form(self):
        """Test form with valid data"""
        form = ClavePedimentoForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_cve_pedimento(self):
        """Test invalid pedimento code length"""
        invalid_data = self.valid_data.copy()
        invalid_data['cve_pedimento'] = 'A'
        form = ClavePedimentoForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['cve_pedimento'][0],
            'La clave de pedimento debe tener al menos 2 caracteres.'
        )

    def test_descripcion_optional(self):
        """Test that descripcion is optional"""
        data = self.valid_data.copy()
        del data['descripcion']
        form = ClavePedimentoForm(data=data)
        self.assertTrue(form.is_valid())

class PedimentoFormTests(TestCase):
    def setUp(self):
        self.agente = AgenteAduanal.objects.create(
            patente="1234",
            nombre="Test Agente"
        )
        self.aduana = AduanaSeccion.objects.create(
            cve_aduana="47",
            cve_seccion="1",
            descripcion="Test Aduana"
        )
        self.clave = ClavePedimento.objects.create(
            cve_pedimento="A1",
            descripcion="Test Clave",
            importacion=True,
            exportacion=False
        )
        
        self.valid_data = {
            'num_pedimento': '123456789012345',
            'tipo_operacion': 1,
            'aduana_seccion': self.aduana.pk,
            'patente': self.agente.patente,
            'clave_pedimento': self.clave.cve_pedimento,
            'fecha_entrada': '2024-01-14',
            'fecha_pago': '2024-01-14'
        }

    def test_valid_form(self):
        """Test form with valid data"""
        form = PedimentoForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_num_pedimento(self):
        """Test form with invalid pedimento number"""
        invalid_data = self.valid_data.copy()
        invalid_data['num_pedimento'] = '12345'
        form = PedimentoForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['num_pedimento'][0],
            'El número de pedimento debe tener 15 caracteres.'
        )

    def test_optional_fecha_pago(self):
        """Test that fecha_pago is optional"""
        data = self.valid_data.copy()
        del data['fecha_pago']
        form = PedimentoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        """Test that required fields are enforced"""
        form = PedimentoForm(data={})
        self.assertFalse(form.is_valid())
        required_fields = ['num_pedimento', 'tipo_operacion', 'aduana_seccion', 
                         'patente', 'clave_pedimento', 'fecha_entrada']
        for field in required_fields:
            self.assertIn(field, form.errors)