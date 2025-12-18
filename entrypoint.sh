#!/bin/bash

# Aplicar migraciones
python manage.py migrate --noinput

# Iniciar Gunicorn
exec gunicorn --bind 0.0.0.0:8000 --workers 3 sistema0800.wsgi:application
