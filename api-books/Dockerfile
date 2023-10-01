FROM python:3.11-slim

# Instala las herramientas necesarias para construir mysqlclient y pkg-config
RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

# Establece el directorio de trabajo en /app
WORKDIR /compose

# Copia el archivo de requerimientos (requirements.txt) a la imagen
COPY req.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r req.txt
RUN pip install psycopg2-binary

# Copia todo el contenido de tu aplicación al directorio de trabajo en la imagen
COPY . .

# Expon el puerto en el que se ejecuta tu aplicación Flask
EXPOSE 8000

# Define el comando para ejecutar tu aplicación
CMD ["python", "app.py"]