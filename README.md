# 🏢 Gestión de Prácticas DRF

Este proyecto es una plataforma desarrollada con Django y Django REST Framework para la gestión de prácticas profesionales, integrando distintas entidades como estudiantes, empresas, prácticas, y asignaciones.

---

## Inicialización Rápida

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/MartinezHU/gestion-practicas-drf.git
   cd gestion-practicas-drf
   ```

2. **Crea y activa un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos (ver apartado abajo para Supabase):**
   - Las configuraciones y credenciales de base de datos se encuentran en `main/settings/base.py`.
   - Puedes adaptarlas para producción usando variables de entorno (`CONNECTION_STRING`).

5. **Aplica migraciones:**
   ```bash
   python manage.py migrate
   ```

6. **Arranca el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

---

## Base de Datos: Uso con Supabase

- El proyecto está preparado para funcionar con **Supabase** como backend de base de datos, aprovechando la compatibilidad de Supabase con PostgreSQL mediante el ORM de Django.
- En la configuración (`main/settings/base.py`) puedes especificar la cadena de conexión de tu proyecto Supabase usando la variable de entorno `CONNECTION_STRING` en el formato:
  ```
  postgres://usuario:password@host:puerto/dbname
  ```
- Además, se incluye la librería oficial de **supabase-py** en los requisitos para poder interactuar con Supabase directamente, permitiendo ejecutar tareas sobre la base de datos fuera del ORM de Django (útil para sincronización, tareas asíncronas, o lógica avanzada).  
  Ejemplo mínimo:
  ```python
  from supabase import create_client, Client

  supabase_url = "https://tu-proyecto.supabase.co"
  supabase_key = "tu-supabase-key"
  supabase: Client = create_client(supabase_url, supabase_key)
  data = supabase.table("nombre_tabla").select("*").execute()
  ```
- Puedes consultar la [documentación oficial](https://supabase.com/docs/reference/python/introduction) para aprovechar toda la potencia de Supabase desde Python.

---

## Estructura del Proyecto

```
gestion-practicas-drf/
├── apps/
│   ├── core/           # Modelos y lógica central de usuarios
│   ├── students/       # Lógica y vistas para estudiantes
│   ├── companies/      # Empresas colaboradoras
│   ├── internships/    # Prácticas gestionadas
│   ├── matches/        # Asignación de estudiantes a prácticas
├── main/
│   ├── __init__.py
│   ├── asgi.py         # Configuración para ASGI
│   ├── celery.py       # Configuración e integración con Celery
│   ├── logging.py      # Configuración y utilidades de logging
│   ├── settings/       # Configuración modular por entorno
│   │   ├── base.py     # Configuración base común
│   │   ├── dev.py      # Configuración específica de desarrollo
│   │   └── installed_apps.py
│   ├── urls.py         # Rutas principales de la API y administración
│   └── wsgi.py         # Configuración para WSGI
├── requirements.txt
└── README.md
```

---

## Configuración Modular

- Separación de la configuración en la carpeta `main/settings/`:
  - `base.py`: configuración general y principal del proyecto, incluyendo la cadena de conexión para Supabase/PostgreSQL.
  - `dev.py`: importa `base.py` y permite sobreescribir para desarrollo.
  - `installed_apps.py`: define las apps instaladas, tanto core de Django como propias (`apps.core`, `apps.students`, etc).

---

## Principales Librerías Utilizadas

- **Django**: Framework principal.
- **Django REST framework**: Para APIs RESTful.
- **Celery**: Para tareas asíncronas (ver integración abajo).
- **django-cors-headers**: Control de CORS para seguridad en APIs.
- **dj-database-url**: Ayuda en la configuración flexible de bases de datos.
- **supabase-py**: Para acceso directo a Supabase cuando sea necesario.
- **Otros:** Puedes consultar el archivo `requirements.txt` para el listado completo.

---

## Integración Celery (Tareas Asíncronas)

- Para utilizar tareas en segundo plano, el proyecto usa Celery configurado en `main/celery.py`.
- La integración está inicializada en el `__init__.py` de `main`.
- **Configuración principal:**
  ```python
  app = Celery('main')
  app.config_from_object('django.conf:settings', namespace='CELERY')
  app.autodiscover_tasks()
  ```
- **Para arrancar worker de Celery:**
  ```bash
  celery -A main worker --loglevel=info
  ```
- La variable de entorno `DJANGO_SETTINGS_MODULE` debe estar en `'main.settings.dev'` (desarrollo), se puede personalizar.

---

## Gestión de Usuarios

- El modelo de usuario personalizado es `APIUser` (apps/core/models.py) que permite ampliar atributos y elegir la app de origen.
- Está configurado desde cero y se usa como modelo principal en toda la plataforma (`AUTH_USER_MODEL = "core.APIUser"`).

---

## Logging Personalizado

- El sistema de logging personalizado adapta el logger de Django, centrado en eventos de API (ver `main/logging.py`).
- Ejemplo de uso a través de decoradores:
  ```python
  @log_api_call(level="info")
  def dispatch(self, request, *args, **kwargs):
      ...
  ```
- El log contiene información enriquecida contextual (usuario, método, endpoint, estado y errores).

---

## Endpoints Principales

- El endpoint administrativo: `/admin/`
- Endpoints REST:
  - `/api/users/` (gestión de usuarios, vía APIUserViewSet)
  - `/rest-auth/` (autenticación vía DRF)
  - Otras rutas agregadas dinámicamente para los modelos definidos en cada app.
