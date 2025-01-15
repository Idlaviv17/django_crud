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
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-input'}),
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_patente(self):
        patente = self.cleaned_data.get('patente')
        if len(patente) != 4:
            raise ValidationError('El número de patente debe tener 4 caracteres.')
        return patente

    def clean_rfc(self):
        rfc = self.cleaned_data.get('rfc')
        if rfc and (len(rfc) != 12 and len(rfc) != 13):
            raise ValidationError('El RFC debe tener 12 o 13 caracteres.')
        return rfc

class PedimentoForm(forms.ModelForm):
    class Meta:
        model = Pedimento
        fields = '__all__'
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'type': 'date'}),
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
        }