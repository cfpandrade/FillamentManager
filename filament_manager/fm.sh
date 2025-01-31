#!/bin/bash

# Borrar todos los docker
docker ps -a -q --filter "status=exited" | xargs docker rm 2>/dev/null

# Detener todos los contenedores en ejecución
docker stop $(docker ps -q)

# Construir la imagen de Docker
docker build -t filament_manager .

# Ejecutar el contenedor
docker run -d -p 5000:5000 -v $(pwd)/data:/data filament_manager

clear

docker ps

