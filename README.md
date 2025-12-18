# Sistema 0800-268-5640

Sistema de gestión de consultas telefónicas para la línea 0800-268-5640 de atención en adicciones.

## 📋 Descripción

Sistema web desarrollado en Django para la carga, gestión y análisis de consultas recibidas en la línea telefónica de atención. Permite a los operadores registrar las consultas y a los administradores visualizar informes estadísticos con gráficos interactivos.

## 🚀 Características

### Para Operadores
- ✅ Carga de consultas mediante formulario completo
- ✅ Vista "Mis Consultas" para ver solo registros propios
- ✅ Búsqueda y filtrado de consultas personales
- ✅ Edición de consultas cargadas

### Para Administradores
- ✅ Panel de informes con gráficos interactivos
- ✅ Filtros avanzados por múltiples criterios
- ✅ Exportación de datos
- ✅ Gestión de usuarios y permisos
- ✅ Acceso al panel de administración de Django

### Gráficos Disponibles
- 📊 Consultas por Zona (Centro-Norte / Sur)
- 📊 Consultas por Sexo
- 📊 Tipo de Consulta (Directa/Indirecta)
- 📊 Tiempo de Consumo
- 📊 Tratamiento Anterior
- 📊 Situación Social
- 📊 Top 10 Ciudades
- 📊 Sustancias más Reportadas
- 📊 Consultas por Operador

## 🛠️ Tecnologías

- **Backend:** Django 5.2.9
- **Frontend:** Bootstrap 5 (CDN)
- **Gráficos:** Plotly
- **Base de datos:** SQLite
- **Servidor WSGI:** Gunicorn
- **Archivos estáticos:** WhiteNoise
- **Contenedores:** Docker

## 📁 Estructura del Proyecto

```
sistema0800/
├── consultas/                 # Aplicación principal
│   ├── migrations/            # Migraciones de base de datos
│   ├── models.py              # Modelos de datos
│   ├── views.py               # Vistas y lógica
│   ├── forms.py               # Formularios
│   ├── filters.py             # Filtros para informes
│   ├── urls.py                # Rutas de la aplicación
│   └── admin.py               # Configuración del admin
├── sistema0800/               # Configuración del proyecto
│   ├── settings.py            # Configuración Django
│   ├── urls.py                # Rutas principales
│   └── wsgi.py                # Punto de entrada WSGI
├── templates/                 # Plantillas HTML
│   ├── base.html              # Plantilla base
│   └── consultas/             # Plantillas de la app
│       ├── home.html
│       ├── login.html
│       ├── cargar_consulta.html
│       ├── mis_consultas.html
│       ├── detalle_consulta.html
│       └── informes.html
├── static/                    # Archivos estáticos
├── Dockerfile                 # Imagen Docker
├── docker-compose.yml         # Orquestación Docker
├── entrypoint.sh              # Script de inicio
├── requirements.txt           # Dependencias Python
└── db.sqlite3                 # Base de datos
```

## ⚙️ Instalación

### Opción 1: Docker (Recomendado para Producción)

```bash
# Clonar repositorio
git clone https://github.com/francofx/sis0800.git
cd sis0800

# Construir y ejecutar
docker-compose up -d

# Ver logs
docker logs sistema0800
```

El sistema estará disponible en: http://localhost:8000

### Opción 2: Instalación Local (Desarrollo)

```bash
# Clonar repositorio
git clone https://github.com/francofx/sis0800.git
cd sis0800

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver 0.0.0.0:8000
```

## 👥 Usuarios del Sistema

### Administrador
| Campo | Valor |
|-------|-------|
| **Usuario** | admin |
| **Contraseña** | admin123 |
| **Permisos** | Acceso completo, informes, gestión de usuarios |

### Operadores
Los operadores solo pueden ver "Mis Consultas" y cargar nuevas consultas.

| Usuario | Nombre Completo | Contraseña |
|---------|-----------------|------------|
| gbotta | Botta Gabriela | Cambiar123 |
| froldan | Roldan Florencia | Cambiar123 |
| gvogel | Vogel Gonzalo | Cambiar123 |
| atonani | Tonani Alejandra | Cambiar123 |
| fmagnin | Magnin Fabricio | Cambiar123 |
| slucero | Lucero Sabrina | Cambiar123 |
| ygoumas | Goumas Yamila | Cambiar123 |
| perrante | Errante Patricia | Cambiar123 |
| abarchiesi | Barchiesi Alejandro | Cambiar123 |
| vrienzi | Rienzi Victoria | Cambiar123 |
| mbolger | Bolger Melisa | Cambiar123 |
| prosciani | Rosciani Pablo | Cambiar123 |
| ralvarez | Alvarez Romina | Cambiar123 |

---

## 📊 Modelo de Datos

### Campos del Formulario de Consulta

#### Datos de la Llamada
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `fecha` | Date | Fecha de la consulta |
| `zona` | Choice | Centro-Norte / Sur |
| `operador` | ForeignKey | Usuario operador |

#### Tipo de Consulta
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `consulta` | Choice | Directa / Indirecta |
| `tipo_vinculo` | String | Tipo de vínculo con la persona |

#### Datos del Interlocutor (quien llama)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `apellido_nombre_interlocutor` | String | Nombre completo |
| `telefono_interlocutor` | String | Teléfono de contacto |

#### Datos del Usuario (persona con consumo problemático)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `apellido_nombre_usuario` | String | Nombre completo |
| `fecha_nacimiento` | Date | Fecha de nacimiento |
| `edad` | Integer | Edad (calculada automáticamente) |
| `sexo` | Choice | Masculino / Femenino / Otro / No corresponde |
| `dni` | String | Documento de identidad |
| `telefono_usuario` | String | Teléfono |
| `provincia` | String | Provincia |
| `ciudad` | String | Ciudad |
| `barrio` | String | Barrio |

#### Datos de Consumo
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `tipo_sustancia` | String | Sustancias (múltiple selección) |
| `tiempo_consumo` | Choice | Menos de 1 año / 1-5 años / 5-10 años / Más de 10 años |
| `tratamiento_anterior` | Choice | SI / No |
| `tratamiento_descripcion` | Text | Descripción del tratamiento |

#### Datos de Salud y Derivación
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `obra_social` | Choice | SI / No |
| `obra_social_nombre` | String | Nombre de la obra social |
| `riesgo_inminente` | Choice | Emergencia / Urgencia / Ninguno |
| `seguimiento` | Choice | 24hs / 48hs |
| `demanda` | Text | Descripción de la demanda |
| `derivacion` | Text | Información de derivación |

#### Situación Social
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `situacion_social` | String | Situación de Calle / Infancia / Violencia / Pueblos Originarios / Judicializado |
| `caracteristica_judicial` | String | Descripción de situación judicial |

#### Observaciones
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `observaciones` | Text | Observaciones adicionales |

---

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `DEBUG` | Modo debug | `True` |
| `SECRET_KEY` | Clave secreta Django | (generada) |
| `ALLOWED_HOSTS` | Hosts permitidos | `*` |
| `CSRF_TRUSTED_ORIGINS` | Orígenes confiables CSRF | `localhost` |

### Configuración Docker

El archivo `docker-compose.yml` permite configurar:

```yaml
services:
  web:
    ports:
      - "8000:8000"  # Puerto de exposición
    environment:
      - DEBUG=False
      - SECRET_KEY=tu-clave-secreta-de-produccion
      - ALLOWED_HOSTS=tu-dominio.com
      - CSRF_TRUSTED_ORIGINS=https://tu-dominio.com
```

---

## 📥 Importación de Datos CSV

Para importar datos desde un archivo CSV:

```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Ejecutar script de importación
python import_csv.py
```

El archivo CSV debe tener las siguientes columnas:
- FECHA, ZONA, OPERADOR, CONSULTA, TIPO_VINCULO
- APELLIDO_NOMBRE_INTERLOCUTOR, TELEFONO_INTERLOCUTOR
- APELLIDO_NOMBRE_USUARIO, FECHA_NACIMIENTO, EDAD, SEXO, DNI
- TELEFONO_USUARIO, PROVINCIA, CIUDAD, BARRIO
- TIPO_SUSTANCIA, TIEMPO_CONSUMO, TRATAMIENTO_ANTERIOR, TRATAMIENTO_DESCRIPCION
- OBRA_SOCIAL, OBRA_SOCIAL_NOMBRE, RIESGO_INMINENTE, SEGUIMIENTO
- DEMANDA, DERIVACION, SITUACION_SOCIAL, CARACTERISTICA_JUDICIAL, OBSERVACIONES

---

## 🔐 Permisos y Roles

### Grupo: Operadores
| Permiso | Estado |
|---------|--------|
| Ver consultas propias | ✅ |
| Cargar nuevas consultas | ✅ |
| Editar consultas propias | ✅ |
| Ver informes | ❌ |
| Ver todas las consultas | ❌ |
| Acceso al admin | ❌ |

### Superusuarios (Administradores)
| Permiso | Estado |
|---------|--------|
| Acceso completo a informes | ✅ |
| Ver todas las consultas | ✅ |
| Gestionar usuarios | ✅ |
| Acceso al panel de administración | ✅ |
| Exportar datos | ✅ |

---

## 🌐 Acceso en Red Local

Para acceder desde otros dispositivos en la red:

1. **Ejecutar el servidor con:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Verificar** que `ALLOWED_HOSTS = ['*']` en `settings.py`

3. **Acceder** desde otros dispositivos usando la IP del servidor:
   ```
   http://192.168.x.x:8000
   ```

4. **Encontrar tu IP local:**
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

---

## 🐳 Comandos Docker

### Gestión de Contenedores

```bash
# Construir imagen
docker build -t sistema0800 .

# Iniciar contenedor
docker-compose up -d

# Detener contenedor
docker-compose down

# Reiniciar contenedor
docker-compose restart

# Ver logs
docker logs sistema0800

# Ver logs en tiempo real
docker logs -f sistema0800
```

### Ejecutar Comandos en el Contenedor

```bash
# Acceder al contenedor
docker exec -it sistema0800 bash

# Crear superusuario
docker exec -it sistema0800 python manage.py createsuperuser

# Ejecutar migraciones
docker exec sistema0800 python manage.py migrate

# Shell de Django
docker exec -it sistema0800 python manage.py shell
```

---

## 📝 Comandos Django

### Migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver migraciones pendientes
python manage.py showmigrations
```

### Usuarios

```bash
# Crear superusuario
python manage.py createsuperuser

# Cambiar contraseña
python manage.py changepassword <username>
```

### Otros

```bash
# Shell interactivo
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic

# Verificar configuración
python manage.py check
```

---

## 🔄 Actualizaciones

Para actualizar el sistema:

### Desarrollo Local

```bash
# Obtener cambios
git pull

# Instalar nuevas dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Reiniciar servidor
```

### Docker

```bash
# Obtener cambios
git pull

# Reconstruir y reiniciar
docker-compose down
docker-compose up -d --build

# Ver logs
docker logs sistema0800
```

---

## 🔍 Filtros Disponibles en Informes

| Filtro | Opciones |
|--------|----------|
| Fecha Desde/Hasta | Selector de fecha |
| Zona | Centro-Norte / Sur |
| Tipo de Consulta | Directa / Indirecta |
| Sexo | Masculino / Femenino / Otro / No corresponde |
| Tiempo de Consumo | Menos de 1 año / 1-5 años / 5-10 años / Más de 10 años |
| Tratamiento Anterior | SI / No |
| Situación Social | Situación de Calle / Infancia / Violencia / Pueblos Originarios / Judicializado |
| Característica Judicial | Campo de texto |
| Usuario (nombre) | Campo de texto |
| Ciudad | Campo de texto |
| Tipo de Sustancia | Campo de texto |
| Operador | Selector de operador |
| Riesgo Inminente | Emergencia / Urgencia / Ninguno |
| Seguimiento | 24hs / 48hs |

---

## 🐛 Solución de Problemas

### El servidor no inicia
```bash
# Verificar que el puerto no esté en uso
netstat -ano | findstr :8000

# Matar proceso si es necesario
taskkill /PID <numero_pid> /F
```

### Error de migraciones
```bash
# Resetear migraciones (cuidado: borra datos)
python manage.py migrate consultas zero
python manage.py migrate
```

### Problemas con Docker
```bash
# Limpiar contenedores e imágenes
docker system prune -a

# Reconstruir desde cero
docker-compose down -v
docker-compose up -d --build
```

### Gráficos no se muestran
- Verificar que Plotly esté instalado: `pip install plotly`
- Revisar la consola del navegador para errores JavaScript
- Asegurar que hay datos en la base de datos

---

## 📞 URLs del Sistema

| URL | Descripción | Acceso |
|-----|-------------|--------|
| `/` | Página de inicio | Público |
| `/login/` | Inicio de sesión | Público |
| `/logout/` | Cerrar sesión | Autenticado |
| `/cargar/` | Cargar nueva consulta | Autenticado |
| `/mis-consultas/` | Ver mis consultas | Autenticado |
| `/consulta/<id>/` | Detalle de consulta | Autenticado |
| `/consulta/<id>/editar/` | Editar consulta | Autenticado |
| `/informes/` | Panel de informes | Solo Admin |
| `/admin/` | Panel de administración | Solo Admin |

---

## 📄 Licencia

Este proyecto es de uso interno para la línea 0800-268-5640 de atención en adicciones.

---

## 👨‍💻 Desarrollo

**Repositorio:** https://github.com/francofx/sis0800

---

*Desarrollado con ❤️ para la gestión de consultas de la línea 0800-268-5640*
