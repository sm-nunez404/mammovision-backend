# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requerimientos al contenedor
COPY requirements.txt .

# Actualizar pip y herramientas esenciales del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    musl-dev \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Actualizar pip antes de instalar dependencias
RUN python -m pip install --upgrade pip

# Instalar las dependencias del archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Establecer el comando por defecto para ejecutar la aplicación
# Cambia "app:app" por tu punto de entrada si usas Flask o algún otro framework
CMD ["python", "app.py"]

# Exponer el puerto 10000
EXPOSE 10000
