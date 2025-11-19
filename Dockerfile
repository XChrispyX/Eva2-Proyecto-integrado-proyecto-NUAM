# Imagen base de Python
FROM python:3.12

# Evitar que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Evitar que la salida se almacene en buffer
ENV PYTHONUNBUFFERED 1

# Carpeta de trabajo
WORKDIR /app

# Copiar primero los archivos de dependencias
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . /app/

# Exponer el puerto 8000 (el que usa Django)
EXPOSE 8000

# Comando por defecto para ejecutar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
