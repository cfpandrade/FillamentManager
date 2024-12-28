FROM python:3.10-slim

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios de trabajo
WORKDIR /app
COPY . /app

# Instalar dependencias de Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto para el servicio Flask
EXPOSE 5000

# Ejecutar el script de inicio
CMD [ "/bin/bash", "/app/run.sh" ]
