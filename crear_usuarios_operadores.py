"""
Script para crear usuarios de operadores existentes.
Username: primera letra del nombre + apellido (ej: vgustavo para Vogel Gustavo)
Contraseña: Cambiar123
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema0800.settings')
django.setup()

from django.contrib.auth.models import User
from consultas.models import Consulta


def crear_usuarios_operadores():
    # Obtener operadores únicos
    operadores = Consulta.objects.exclude(
        operador__isnull=True
    ).exclude(
        operador=''
    ).values_list('operador', flat=True).distinct()
    
    operadores_unicos = set(operadores)
    print(f"Operadores únicos encontrados: {len(operadores_unicos)}")
    
    usuarios_creados = []
    usuarios_existentes = []
    
    for operador in sorted(operadores_unicos):
        # Parsear nombre: "Apellido Nombre" o "Nombre Apellido"
        partes = operador.strip().split()
        
        if len(partes) >= 2:
            # Asumimos formato "Apellido Nombre" basado en los datos
            # Ej: "Botta Georgina" -> gbotta
            apellido = partes[0].lower()
            nombre = partes[1].lower()
            username = nombre[0] + apellido  # primera letra nombre + apellido
        else:
            username = operador.lower().replace(' ', '')
        
        # Limpiar caracteres especiales
        username = username.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        username = username.replace('ñ', 'n')
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            usuarios_existentes.append((operador, username))
            print(f"  Ya existe: {username} ({operador})")
            continue
        
        # Crear usuario
        try:
            # Separar nombre y apellido para el modelo User
            if len(partes) >= 2:
                first_name = partes[1]  # Nombre
                last_name = partes[0]   # Apellido
            else:
                first_name = operador
                last_name = ''
            
            user = User.objects.create_user(
                username=username,
                password='Cambiar123',
                first_name=first_name,
                last_name=last_name,
                email=f'{username}@sistema0800.local'
            )
            usuarios_creados.append((operador, username))
            print(f"  Creado: {username} ({operador}) - {first_name} {last_name}")
            
        except Exception as e:
            print(f"  Error creando {username}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Usuarios creados: {len(usuarios_creados)}")
    print(f"Usuarios que ya existían: {len(usuarios_existentes)}")
    print(f"\nCredenciales: usuario / Cambiar123")
    print(f"\nUsuarios creados:")
    for operador, username in usuarios_creados:
        print(f"  {username:20} -> {operador}")


if __name__ == '__main__':
    crear_usuarios_operadores()
