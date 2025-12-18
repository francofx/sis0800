from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Consulta


class ConsultaForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha"
    )
    
    class Meta:
        model = Consulta
        exclude = ['marca_temporal', 'creado_por', 'fecha_creacion', 'fecha_modificacion']
        widgets = {
            'zona': forms.Select(attrs={'class': 'form-select'}),
            'operador': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_nombre_interlocutor': forms.TextInput(attrs={'class': 'form-control'}),
            'consulta': forms.Select(attrs={'class': 'form-select'}),
            'telefono_interlocutor': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_vinculo': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'apellido_nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'barrio': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'escolarizado': forms.Select(attrs={'class': 'form-select'}),
            'etapa_escolar': forms.Select(attrs={'class': 'form-select'}),
            'obra_social': forms.Select(attrs={'class': 'form-select'}),
            'nombre_obra_social': forms.TextInput(attrs={'class': 'form-control'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_nombre_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'dni_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'tiempo_consumo': forms.Select(attrs={'class': 'form-select'}),
            'tipo_sustancia': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tratamiento_anterior': forms.Select(attrs={'class': 'form-select'}),
            'tipo_tratamiento_anterior': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'efector_salud_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'riesgo_inminente': forms.Select(attrs={'class': 'form-select'}),
            'institucion_derivado': forms.TextInput(attrs={'class': 'form-control'}),
            'seguimiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'situacion_social': forms.Select(attrs={'class': 'form-select'}),
            'caracteristica_judicial': forms.Select(attrs={'class': 'form-select'}),
            'intervencion_propuesta': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
