# Proyecto NUAM Gestión de Calificaciones Tributarias

Desarrollado por: Michelle Villalobos, Christian Aguila y Diego Poblete
Carrera: Analista Programador - INACAP  
Profesor: Javier Arturo Garcia Barrientos
Fecha: Octubre 2025

## Descripción del Proyecto
Aplicación web desarrollada en Django, que permite gestionar las calificaciones tributarias de la empresa NUAM, integrando los mercados financieros de Chile, Perú y Colombia.  
El sistema soporta operaciones en tres monedas (CLP, PEN y COP), con CRUD completo de registros y almacenamiento seguro en base de datos.

## Funcionalidades Principales
- CRUD de calificaciones tributarias.
- Campo de tipo de moneda (CLP / PEN / COP).
- Roles y usuarios.
- Validación de datos.
- Panel de administración (superusuario Django).
- Interfaz visual con HTML, CSS y JavaScript.

## Tecnologías Utilizadas
- Python 3.13  
- Django 5.2.7  
- SQLite3  
- HTML5 / CSS3 / JavaScript  
- Entorno virtual `.venv`

## Instalación y Configuración


# Clonar el repositorio
git clone https://github.com/XChrispyX/NUAM_BackEnd.git
cd NUAM_BackEnd

# Crear entorno virtual
python -m venv .venv
# Activar entorno
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Migrar base de datos
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar el servidor
python manage.py runserver
