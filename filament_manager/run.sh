#!/bin/bash

# Inicializar base de datos si no existe
DB_PATH="/data/filament_inventory.db"
if [ ! -f "$DB_PATH" ]; then
  echo "Creando base de datos en $DB_PATH..."
  sqlite3 "$DB_PATH" <<EOF
CREATE TABLE IF NOT EXISTS filamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    color TEXT NOT NULL,
    peso_total REAL NOT NULL,
    peso_restante REAL NOT NULL,
    marca TEXT,
    ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
EOF
fi

# Ejecutar aplicación principal
python3 app.py
