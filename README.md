# Proyecto NUAM – Gestión de Calificaciones Tributarias

**Integrantes:**  
- Michelle Villalobos  
- Christian Aguila  
- Diego Poblete  

**Carrera:** Analista Programador – INACAP  
**Profesor:** Javier Arturo García Barrientos  
**Fecha:** Octubre 2025  

---

## 📌 Descripción General

Sistema web desarrollado en **Django**, orientado a la gestión de calificaciones tributarias para la empresa **NUAM**, entidad financiera que integra mercados de Chile, Perú y Colombia.

El proyecto incluye:

- CRUD completo de calificaciones tributarias  
- Gestión de usuarios y roles  
- Conversión de montos entre **CLP, PEN y COP** mediante API externa HTTPS  
- API REST propia para operar vía JSON  
- Integración con **Kafka (Producer / Consumer)** mediante docker-compose  
- Logging estructurado y manejo de errores  

---

## 🚀 Funcionalidades Principales

- Crear, listar, editar y eliminar calificaciones tributarias  
- Selección de moneda (CLP / PEN / COP)  
- Panel administrativo de Django  
- API REST completa (GET, POST, PUT/PATCH, DELETE)  
- Conversión de moneda vía API HTTPS  
- Producer Kafka (envío de datos al topic)  
- Consumer Kafka (lectura de eventos)  
- Logging en archivo `nuam.log`

---

## 🛠 Tecnologías Utilizadas

- Python 3.13  
- Django 5.2.7  
- SQLite3  
- HTML5 / CSS3 / JavaScript  
- API externa: https://api.exchangerate.host (HTTPS)  
- Kafka + Zookeeper (Docker)  
- Docker y Docker Compose  
- Entorno virtual `.venv`

---

# 📦 **Ejecución del Proyecto (Modo Local con .venv)**

### 1️⃣ Clonar el repositorio

git clone https://github.com/MiKhali01/NUAM_BackEnd.git
cd NUAM_BackEnd

# Clonar el repositorio
git clone https://github.com/XChrispyX/Eva2-Proyecto-integrado-proyecto-NUAM.git
cd Eva2-Proyecto-integrado-proyecto-NUAM

### Crear y activar el entorno virtual

Windows

python -m venv .venv
.venv\Scripts\activate

Linux/Mac

python3 -m venv .venv
source .venv/bin/activat

### Instalar dependencias

pip install -r requirements.txt

### Migrar base de datos

python manage.py makemigrations
python manage.py migrate

### Crear superusuario

python manage.py createsuperuser


### Ejecutar servidor

python manage.py runserver

Acceder en:
👉 http://127.0.0.1:8000

👉 http://127.0.0.1:8000/admin

### 🐳 Ejecución con Docker

El proyecto incluye un Dockerfile y un docker-compose.yml listo para levantar:

- Django (nuam_app)

- Kafka

- Zookeeper

### Levantar todo el entorno
docker-compose up -d --build

### Aplicar migraciones dentro del contenedor
docker-compose exec nuam_app python manage.py migrate

### Crear superusuario
docker-compose exec nuam_app python manage.py createsuperuser

### Ejecutar el consumer Kafka
docker-compose exec nuam_app python manage.py run_kafka_consumer


La aplicación queda disponible en:
👉 http://localhost:8080

### 🌐 API REST

### Obtener todas las calificaciones
GET /api/calificaciones/

### Crear calificacion
POST /api/calificaciones/
Content-Type: application/json
{
  "rut_empresa": "11111111-1",
  "anio": 2025,
  "instrumento": "Acciones",
  "monto": 1500000,
  "moneda": "CLP"
}
### Detalle / Modificacion / Eliminacion
GET    /api/calificaciones/<id>/
PUT    /api/calificaciones/<id>/
PATCH  /api/calificaciones/<id>/
DELETE /api/calificaciones/<id>/

### Conversion de moneda (HTTPS)
POST /api/convertir-monto/
{
  "monto": 1000,
  "moneda_origen": "CLP",
  "moneda_destino": "PEN"
}

### 📡 Kafka – Productor y Consumidor
## Productor

Cada vez que se crea una calificación, se envía un mensaje JSON al topic:

nuam_calificaciones


## Consumidor

Ejecutar:

docker-compose exec nuam_app python manage.py run_kafka_consumer

Si Kafka está activo, aparecerán mensajes al crear registros.

### 📝 Logging y Manejo de Errores

El sistema implementa:

Logging estructurado en archivo nuam.log

Manejo de errores con try/except

Respuestas JSON claras para errores de API

Validación de campos faltantes

Manejo de errores de Kafka (producto, consumidor)

## Estructura del proyecto
NUAM_BackEnd/
│
├── core_app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── signals.py
│   ├── management/
│   │   └── commands/run_kafka_consumer.py
│   └── templates/
│
├── nuam/
│   ├── settings.py
│   ├── urls.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
