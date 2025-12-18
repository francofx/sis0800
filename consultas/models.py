from django.db import models
from django.contrib.auth.models import User


class Consulta(models.Model):
    ZONA_CHOICES = [
        ('Sur', 'Sur'),
        ('Centro - Norte', 'Centro - Norte'),
        ('Norte', 'Norte'),
        ('Oeste', 'Oeste'),
    ]
    
    CONSULTA_CHOICES = [
        ('Directa', 'Directa'),
        ('Indirecta', 'Indirecta'),
    ]
    
    SEXO_CHOICES = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('Otro', 'Otro'),
    ]
    
    ESCOLARIZADO_CHOICES = [
        ('SI', 'Sí'),
        ('No', 'No'),
    ]
    
    ETAPA_ESCOLAR_CHOICES = [
        ('Primaria Incompleta', 'Primaria Incompleta'),
        ('Primaria Completa', 'Primaria Completa'),
        ('Secundaria Incompleta', 'Secundaria Incompleta'),
        ('Secundaria Completa', 'Secundaria Completa'),
        ('Terciario/Universitario Incompleto', 'Terciario/Universitario Incompleto'),
        ('Terciario/Universitario Completo', 'Terciario/Universitario Completo'),
    ]
    
    OBRA_SOCIAL_CHOICES = [
        ('SI', 'Sí'),
        ('No', 'No'),
    ]
    
    TRATAMIENTO_ANTERIOR_CHOICES = [
        ('SI', 'Sí'),
        ('No', 'No'),
    ]
    
    TIEMPO_CONSUMO_CHOICES = [
        ('Menos de 1 año', 'Menos de 1 año'),
        ('De 1 años a 5', 'De 1 años a 5'),
        ('de 5 años a 10', 'De 5 años a 10'),
        ('Más de 10 años', 'Más de 10 años'),
    ]
    
    RIESGO_CHOICES = [
        ('SI', 'Sí'),
        ('No', 'No'),
    ]
    
    SITUACION_SOCIAL_CHOICES = [
        ('Situación de Calle', 'Situación de Calle'),
        ('Infancia', 'Infancia'),
        ('Violencia', 'Violencia'),
        ('', 'Sin especificar'),
    ]
    
    CARACTERISTICA_JUDICIAL_CHOICES = [
        ('Judicializado', 'Judicializado'),
        ('', 'Sin especificar'),
    ]
    
    # Campos del formulario
    marca_temporal = models.DateTimeField(auto_now_add=True, verbose_name="Marca temporal")
    fecha = models.DateField(verbose_name="Fecha")
    zona = models.CharField(max_length=50, choices=ZONA_CHOICES, verbose_name="Zona")
    operador = models.CharField(max_length=100, verbose_name="Operador")
    
    # Datos del interlocutor
    apellido_nombre_interlocutor = models.CharField(max_length=200, verbose_name="Apellido y Nombre Interlocutor")
    consulta = models.CharField(max_length=20, choices=CONSULTA_CHOICES, verbose_name="Consulta")
    telefono_interlocutor = models.CharField(max_length=50, blank=True, null=True, verbose_name="Teléfono Interlocutor")
    tipo_vinculo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tipo de Vínculo (Consulta Indirecta)")
    motivo_consulta = models.TextField(verbose_name="Motivo de la Consulta")
    
    # Datos del usuario
    apellido_nombre_usuario = models.CharField(max_length=200, verbose_name="Apellido y Nombre Usuario")
    dni = models.CharField(max_length=20, blank=True, null=True, verbose_name="DNI")
    fecha_nacimiento = models.CharField(max_length=50, blank=True, null=True, verbose_name="Fecha de Nacimiento")
    edad = models.CharField(max_length=20, blank=True, null=True, verbose_name="Edad")
    sexo = models.CharField(max_length=20, choices=SEXO_CHOICES, verbose_name="Sexo")
    nacionalidad = models.CharField(max_length=50, default="Argentina", verbose_name="Nacionalidad")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    barrio = models.CharField(max_length=100, blank=True, null=True, verbose_name="Barrio")
    direccion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Dirección")
    telefono = models.CharField(max_length=50, blank=True, null=True, verbose_name="Teléfono")
    
    # Datos educativos
    escolarizado = models.CharField(max_length=5, choices=ESCOLARIZADO_CHOICES, blank=True, null=True, verbose_name="Escolarizado")
    etapa_escolar = models.CharField(max_length=100, choices=ETAPA_ESCOLAR_CHOICES, blank=True, null=True, verbose_name="Etapa Escolar")
    
    # Datos de obra social
    obra_social = models.CharField(max_length=5, choices=OBRA_SOCIAL_CHOICES, blank=True, null=True, verbose_name="Obra Social")
    nombre_obra_social = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre Obra Social")
    
    # Datos laborales
    ocupacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ocupación")
    
    # Datos de referencia afectiva
    apellido_nombre_referencia = models.CharField(max_length=200, blank=True, null=True, verbose_name="Apellido y Nombre Referencia Afectiva")
    dni_referencia = models.CharField(max_length=20, blank=True, null=True, verbose_name="DNI Referencia Afectiva")
    telefono_referencia = models.CharField(max_length=50, blank=True, null=True, verbose_name="Teléfono Referencia Afectiva")
    
    # Datos de consumo
    tiempo_consumo = models.CharField(max_length=50, choices=TIEMPO_CONSUMO_CHOICES, blank=True, null=True, verbose_name="Tiempo de Consumo")
    tipo_sustancia = models.TextField(blank=True, null=True, verbose_name="Tipo de Sustancia que Consume")
    tratamiento_anterior = models.CharField(max_length=5, choices=TRATAMIENTO_ANTERIOR_CHOICES, blank=True, null=True, verbose_name="Tratamiento Anterior")
    tipo_tratamiento_anterior = models.TextField(blank=True, null=True, verbose_name="Tipo de Tratamiento Anterior")
    
    # Datos de salud
    efector_salud_referencia = models.CharField(max_length=200, blank=True, null=True, verbose_name="Efector de Salud de Referencia")
    riesgo_inminente = models.CharField(max_length=5, choices=RIESGO_CHOICES, blank=True, null=True, verbose_name="Riesgo Inminente")
    institucion_derivado = models.CharField(max_length=200, blank=True, null=True, verbose_name="Institución/Efector Derivado")
    seguimiento = models.TextField(blank=True, null=True, verbose_name="Seguimiento")
    
    # Datos sociales
    situacion_social = models.CharField(max_length=50, choices=SITUACION_SOCIAL_CHOICES, blank=True, null=True, verbose_name="Situación Social")
    caracteristica_judicial = models.CharField(max_length=50, choices=CARACTERISTICA_JUDICIAL_CHOICES, blank=True, null=True, verbose_name="Característica Judicial")
    intervencion_propuesta = models.TextField(blank=True, null=True, verbose_name="Intervención Propuesta")
    
    # Auditoría
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='consultas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ['-fecha', '-marca_temporal']

    def __str__(self):
        return f"{self.fecha} - {self.apellido_nombre_usuario} - {self.zona}"
