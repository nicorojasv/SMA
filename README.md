# Sistema de Gestión Ambiental

## Descripción

Sistema de gestión ambiental desarrollado para la **Superintendencia del Medio Ambiente de Chile (SMA)**. Este proyecto proporciona una API RESTful para la gestión de medidas, planes reportes y documentos ambientales, permitiendo el seguimiento y control de las medidas implementadas por diferentes Organismos sectoriales.

## Explicación del Uso

El Sistema de Gestión Ambiental está diseñado para facilitar la gestión y seguimiento de planes y medidas ambientales en Chile. El sistema permite:

- **Administración de Organismos Sectoriales**: Gestionar los organismos sectoriales responsables de implementar las medidas.
- **Control de Medidas**: Permite definir, clasificar y monitorear medidas ambientales, asociadas a planes específicos.
- **Gestión de Planes**: Crear, actualizar y dar seguimiento a planes ambientales asociado a medidas.
- **Sistema de Reportes**: Generar y almacenar reportes sobre el avance de las medidas ambientales.
- **Gestión Documental**: Almacenar y gestionar documentos relacionados con los planes y medidas.

El sistema está orientado a usuarios/as de la Superintendencia del Medio Ambiente y organismos sectoriales, permitiendo un control centralizado de todas las actividades ambientales bajo su responsabilidad.

## Características

### Características Funcionales
- Administración de organismos sectoriales
- Gestión de planes ambientales
- Seguimiento y control de medidas ambientales
- Sistema de reportes y documentación ambiental
- Autenticación por medio de rut chileno
- Gestión de documentos ambientales
- Control de acceso basado en permisos

### Características Técnicas
- API RESTful con Django REST Framework
- Documentación automática de API con drf-spectacular
- Sistema de autenticación con RUT chileno
- Pruebas automatizadas con pytest
- Configuración mediante variables de entorno
- Base de datos PostgreSQL
- Serialización de datos con DRF
- Validaciones personalizadas
- Sistema de migraciones de base de datos
- Interfaz de administración (Django admin)

## Tecnologías

### Backend
- Python 3.x
- Django 5.1.5
- Django REST Framework 3.15.2
- PostgreSQL
- pytest
- factory-boy
- drf-spectacular

### Documentación
- Swagger UI para documentación de API
- ReDoc para documentación alternativa
- Documentación de código con docstrings

## Requisitos Previos

### Software
- Python 3.x
- PostgreSQL
- pip (gestor de paquetes de Python)
- Git

## Instalación

1. **Clonar el repositorio**

   Puede usar **HTTPS** o **SSH**, según su configuración de GitHub:

   - Clonar con HTTPS:
     ```bash
     git clone https://github.com/nicorojasv/SMA.git
     ```

   - Clonar con SSH:
     ```bash
     git clone git@github.com:nicorojasv/SMA.git
     ```

   Luego acceder al directorio:

   ```bash
   cd SMA
   ```

2. **Crear y activar un entorno virtual**

   En macOS o Linux:
   ```bash
   python -m venv env
   source env/bin/activate
   ```

   En Windows:
   ```bash
   python -m venv env
   env\Scripts\activate
   ```

3. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno**

   Copiar el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

   Esto copiará el archivo `.env.example` a `.env`, donde deberá ingresar sus configuraciones de entorno para la conexión con PostgreSQL.

5. **Aplicar las migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear un superusuario**
   ```bash
   python manage.py createsuperuser
   ```

## Uso

### Desarrollo
```bash
python manage.py runserver
```

### Pruebas
Para ejecutar las pruebas, utilizar el siguiente comando:
```bash
python -m pytest -v
```

**Importante**: Antes de correr las pruebas, asegurarse de:
1. Tener el entorno virtual activado
2. Configurar las variables de entorno 

## Estructura del Proyecto

```
SMA/
├── SMA/                   # Configuración principal del proyecto
│   ├── settings.py        # Configuraciones del proyecto
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuración WSGI
├── plan/                  # Aplicación principal
│   ├── migrations/        # Migraciones de la aplicación plan 
│   ├── templates/         # Plantillas HTML
│   │   ├── base.html      # Plantilla base
│   │   ├── home.html      # Página principal
│   │   ├── signin.html    # Página de inicio de sesión
│   │   ├── signup.html    # Página de registro
│   │   ├── panel_sma.html # Panel de administración (sólo demostración)
│   │   └── _navbar.html   # Barra de navegación
│   ├── tests/             # Pruebas automatizadas
│   │   ├── test_models.py # Pruebas de modelos
│   │   ├── test_views.py  # Pruebas de vistas
│   │   ├── test_forms.py  # Pruebas de formularios
│   │   ├── test_serializers.py # Pruebas de serializadores
│   │   ├── test_utils.py  # Pruebas de utilidades
│   │   └── __init__.py    # Inicializador de pruebas
│   ├── admin.py           # Configuración del panel de administración
│   ├── apps.py            # Configuración de la aplicación plan
│   ├── forms.py           # Formularios de la aplicación plan
│   ├── models.py          # Modelos: Plan, Medida, OrganismoSectorial, etc.
│   ├── serializers.py     # Serializadores de datos
│   ├── utils.py           # Utilidades
│   └── views.py           # Lógica de negocio y vistas
├── .env.example           # Variables de entorno de ejemplo
├── requirements.txt       # Dependencias del proyecto
└── manage.py             # Script de gestión de Django
```

## Documentación de la API

La documentación de la API está disponible en:

- Swagger UI: http://127.0.0.1:8000/api/docs/
- Esquema OpenAPI: http://127.0.0.1:8000/api/schema/

## Contacto

- Camila Oyarzún
- Stefanya Pulgar
- Nicolas Rojas
- luis Paillan
- Cristóbal Gajardo
- Carlos Azócar

## Estado del Proyecto

🟢 En desarrollo activo

## Métricas del Proyecto

- Documentación API: 100%
- Versión actual: 1.0


sss