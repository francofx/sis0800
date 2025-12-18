from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder

from .models import Consulta
from .forms import ConsultaForm, CustomUserCreationForm
from .filters import ConsultaFilter


def is_admin(user):
    """Verifica si el usuario es administrador (staff o superuser)"""
    return user.is_staff or user.is_superuser


def home(request):
    """Página de inicio"""
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('informes')
        return redirect('cargar_consulta')
    return render(request, 'consultas/home.html')


def registro(request):
    """Registro de nuevos usuarios"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido al sistema.')
            return redirect('cargar_consulta')
    else:
        form = CustomUserCreationForm()
    return render(request, 'consultas/registro.html', {'form': form})


def login_view(request):
    """Vista de login personalizada"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.first_name or user.username}!')
            if is_admin(user):
                return redirect('informes')
            return redirect('cargar_consulta')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'consultas/login.html')


def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('home')


@login_required
def cargar_consulta(request):
    """Formulario para cargar una nueva consulta"""
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.creado_por = request.user
            consulta.save()
            messages.success(request, '¡Consulta cargada exitosamente!')
            return redirect('cargar_consulta')
    else:
        form = ConsultaForm()
    return render(request, 'consultas/cargar_consulta.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def informes(request):
    """Panel de informes para administradores"""
    filterset = ConsultaFilter(request.GET, queryset=Consulta.objects.all())
    consultas = filterset.qs
    
    # Paginación
    paginator = Paginator(consultas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estadísticas generales
    total_consultas = consultas.count()
    
    # Datos para gráficos
    graficos = {}
    
    if total_consultas > 0:
        # Gráfico de consultas por zona
        zona_data = consultas.values('zona').annotate(count=Count('id')).order_by('-count')
        if zona_data:
            fig_zona = px.pie(
                values=[d['count'] for d in zona_data],
                names=[d['zona'] or 'Sin zona' for d in zona_data],
                title='Consultas por Zona',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_zona.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            graficos['zona'] = json.dumps(fig_zona, cls=PlotlyJSONEncoder)
        
        # Gráfico de consultas por sexo
        sexo_data = consultas.values('sexo').annotate(count=Count('id')).order_by('-count')
        if sexo_data:
            fig_sexo = px.bar(
                x=[d['sexo'] or 'Sin especificar' for d in sexo_data],
                y=[d['count'] for d in sexo_data],
                title='Consultas por Sexo',
                labels={'x': 'Sexo', 'y': 'Cantidad'},
                color=[d['sexo'] or 'Sin especificar' for d in sexo_data],
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_sexo.update_layout(margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
            graficos['sexo'] = json.dumps(fig_sexo, cls=PlotlyJSONEncoder)
        
        # Gráfico de tiempo de consumo
        tiempo_data = consultas.exclude(tiempo_consumo__isnull=True).exclude(tiempo_consumo='').values('tiempo_consumo').annotate(count=Count('id')).order_by('-count')
        if tiempo_data:
            fig_tiempo = px.bar(
                x=[d['tiempo_consumo'] for d in tiempo_data],
                y=[d['count'] for d in tiempo_data],
                title='Tiempo de Consumo',
                labels={'x': 'Tiempo', 'y': 'Cantidad'},
                color_discrete_sequence=['#36b9cc']
            )
            fig_tiempo.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            graficos['tiempo_consumo'] = json.dumps(fig_tiempo, cls=PlotlyJSONEncoder)
        
        # Gráfico de tipo de consulta
        consulta_data = consultas.values('consulta').annotate(count=Count('id')).order_by('-count')
        if consulta_data:
            fig_consulta = px.pie(
                values=[d['count'] for d in consulta_data],
                names=[d['consulta'] or 'Sin especificar' for d in consulta_data],
                title='Tipo de Consulta (Directa/Indirecta)',
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_consulta.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            graficos['consulta'] = json.dumps(fig_consulta, cls=PlotlyJSONEncoder)
        
        # Gráfico de tratamiento anterior
        trat_data = consultas.exclude(tratamiento_anterior__isnull=True).exclude(tratamiento_anterior='').values('tratamiento_anterior').annotate(count=Count('id')).order_by('-count')
        if trat_data:
            fig_trat = px.pie(
                values=[d['count'] for d in trat_data],
                names=['Sí' if d['tratamiento_anterior'] == 'SI' else 'No' for d in trat_data],
                title='¿Tuvo Tratamiento Anterior?',
                color_discrete_sequence=['#1cc88a', '#e74a3b']
            )
            fig_trat.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            graficos['tratamiento'] = json.dumps(fig_trat, cls=PlotlyJSONEncoder)
        
        # Gráfico de consultas por ciudad (top 10)
        ciudad_data = consultas.exclude(ciudad__isnull=True).exclude(ciudad='').values('ciudad').annotate(count=Count('id')).order_by('-count')[:10]
        if ciudad_data:
            fig_ciudad = px.bar(
                x=[d['ciudad'] for d in ciudad_data],
                y=[d['count'] for d in ciudad_data],
                title='Top 10 Ciudades con más Consultas',
                labels={'x': 'Ciudad', 'y': 'Cantidad'},
                color_discrete_sequence=['#4e73df']
            )
            fig_ciudad.update_layout(margin=dict(l=20, r=20, t=40, b=20), xaxis_tickangle=-45)
            graficos['ciudad'] = json.dumps(fig_ciudad, cls=PlotlyJSONEncoder)
        
        # Análisis de sustancias
        sustancias_count = {}
        for consulta_obj in consultas.exclude(tipo_sustancia__isnull=True).exclude(tipo_sustancia=''):
            if consulta_obj.tipo_sustancia:
                for sustancia in consulta_obj.tipo_sustancia.replace(', ', ',').split(','):
                    sustancia = sustancia.strip()
                    if sustancia:
                        sustancias_count[sustancia] = sustancias_count.get(sustancia, 0) + 1
        
        if sustancias_count:
            sorted_sustancias = sorted(sustancias_count.items(), key=lambda x: x[1], reverse=True)[:10]
            fig_sustancias = px.bar(
                x=[s[0] for s in sorted_sustancias],
                y=[s[1] for s in sorted_sustancias],
                title='Sustancias más Reportadas',
                labels={'x': 'Sustancia', 'y': 'Menciones'},
                color_discrete_sequence=['#f6c23e']
            )
            fig_sustancias.update_layout(margin=dict(l=20, r=20, t=40, b=20), xaxis_tickangle=-45)
            graficos['sustancias'] = json.dumps(fig_sustancias, cls=PlotlyJSONEncoder)
        
        # Gráfico de situación social
        sit_social_data = consultas.exclude(situacion_social__isnull=True).exclude(situacion_social='').values('situacion_social').annotate(count=Count('id')).order_by('-count')
        if sit_social_data:
            fig_social = px.pie(
                values=[d['count'] for d in sit_social_data],
                names=[d['situacion_social'] for d in sit_social_data],
                title='Situación Social',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_social.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            graficos['situacion_social'] = json.dumps(fig_social, cls=PlotlyJSONEncoder)
    
    context = {
        'filterset': filterset,
        'page_obj': page_obj,
        'total_consultas': total_consultas,
        'graficos': graficos,
    }
    return render(request, 'consultas/informes.html', context)


@login_required
@user_passes_test(is_admin)
def detalle_consulta(request, pk):
    """Ver detalle de una consulta"""
    consulta = get_object_or_404(Consulta, pk=pk)
    return render(request, 'consultas/detalle_consulta.html', {'consulta': consulta})


@login_required
@user_passes_test(is_admin)
def exportar_datos(request):
    """Exportar datos filtrados a CSV"""
    import csv
    from django.http import HttpResponse
    
    filterset = ConsultaFilter(request.GET, queryset=Consulta.objects.all())
    consultas = filterset.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="consultas_0800.csv"'
    response.write('\ufeff')  # BOM para UTF-8
    
    writer = csv.writer(response)
    
    # Encabezados
    headers = [
        'ID', 'Fecha', 'Zona', 'Operador', 'Interlocutor', 'Consulta', 'Tel. Interlocutor',
        'Tipo Vínculo', 'Motivo', 'Usuario', 'DNI', 'Fecha Nac.', 'Edad', 'Sexo',
        'Nacionalidad', 'Ciudad', 'Barrio', 'Dirección', 'Teléfono', 'Escolarizado',
        'Etapa Escolar', 'Obra Social', 'Nombre OS', 'Ocupación', 'Ref. Afectiva',
        'DNI Ref.', 'Tel. Ref.', 'Tiempo Consumo', 'Sustancia', 'Trat. Anterior',
        'Tipo Trat. Anterior', 'Efector Salud', 'Riesgo', 'Institución Derivado',
        'Seguimiento', 'Sit. Social', 'Car. Judicial', 'Intervención'
    ]
    writer.writerow(headers)
    
    for c in consultas:
        writer.writerow([
            c.id, c.fecha, c.zona, c.operador, c.apellido_nombre_interlocutor,
            c.consulta, c.telefono_interlocutor, c.tipo_vinculo, c.motivo_consulta,
            c.apellido_nombre_usuario, c.dni, c.fecha_nacimiento, c.edad, c.sexo,
            c.nacionalidad, c.ciudad, c.barrio, c.direccion, c.telefono,
            c.escolarizado, c.etapa_escolar, c.obra_social, c.nombre_obra_social,
            c.ocupacion, c.apellido_nombre_referencia, c.dni_referencia,
            c.telefono_referencia, c.tiempo_consumo, c.tipo_sustancia,
            c.tratamiento_anterior, c.tipo_tratamiento_anterior,
            c.efector_salud_referencia, c.riesgo_inminente, c.institucion_derivado,
            c.seguimiento, c.situacion_social, c.caracteristica_judicial,
            c.intervencion_propuesta
        ])
    
    return response
