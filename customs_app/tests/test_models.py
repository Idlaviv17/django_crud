from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from customs_app.models import AgenteAduanal, Pedimento, AduanaSeccion, ClavePedimento
from datetime import date

class AgenteAduanalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.agente = AgenteAduanal.objects.create(
            patente="1234",
            nombre="Test Agente",
            rfc="TEST123456ABC",
            curp="CURP123456HDFXXX01",
            razon_social="Test Agente SA de CV",
            direccion1="Calle Test 123",
            serie="A1"
        )

    def test_agente_creation(self):
        """Test basic agent creation"""
        self.assertTrue(isinstance(self.agente, AgenteAduanal))
        self.assertEqual(self.agente.__str__(), "1234 - Test Agente")

    def test_patente_validation(self):
        """Test patent number validation"""
        with self.assertRaises(ValidationError):
            agente = AgenteAduanal(
                patente="123",
                nombre="Test Invalid"
            )
            agente.full_clean()

    def test_rfc_validation(self):
        """Test RFC format validation"""
        agente = AgenteAduanal.objects.create(
            patente="5678",
            nombre="Test RFC",
            rfc="INVALID-RFC"
        )
        with self.assertRaises(ValidationError):
            agente.full_clean()

class PedimentoTests(TestCase):
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
        self.pedimento = Pedimento.objects.create(
            num_pedimento="1234567890123",
            tipo_operacion=1,
            aduana_seccion=self.aduana,
            patente=self.agente,
            clave_pedimento=self.clave,
            fecha_entrada=date.today()
        )

    def test_pedimento_creation(self):
        """Test basic pedimento creation"""
        self.assertTrue(isinstance(self.pedimento, Pedimento))
        self.assertEqual(self.pedimento.__str__(), "1234567890123")

    def test_pedimento_validation(self):
        """Test pedimento number validation"""
        with self.assertRaises(ValidationError):
            pedimento = Pedimento(
                num_pedimento="123",
                tipo_operacion=1,
                aduana_seccion=self.aduana,
                patente=self.agente,
                clave_pedimento=self.clave,
                fecha_entrada=date.today()
            )
            pedimento.full_clean()

    def test_tipo_operacion_choices(self):
        """Test operation type choices"""
        pedimento = Pedimento.objects.create(
            num_pedimento="9876543210123",
            tipo_operacion=1,  # Should be 1 or 2
            aduana_seccion=self.aduana,
            patente=self.agente,
            clave_pedimento=self.clave,
            fecha_entrada=date.today()
        )
        self.assertIn(pedimento.tipo_operacion, [1, 2])

class AduanaSeccionTests(TestCase):
    def setUp(self):
        self.aduana = AduanaSeccion.objects.create(
            cve_aduana="47",
            cve_seccion="1",
            descripcion="Test Aduana"
        )

    def test_aduana_creation(self):
        """Test basic aduana creation"""
        self.assertTrue(isinstance(self.aduana, AduanaSeccion))
        self.assertEqual(self.aduana.__str__(), "47-1 Test Aduana")

    def test_unique_together_constraint(self):
        """Test unique together constraint for cve_aduana and cve_seccion"""
        with self.assertRaises(Exception):
            AduanaSeccion.objects.create(
                cve_aduana="47",
                cve_seccion="1",
                descripcion="Duplicate Test"
            )

class ClavePedimentoTests(TestCase):
    def setUp(self):
        self.clave = ClavePedimento.objects.create(
            cve_pedimento="A1",
            descripcion="Test Clave",
            importacion=True,
            exportacion=False
        )

    def test_clave_creation(self):
        """Test basic clave creation"""
        self.assertTrue(isinstance(self.clave, ClavePedimento))
        self.assertEqual(self.clave.__str__(), "A1 - Test Clave")

    def test_boolean_fields(self):
        """Test importacion and exportacion boolean fields"""
        self.assertTrue(self.clave.importacion)
        self.assertFalse(self.clave.exportacion)