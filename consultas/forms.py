from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Consulta


def get_tipo_vinculo_choices():
    """Obtiene los tipos de vínculo únicos de la base de datos"""
    vinculos = Consulta.objects.exclude(
        tipo_vinculo__isnull=True
    ).exclude(
        tipo_vinculo=''
    ).values_list('tipo_vinculo', flat=True).distinct()
    
    choices = [('', '---------')]
    for vinculo in sorted(set(vinculos)):
        choices.append((vinculo, vinculo))
    return choices


def get_tipo_sustancia_choices():
    """Obtiene los tipos de sustancia únicos de la base de datos"""
    sustancias_raw = Consulta.objects.exclude(
        tipo_sustancia__isnull=True
    ).exclude(
        tipo_sustancia=''
    ).values_list('tipo_sustancia', flat=True)
    
    # Extraer sustancias individuales (pueden estar separadas por comas)
    todas = set()
    for registro in sustancias_raw:
        if registro:
            for s in str(registro).split(','):
                s = s.strip()
                if s:
                    todas.add(s)
    
    choices = []
    for sustancia in sorted(todas):
        choices.append((sustancia, sustancia))
    return choices


class ConsultaForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha"
    )
    
    operador = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        label="Operador"
    )
    
    tipo_vinculo = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        label="Tipo de Vínculo"
    )
    
    tipo_sustancia = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Tipo de Sustancia que Consume"
    )
    
    situacion_social = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Situación Social"
    )
    
    class Meta:
        model = Consulta
        exclude = ['marca_temporal', 'creado_por', 'fecha_creacion', 'fecha_modificacion']
        widgets = {
            'zona': forms.Select(attrs={'class': 'form-select'}),
            'apellido_nombre_interlocutor': forms.TextInput(attrs={'class': 'form-control'}),
            'consulta': forms.Select(attrs={'class': 'form-select'}),
            'telefono_interlocutor': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'apellido_nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_fecha_nacimiento'}),
            'edad': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_edad'}),
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
            'tratamiento_anterior': forms.Select(attrs={'class': 'form-select'}),
            'tipo_tratamiento_anterior': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'efector_salud_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'riesgo_inminente': forms.Select(attrs={'class': 'form-select'}),
            'institucion_derivado': forms.TextInput(attrs={'class': 'form-control'}),
            'seguimiento': forms.Select(attrs={'class': 'form-select'}),
            'caracteristica_judicial': forms.TextInput(attrs={'class': 'form-control'}),
            'intervencion_propuesta': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar opciones de tipo de vínculo desde la base de datos
        self.fields['tipo_vinculo'].choices = get_tipo_vinculo_choices()
        
        # Cargar opciones de tipo de sustancia desde la base de datos
        self.fields['tipo_sustancia'].choices = get_tipo_sustancia_choices()
        
        # Cargar opciones de situación social
        self.fields['situacion_social'].choices = Consulta.SITUACION_SOCIAL_CHOICES
        
        # Si estamos editando, cargar las sustancias seleccionadas
        if self.instance and self.instance.pk and self.instance.tipo_sustancia:
            sustancias_guardadas = [s.strip() for s in self.instance.tipo_sustancia.split(',') if s.strip()]
            self.initial['tipo_sustancia'] = sustancias_guardadas
        
        # Si estamos editando, cargar las situaciones sociales seleccionadas
        if self.instance and self.instance.pk and self.instance.situacion_social:
            situaciones_guardadas = [s.strip() for s in self.instance.situacion_social.split(',') if s.strip()]
            self.initial['situacion_social'] = situaciones_guardadas
        
        # Si hay usuario logueado, usar su nombre como operador
        if user and user.is_authenticated:
            nombre_operador = f"{user.last_name} {user.first_name}".strip()
            if not nombre_operador:
                nombre_operador = user.username
            self.fields['operador'].initial = nombre_operador
    
    def clean_tipo_sustancia(self):
        """Convierte la lista de sustancias seleccionadas a texto separado por comas"""
        sustancias = self.cleaned_data.get('tipo_sustancia', [])
        if sustancias:
            return ', '.join(sustancias)
        return ''
    
    def clean_situacion_social(self):
        """Convierte la lista de situaciones sociales seleccionadas a texto separado por comas"""
        situaciones = self.cleaned_data.get('situacion_social', [])
        if situaciones:
            return ', '.join(situaciones)
        return ''


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
