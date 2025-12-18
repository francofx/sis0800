import django_filters
from .models import Consulta


class ConsultaFilter(django_filters.FilterSet):
    fecha_desde = django_filters.DateFilter(field_name='fecha', lookup_expr='gte', label='Fecha desde')
    fecha_hasta = django_filters.DateFilter(field_name='fecha', lookup_expr='lte', label='Fecha hasta')
    apellido_nombre_usuario = django_filters.CharFilter(lookup_expr='icontains', label='Usuario (contiene)')
    apellido_nombre_interlocutor = django_filters.CharFilter(lookup_expr='icontains', label='Interlocutor (contiene)')
    ciudad = django_filters.CharFilter(lookup_expr='icontains', label='Ciudad (contiene)')
    tipo_sustancia = django_filters.CharFilter(lookup_expr='icontains', label='Sustancia (contiene)')
    operador = django_filters.CharFilter(lookup_expr='icontains', label='Operador (contiene)')
    
    class Meta:
        model = Consulta
        fields = {
            'zona': ['exact'],
            'consulta': ['exact'],
            'sexo': ['exact'],
            'tiempo_consumo': ['exact'],
            'tratamiento_anterior': ['exact'],
            'situacion_social': ['exact'],
            'caracteristica_judicial': ['exact'],
            'obra_social': ['exact'],
            'escolarizado': ['exact'],
            'riesgo_inminente': ['exact'],
        }
