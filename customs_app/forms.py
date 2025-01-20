from django import forms
from django.core.exceptions import ValidationError
from .models import AgenteAduanal, Pedimento, AduanaSeccion, ClavePedimento

class AgenteAduanalForm(forms.ModelForm):
    patente = forms.CharField(label='Número de Patente')
    nombre = forms.CharField(label='Nombre', max_length=80, required=False)
    razon_social = forms.CharField(label='Razón Social', max_length=80, required=False)
    rfc = forms.CharField(label='RFC', max_length=20, required=False)
    curp = forms.CharField(label='CURP', max_length=18, required=False)
    direccion1 = forms.CharField(label='Dirección 1', max_length=60, required=False)
    direccion2 = forms.CharField(label='Dirección 2', max_length=60, required=False)
    direccion3 = forms.CharField(label='Dirección 3', max_length=60, required=False)
    serie = forms.CharField(label='Serie', max_length=30, required=False)

    class Meta:
        model = AgenteAduanal
        fields = '__all__'

    def clean_patente(self):
        patente = self.cleaned_data.get('patente')
        if len(patente) != 4:
            raise ValidationError('La patente debe contener exactamente 4 caracteres alfanuméricos.')
        return patente

class AduanaSeccionForm(forms.ModelForm):
    cve_aduana = forms.CharField(label='Clave de Aduana')
    cve_seccion = forms.CharField(label='Clave de Sección')
    descripcion = forms.CharField(label='Descripción', max_length=60, required=False)
    
    class Meta:
        model = AduanaSeccion
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        cve_aduana = cleaned_data.get('cve_aduana')
        cve_seccion = cleaned_data.get('cve_seccion')
        
        if cve_aduana and len(cve_aduana) != 2:
            raise ValidationError({
                'cve_aduana': 'La clave de aduana debe contener exactamente 2 caracteres.'
            })
        if cve_seccion and len(cve_seccion) != 1:
            raise ValidationError({
                'cve_seccion': 'La clave de sección debe contener exactamente 1 caracter.'
            })
        
        return cleaned_data

class ClavePedimentoForm(forms.ModelForm):
    cve_pedimento = forms.CharField(label='Clave de Pedimento')
    descripcion = forms.CharField(label='Descripción', max_length=120, required=False)
    importacion = forms.BooleanField(label='Importación', required=False)
    exportacion = forms.BooleanField(label='Exportación', required=False)
    
    class Meta:
        model = ClavePedimento
        fields = '__all__'

    def clean_cve_pedimento(self):
        cve = self.cleaned_data.get('cve_pedimento')
        if len(cve) < 2:
            raise ValidationError('La clave de pedimento debe contener al menos 2 caracteres. Por favor, verifique la información.')
        return cve

class PedimentoForm(forms.ModelForm):
    num_pedimento = forms.CharField(label='Número de Pedimento')
    tipo_operacion = forms.ChoiceField(label='Tipo de Operación', choices=Pedimento.TIPO_OPERACION_CHOICES)
    aduana_seccion = forms.ModelChoiceField(label='Aduana y Sección', queryset=AduanaSeccion.objects.all())
    patente = forms.ModelChoiceField(label='Patente', queryset=AgenteAduanal.objects.all())
    clave_pedimento = forms.ModelChoiceField(label='Clave de Pedimento', queryset=ClavePedimento.objects.all())
    fecha_entrada = forms.DateField(label='Fecha de Entrada', widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_pago = forms.DateField(label='Fecha de Pago', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Pedimento
        fields = '__all__'

    def clean_num_pedimento(self):
        num = self.cleaned_data.get('num_pedimento')
        if len(num) != 15:
            raise ValidationError('El número de pedimento debe contener exactamente 15 caracteres.')
        return num

    def clean(self):
        cleaned_data = super().clean()
        tipo_operacion = cleaned_data.get('tipo_operacion')
        clave_pedimento = cleaned_data.get('clave_pedimento')
        
        if clave_pedimento:
            if tipo_operacion == 1 and not clave_pedimento.importacion:
                raise ValidationError({
                    'clave_pedimento': 'La clave de pedimento seleccionada no es válida para operaciones de importación.'
                })
            elif tipo_operacion == 2 and not clave_pedimento.exportacion:
                raise ValidationError({
                    'clave_pedimento': 'La clave de pedimento seleccionada no es válida para operaciones de exportación.'
                })

        return cleaned_data