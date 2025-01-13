from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

class AgenteAduanal(models.Model):
    patente = models.CharField(
        primary_key=True,
        max_length=4,
        validators=[MinLengthValidator(4), MaxLengthValidator(4)]
    )
    nombre = models.CharField(max_length=80, null=True)
    razon_social = models.CharField(max_length=80, null=True)
    rfc = models.CharField(max_length=20, null=True)
    curp = models.CharField(max_length=18, null=True)
    direccion1 = models.CharField(max_length=60, null=True)
    direccion2 = models.CharField(max_length=60, null=True)
    direccion3 = models.CharField(max_length=60, null=True)
    serie = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.patente} - {self.nombre}"

    class Meta:
        verbose_name_plural = "Agentes Aduanales"

class AduanaSeccion(models.Model):
    cve_aduana = models.CharField(max_length=2)
    cve_seccion = models.CharField(max_length=1)
    descripcion = models.CharField(max_length=60, null=True)

    class Meta:
        unique_together = ('cve_aduana', 'cve_seccion')

    def __str__(self):
        return f"{self.cve_aduana}-{self.cve_seccion} {self.descripcion}"

class ClavePedimento(models.Model):
    cve_pedimento = models.CharField(primary_key=True, max_length=3)
    descripcion = models.CharField(max_length=120, null=True)
    importacion = models.BooleanField()
    exportacion = models.BooleanField()

    def __str__(self):
        return f"{self.cve_pedimento} - {self.descripcion}"

class Pedimento(models.Model):
    TIPO_OPERACION_CHOICES = [
        (1, 'Importación'),
        (2, 'Exportación'),
    ]

    num_pedimento = models.CharField(primary_key=True, max_length=15)
    tipo_operacion = models.IntegerField(choices=TIPO_OPERACION_CHOICES)
    aduana_seccion = models.ForeignKey(
        AduanaSeccion,
        on_delete=models.PROTECT,
        to_field='id'
    )
    patente = models.ForeignKey(
        AgenteAduanal,
        on_delete=models.PROTECT,
        to_field='patente'
    )
    clave_pedimento = models.ForeignKey(
        ClavePedimento,
        on_delete=models.PROTECT,
        to_field='cve_pedimento'
    )
    fecha_entrada = models.DateField()
    fecha_pago = models.DateField(null=True)

    def __str__(self):
        return self.num_pedimento
