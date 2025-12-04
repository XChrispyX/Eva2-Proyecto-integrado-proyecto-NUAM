# Proyecto NUAM – Gestión de Calificaciones Tributarias

**Integrantes:**

- Michelle Villalobos  
- Christian Aguila  
- Diego Poblete  

**Carrera:** Analista Programador – INACAP  
**Profesor:** Javier Arturo García Barrientos  
**Fecha:** Octubre 2025 - Diciembre 2025   

---

## 📌 Descripción General

Sistema web desarrollado en **Django** para la gestión de **calificaciones tributarias** de la empresa **NUAM**, entidad financiera que integra mercados de **Chile, Perú y Colombia**.

El proyecto se compone de:

- Backend principal en **Django** (`nuam_app`)
- **Microservicio de monedas** en **FastAPI** (`monedas_service`)
- Integración con **Apache2** como *reverse proxy* con **HTTPS** usando certificados generados con **mkcert**
- Integración con **Kafka** (productor y consumidor) usando `docker-compose`
- Dashboard de visualización de datos y gráficos de monedas
- Logging estructurado y manejo de errores

---

## 🧱 Arquitectura General

- **Django (nuam_app)**  
  - CRUD de calificaciones tributarias  
  - API REST principal (`/api/calificaciones/`, `/api/convertir-monto/`)  
  - Dashboard y vistas HTML

- **Microservicio de Monedas (monedas_service)**  
  - Implementado con **FastAPI**  
  - Endpoint principal: `GET /api/monedas/`  
  - Consulta a API externa HTTPS `https://open.er-api.com/v6/latest/CLP`  
  - Fallback con valores por defecto si la API externa falla

- **Kafka + Zookeeper (Docker)**  
  - Productor: envía eventos al topic `nuam_calificaciones` al crear calificaciones  
  - Consumidor: procesa mensajes desde `manage.py run_kafka_consumer`

- **Apache2 + HTTPS (mkcert)**  
  - Termina la conexión HTTPS en `https://localhost`  
  - Actúa como **reverse proxy** hacia el contenedor Docker `nuam_app`  
  - Opcionalmente puede exponer endpoints internos como `/api/monedas/`

---

## 🚀 Funcionalidades Principales

- Crear, listar, editar y eliminar calificaciones tributarias
- Selección de moneda (**CLP / PEN / COP**, más soporte a COL/SOL/UF en el microservicio)
- Panel administrativo de Django
- API REST completa (GET, POST, PUT/PATCH, DELETE)
- Conversión de montos usando API externa HTTPS
- Microservicio FastAPI para valores de **COL, CLP, SOL, UF**
- Dashboard con gráficos de monedas y datos actualizados
- Integración con **Kafka** (productor y consumidor)
- Logging en archivo `nuam.log`
- Despliegue mediante **Docker** + **Apache2** con **HTTPS**

---

## 🛠 Tecnologías Utilizadas

- **Lenguaje:** Python 3.12  
- **Framework web:** Django 5.2.7  
- **Microservicios:** FastAPI 0.123.0 + Uvicorn  
- **Base de datos:** SQLite3 (modo desarrollo)  
- **Frontend:** HTML5, CSS3, JavaScript  
- **Mensajería:** Kafka + Zookeeper (imágenes `wurstmeister/*`)  
- **Contenedores:** Docker y Docker Compose  
- **Servidor web / reverse proxy:** Apache2 (XAMPP en Windows / nativo en Linux)  
- **Certificados:** mkcert (CA local y certificados válidos para `localhost`)  
- **API externa de monedas:** `https://open.er-api.com/v6/latest/CLP` (HTTPS)  

---

# 📦 Instalación y Ejecución

## 1️⃣ Clonar el repositorio
``git clone https://github.com/XChrispyX/Eva2-Proyecto-integrado-proyecto-NUAM.git``

``cd Eva2-Proyecto-integrado-proyecto-NUAM``

# 2️⃣ Modo Desarrollo con Entorno Virtual (.venv)
# 2.1 Windows
# Crear entorno virtual
``python -m venv .venv``

# Activar entorno virtual
``.venv\Scripts\activate``

# Actualizar pip e instalar dependencias
``pip install --upgrade pip``
``pip install -r requirements.txt``

# Migrar base de datos
``python manage.py makemigrations``
``python manage.py migrate``

# Crear superusuario
``python manage.py createsuperuser``

# Ejecutar servidor Django
``python manage.py runserver``

Acceder en:
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/

En este modo, el microservicio FastAPI se puede ejecutar aparte con:
python -m uvicorn monedas_service.app:app --reload --port 8001
# Endpoint: http://127.0.0.1:8001/api/monedas/

# 3️⃣ Ejecución con Docker (Windows y Linux)
El proyecto incluye un Dockerfile y un docker-compose.yml que levantan:

- nuam_app → Django

- monedas_service → FastAPI

- kafka

- zookeeper

# Levantar todo el entorno

``docker-compose up -d --build``

# Aplicar migraciones dentro del contenedor

``docker-compose exec nuam_app python manage.py migrate``

# Crear superusuario (Docker)

``docker-compose exec nuam_app python manage.py createsuperuser``

# Ejecutar el consumer de Kafka

``docker-compose exec nuam_app python manage.py run_kafka_consumer``

La aplicacion queda disponible en:

http://localhost:8080/ → Django (nuam_app)

http://localhost:8001/api/monedas/ → microservicio FastAPI

# 🌐 Configuración de HTTPS con Apache2 y mkcert
El sistema se despliega con Apache2 como reverse proxy, usando HTTPS con certificados generados por mkcert.
El flujo es: 
Navegador (https://localhost)  →  Apache2 (443, HTTPS) →  http://127.0.0.1:8080  (contenedor nuam_app)

# 4️⃣ Windows – Apache2 (XAMPP) + mkcert

Generar certificados con mkcert

# Instalar mkcert (Windows)
Descargar desde el repositorio oficial: 

https://github.com/FiloSottile/mkcert/releases 

y agregar al PATH.

# Instalar la CA local

``mkcert -install``

# Generar certificado para localhost:

``mkcert localhost 127.0.0.1 ::1``

# Copiar los archivos generados a XAMPP, por ejemplo:

C:\xampp\apache\crt\localhost+2.pem

C:\xampp\apache\crt\localhost+2-key.pem

# Configurar VirtualHost HTTPS en XAMPP
Editar C:\xampp\apache\conf\extra\httpd-ssl.conf y agregar un bloque similar:

<VirtualHost _default_:443>
    ServerName localhost

    SSLEngine on
    SSLCertificateFile "C:/xampp/apache/crt/localhost+2.pem"
    SSLCertificateKeyFile "C:/xampp/apache/crt/localhost+2-key.pem"

    ProxyRequests Off
    ProxyPreserveHost On

    # Reverse Proxy hacia el contenedor Django (nuam_app → puerto 8080)
    ProxyPass        /  http://127.0.0.1:8080/
    ProxyPassReverse /  http://127.0.0.1:8080/

    RequestHeader set X-Forwarded-Proto "https"

    ErrorLog "logs/ssl-error.log"
    CustomLog "logs/ssl-access.log" combined
</VirtualHost>

# Habilitar los módulos necesarios en XAMPP:

mod_ssl 

mod_proxy

mod_proxy_http

mod_headers

Reiniciar Apache desde el panel de XAMPP.

# Ahora se puede acceder al sistema en:

https://localhost/ (certificado válido por mkcert)

# 5️⃣ Linux – Apache2 nativo + mkcert

# Instalar Apache2 y modulos

``sudo apt update``

``sudo apt install apache2``

``sudo a2enmod ssl``

``sudo a2enmod proxy``

``sudo a2enmod proxy_http``

``sudo a2enmod headers``

``sudo systemctl restart apache2``

# Instalar mkcert en Linux
``sudo apt install libnss3-tools``

``wget https://github.com/FiloSottile/mkcert/releases/latest/download/mkcert-linux-amd64 -O mkcert``

``chmod +x mkcert``

``sudo mv mkcert /usr/local/bin/``

# Instalar la CA local:

``mkcert -install``

# Generar certificado para localhost:

``mkcert localhost 127.0.0.1 ::1``

# Mover los certificados:

``sudo mkdir -p /etc/apache2/certs``
``sudo mv localhost+2.pem /etc/apache2/certs/nuam-localhost.pem``
``sudo mv localhost+2-key.pem /etc/apache2/certs/nuam-localhost-key.pem``

# VirtualHost HTTPS en Linux

Crear archivo de sitio, por ejemplo:

``sudo nano /etc/apache2/sites-available/nuam-https.conf``

# Contenido:

<VirtualHost *:443>
    ServerName localhost

    SSLEngine on
    SSLCertificateFile /etc/apache2/certs/nuam-localhost.pem
    SSLCertificateKeyFile /etc/apache2/certs/nuam-localhost-key.pem

    ProxyRequests Off
    ProxyPreserveHost On

    # Reverse Proxy hacia el contenedor Django (nuam_app → puerto 8080)
    ProxyPass        /  http://127.0.0.1:8080/
    ProxyPassReverse /  http://127.0.0.1:8080/

    RequestHeader set X-Forwarded-Proto "https"

    ErrorLog ${APACHE_LOG_DIR}/nuam-ssl-error.log
    CustomLog ${APACHE_LOG_DIR}/nuam-ssl-access.log combined
</VirtualHost>

# Habilitar el sitio y el puerto 443

``sudo a2ensite nuam-https.conf``
``sudo a2enmod ssl``
``sudo systemctl reload apache2``

Con Docker corriendo (docker-compose up -d --build), el sistema queda disponible en:

https://localhost/ (HTTPS válido, reverse proxy a Django en Docker)

# 🔄 Microservicio de Monedas (FastAPI)
Ruta: monedas_service/app.py

Endpoint principal: GET /api/monedas/

Consulta https://open.er-api.com/v6/latest/CLP

Obtiene tasas para:

COP (Colombia)

PEN (Perú – Sol)

CLF (UF)

Si la API externa falla, usa valores por defecto:

{
  "CLP": 1,
  "COL": 0.004,
  "SOL": 0.0035,
  "UF": 0.000027,
  "source": "default_error"
}

# Definición en docker-compose.yml
monedas_service:
  build: .
  container_name: monedas_service
  volumes:
    - .:/app
  depends_on:
    - kafka
  working_dir: /app/monedas_service
  command: uvicorn app:app --host 0.0.0.0 --port 8001
  ports:
    - "8001:8001"

# 🔄 Consumo desde Django (Dashboard)

En core_app/views.py, el dashboard llama al microservicio de monedas usando
la URL configurable definida en settings.MONEDAS_API_URL:

import requests
from django.conf import settings

def dashboard_monedas(request):
    api_url = settings.MONEDAS_API_URL  # se lee desde settings.py

    resp = requests.get(api_url, timeout=5)
    data = resp.json()
    # Datos se usan para gráficos y visualización en el dashboard

# 📡 API REST (Django)

# Obtener todas las calificaciones

GET /api/calificaciones/

# Crear calificación

POST /api/calificaciones/
Content-Type: application/json

{
  "rut_empresa": "11111111-1",
  "anio": 2025,
  "instrumento": "Acciones",
  "monto": 1500000,
  "moneda": "CLP"
}
# Detalle / Modificación / Eliminación
GET    /api/calificaciones/<id>/
PUT    /api/calificaciones/<id>/
PATCH  /api/calificaciones/<id>/
DELETE /api/calificaciones/<id>/

# Conversión de moneda (HTTPS)
POST /api/convertir-monto/
Content-Type: application/json

{
  "monto": 1000,
  "moneda_origen": "CLP",
  "moneda_destino": "PEN"
}

# 📡 Kafka – Productor y Consumidor

# Productor
Cada vez que se crea una calificación, se envía un mensaje JSON al topic:

nuam_calificaciones

con información relevante de la calificación tributaria.

# Consumidor

Ejecutar el consumidor dentro del contenedor:

docker-compose exec nuam_app python manage.py run_kafka_consumer

Si Kafka está activo, aparecerán mensajes en consola al crear registros nuevos.

# 📝 Logging y Manejo de Errores

El sistema implementa:

Logging estructurado en archivo nuam.log

Manejo de excepciones con try/except en vistas y microservicio

Respuestas JSON claras para errores de API

Validación de campos faltantes o datos inválidos

Manejo de errores de conexión hacia:

Kafka (productor/consumidor)

API externa de monedas

Microservicio FastAPI