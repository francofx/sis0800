from django.contrib import admin
from .models import Consulta


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'zona', 'operador', 'apellido_nombre_usuario', 'consulta', 'ciudad']
    list_filter = ['zona', 'consulta', 'sexo', 'tiempo_consumo', 'tratamiento_anterior', 'fecha']
    search_fields = ['apellido_nombre_usuario', 'apellido_nombre_interlocutor', 'ciudad', 'operador']
    date_hierarchy = 'fecha'
    ordering = ['-fecha']
