# Sistema 0800 - Gestión de Consultas

Sistema web desarrollado en Django para la carga y análisis de consultas telefónicas del servicio 0800.

## Características

- **Carga de Consultas**: Formulario completo para registrar consultas telefónicas
- **Panel de Informes**: Gráficos interactivos y filtros avanzados (solo administradores)
- **Control de Usuarios**: Roles diferenciados (usuarios normales y administradores)
- **Exportación de Datos**: Descarga de datos filtrados en formato CSV

## Tecnologías

- Python 3.11+
- Django 5.2
- Bootstrap 5
- Plotly (gráficos interactivos)
- SQLite (base de datos)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repo>
cd 0800
```

2. Crear entorno virtual:
```bash
python -m venv venv
```

3. Activar entorno virtual:
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install django pandas plotly django-filter
```

5. Aplicar migraciones:
```bash
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

7. (Opcional) Importar datos desde CSV:
```bash
python import_csv.py ruta/al/archivo.csv
```

8. Ejecutar servidor:
```bash
python manage.py runserver
```

9. Acceder a http://127.0.0.1:8000

## Usuarios

- **Usuarios normales**: Pueden cargar consultas
- **Administradores (staff)**: Pueden ver informes y exportar datos

## Estructura del Proyecto

```
├── consultas/          # App principal
│   ├── models.py       # Modelo Consulta
│   ├── views.py        # Vistas
│   ├── forms.py        # Formularios
│   ├── filters.py      # Filtros para informes
│   └── urls.py         # URLs
├── templates/          # Templates HTML
├── sistema0800/        # Configuración Django
├── import_csv.py       # Script de importación
└── manage.py
```

## Licencia

MIT
