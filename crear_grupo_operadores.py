"""
Script para crear grupo Operadores y asignar usuarios.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema0800.settings')
django.setup()

from django.contrib.auth.models import Group, User

# Crear grupo Operadores
grupo, created = Group.objects.get_or_create(name='Operadores')
print(f"Grupo 'Operadores': {'creado' if created else 'ya existía'}")

# Obtener usuarios operadores (excluir admin y superusuarios)
operadores = User.objects.exclude(is_superuser=True).exclude(username='admin')

# Agregar usuarios al grupo
for user in operadores:
    grupo.user_set.add(user)
    print(f"  Agregado al grupo: {user.username}")

print(f"\nTotal usuarios en grupo Operadores: {grupo.user_set.count()}")
