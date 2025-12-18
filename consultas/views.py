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
        form = ConsultaForm(request.POST, user=request.user)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.creado_por = request.user
            consulta.save()
            messages.success(request, '¡Consulta cargada exitosamente!')
            return redirect('cargar_consulta')
    else:
        form = ConsultaForm(user=request.user)
    return render(request, 'consultas/cargar_consulta.html', {'form': form})


@login_required
def mis_consultas(request):
    """Listado de consultas cargadas por el operador actual"""
    # Obtener nombre del operador actual
    nombre_operador = f"{request.user.last_name} {request.user.first_name}".strip()
    
    # Filtrar consultas por el operador actual (por nombre o por creado_por)
    consultas = Consulta.objects.filter(
        Q(operador=nombre_operador) | Q(creado_por=request.user)
    ).distinct()
    
    # Búsqueda general
    busqueda = request.GET.get('q', '').strip()
    if busqueda:
        consultas = consultas.filter(
            Q(apellido_nombre_usuario__icontains=busqueda) |
            Q(apellido_nombre_interlocutor__icontains=busqueda) |
            Q(dni__icontains=busqueda) |
            Q(ciudad__icontains=busqueda) |
            Q(barrio__icontains=busqueda) |
            Q(telefono__icontains=busqueda) |
            Q(telefono_interlocutor__icontains=busqueda) |
            Q(motivo_consulta__icontains=busqueda) |
            Q(tipo_sustancia__icontains=busqueda) |
            Q(intervencion_propuesta__icontains=busqueda) |
            Q(zona__icontains=busqueda) |
            Q(consulta__icontains=busqueda)
        )
    
    consultas = consultas.order_by('-fecha', '-marca_temporal')
    
    # Paginación
    paginator = Paginator(consultas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'consultas/mis_consultas.html', {
        'page_obj': page_obj,
        'total_consultas': consultas.count(),
        'nombre_operador': nombre_operador,
        'busqueda': busqueda,
    })


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
        zona_data = list(consultas.values('zona').annotate(count=Count('id')).order_by('-count'))
        if zona_data:
            labels = [d['zona'] or 'Sin zona' for d in zona_data]
            values = [d['count'] for d in zona_data]
            fig_zona = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
            fig_zona.update_layout(title='Consultas por Zona', margin=dict(l=20, r=20, t=40, b=20))
            graficos['zona'] = json.dumps(fig_zona, cls=PlotlyJSONEncoder)
        
        # Gráfico de consultas por sexo
        sexo_data = list(consultas.exclude(sexo__isnull=True).exclude(sexo='').values('sexo').annotate(count=Count('id')).order_by('-count'))
        if sexo_data:
            x_vals = [d['sexo'] for d in sexo_data]
            y_vals = [d['count'] for d in sexo_data]
            fig_sexo = go.Figure(data=[go.Bar(x=x_vals, y=y_vals, marker_color='#4e73df')])
            fig_sexo.update_layout(title='Consultas por Sexo', xaxis_title='Sexo', yaxis_title='Cantidad', margin=dict(l=20, r=20, t=40, b=20))
            graficos['sexo'] = json.dumps(fig_sexo, cls=PlotlyJSONEncoder)
        
        # Gráfico de tiempo de consumo
        tiempo_data = list(consultas.exclude(tiempo_consumo__isnull=True).exclude(tiempo_consumo='').values('tiempo_consumo').annotate(count=Count('id')).order_by('-count'))
        if tiempo_data:
            x_vals = [d['tiempo_consumo'] for d in tiempo_data]
            y_vals = [d['count'] for d in tiempo_data]
            fig_tiempo = go.Figure(data=[go.Bar(x=x_vals, y=y_vals, marker_color='#36b9cc')])
            fig_tiempo.update_layout(title='Tiempo de Consumo', xaxis_title='Tiempo', yaxis_title='Cantidad', margin=dict(l=20, r=20, t=40, b=20))
            graficos['tiempo_consumo'] = json.dumps(fig_tiempo, cls=PlotlyJSONEncoder)
        
        # Gráfico de tipo de consulta
        consulta_data = list(consultas.values('consulta').annotate(count=Count('id')).order_by('-count'))
        if consulta_data:
            labels = [d['consulta'] or 'Sin especificar' for d in consulta_data]
            values = [d['count'] for d in consulta_data]
            fig_consulta = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig_consulta.update_layout(title='Tipo de Consulta (Directa/Indirecta)', margin=dict(l=20, r=20, t=40, b=20))
            graficos['consulta'] = json.dumps(fig_consulta, cls=PlotlyJSONEncoder)
        
        # Gráfico de tratamiento anterior
        trat_data = list(consultas.exclude(tratamiento_anterior__isnull=True).exclude(tratamiento_anterior='').values('tratamiento_anterior').annotate(count=Count('id')).order_by('-count'))
        if trat_data:
            labels = ['Sí' if d['tratamiento_anterior'] == 'SI' else 'No' for d in trat_data]
            values = [d['count'] for d in trat_data]
            fig_trat = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig_trat.update_layout(title='¿Tuvo Tratamiento Anterior?', margin=dict(l=20, r=20, t=40, b=20))
            graficos['tratamiento'] = json.dumps(fig_trat, cls=PlotlyJSONEncoder)
        
        # Gráfico de consultas por ciudad (top 10)
        ciudad_data = list(consultas.exclude(ciudad__isnull=True).exclude(ciudad='').values('ciudad').annotate(count=Count('id')).order_by('-count')[:10])
        if ciudad_data:
            x_vals = [d['ciudad'] for d in ciudad_data]
            y_vals = [d['count'] for d in ciudad_data]
            fig_ciudad = go.Figure(data=[go.Bar(x=x_vals, y=y_vals, marker_color='#4e73df')])
            fig_ciudad.update_layout(title='Top 10 Ciudades con más Consultas', xaxis_title='Ciudad', yaxis_title='Cantidad', margin=dict(l=20, r=20, t=40, b=20), xaxis_tickangle=-45)
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
            x_vals = [s[0] for s in sorted_sustancias]
            y_vals = [s[1] for s in sorted_sustancias]
            fig_sustancias = go.Figure(data=[go.Bar(x=x_vals, y=y_vals, marker_color='#f6c23e')])
            fig_sustancias.update_layout(title='Sustancias más Reportadas', xaxis_title='Sustancia', yaxis_title='Menciones', margin=dict(l=20, r=20, t=40, b=20), xaxis_tickangle=-45)
            graficos['sustancias'] = json.dumps(fig_sustancias, cls=PlotlyJSONEncoder)
        
        # Gráfico de situación social
        sit_social_data = list(consultas.exclude(situacion_social__isnull=True).exclude(situacion_social='').values('situacion_social').annotate(count=Count('id')).order_by('-count'))
        if sit_social_data:
            labels = [d['situacion_social'] for d in sit_social_data]
            values = [d['count'] for d in sit_social_data]
            fig_social = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig_social.update_layout(title='Situación Social', margin=dict(l=20, r=20, t=40, b=20))
            graficos['situacion_social'] = json.dumps(fig_social, cls=PlotlyJSONEncoder)
        
        # Gráfico de consultas por operador
        operador_data = list(consultas.exclude(operador__isnull=True).exclude(operador='').values('operador').annotate(count=Count('id')).order_by('-count'))
        if operador_data:
            x_vals = [d['operador'] for d in operador_data]
            y_vals = [d['count'] for d in operador_data]
            fig_operador = go.Figure(data=[go.Bar(x=x_vals, y=y_vals, marker_color='#6f42c1')])
            fig_operador.update_layout(title='Consultas por Operador', xaxis_title='Operador', yaxis_title='Cantidad', margin=dict(l=20, r=20, t=40, b=20), xaxis_tickangle=-45)
            graficos['operador'] = json.dumps(fig_operador, cls=PlotlyJSONEncoder)
    
    # Obtener lista de operadores únicos para el filtro
    operadores = Consulta.objects.exclude(
        operador__isnull=True
    ).exclude(
        operador=''
    ).values_list('operador', flat=True).distinct().order_by('operador')
    
    context = {
        'filterset': filterset,
        'page_obj': page_obj,
        'total_consultas': total_consultas,
        'graficos': graficos,
        'operadores': operadores,
    }
    return render(request, 'consultas/informes.html', context)


@login_required
def detalle_consulta(request, pk):
    """Ver detalle de una consulta"""
    consulta = get_object_or_404(Consulta, pk=pk)
    
    # Si no es admin, solo puede ver sus propias consultas
    if not is_admin(request.user):
        nombre_operador = f"{request.user.last_name} {request.user.first_name}".strip()
        if consulta.operador != nombre_operador and consulta.creado_por != request.user:
            messages.error(request, 'No tienes permiso para ver esta consulta.')
            return redirect('mis_consultas')
    
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
