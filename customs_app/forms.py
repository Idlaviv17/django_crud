from django import forms
from django.core.exceptions import ValidationError
from .models import AgenteAduanal, Pedimento, AduanaSeccion, ClavePedimento

class AgenteAduanalForm(forms.ModelForm):
    nombre = forms.CharField(max_length=80, required=False)
    razon_social = forms.CharField(max_length=80, required=False)
    rfc = forms.CharField(max_length=20, required=False)
    curp = forms.CharField(max_length=18, required=False)
    direccion1 = forms.CharField(max_length=60, required=False)
    direccion2 = forms.CharField(max_length=60, required=False)
    direccion3 = forms.CharField(max_length=60, required=False)
    serie = forms.CharField(max_length=30, required=False)

    class Meta:
        model = AgenteAduanal
        fields = '__all__'

    def clean_patente(self):
        patente = self.cleaned_data.get('patente')
        if len(patente) != 4:
            raise ValidationError('El número de patente debe tener 4 caracteres.')
        return patente

class AduanaSeccionForm(forms.ModelForm):
    descripcion = forms.CharField(max_length=60, required=False)
    
    class Meta:
        model = AduanaSeccion
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        cve_aduana = cleaned_data.get('cve_aduana')
        cve_seccion = cleaned_data.get('cve_seccion')
        
        if cve_aduana and len(cve_aduana) != 2:
            raise ValidationError('La clave de aduana debe tener 2 caracteres.')
        if cve_seccion and len(cve_seccion) != 1:
            raise ValidationError('La clave de sección debe tener 1 caracter.')
        
        return cleaned_data

class ClavePedimentoForm(forms.ModelForm):
    descripcion = forms.CharField(max_length=120, required=False)
    
    class Meta:
        model = ClavePedimento
        fields = '__all__'

    def clean_cve_pedimento(self):
        cve = self.cleaned_data.get('cve_pedimento')
        if len(cve) < 2:
            raise ValidationError('La clave de pedimento debe tener al menos 2 caracteres.')
        return cve

class PedimentoForm(forms.ModelForm):
    fecha_pago = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Pedimento
        fields = '__all__'
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_num_pedimento(self):
        num = self.cleaned_data.get('num_pedimento')
        if len(num) != 15:
            raise ValidationError('El número de pedimento debe tener 15 caracteres.')
        return num