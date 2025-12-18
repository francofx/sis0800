from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cargar/', views.cargar_consulta, name='cargar_consulta'),
    path('mis-consultas/', views.mis_consultas, name='mis_consultas'),
    path('informes/', views.informes, name='informes'),
    path('consulta/<int:pk>/', views.detalle_consulta, name='detalle_consulta'),
    path('exportar/', views.exportar_datos, name='exportar_datos'),
]
