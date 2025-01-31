from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = "/data/filament_inventory.db"

# Función para interactuar con la base de datos
def query_db(query, args=(), commit=False, fetch_one=False, fetch_all=False):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, args)
            if commit:
                conn.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# Ruta para servir la interfaz gráfica
@app.route("/")
def index():
    return send_from_directory("web", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("web", path)

# Ruta para obtener todos los filamentos
@app.route("/filamentos", methods=["GET"])
def get_filamentos():
    filamentos = query_db("SELECT * FROM filamentos", fetch_all=True)
    if not filamentos:
        return jsonify({"message": "No se encontraron filamentos"}), 404
    return jsonify([{
        "id": f[0],
        "nombre": f[1],
        "tipo": f[2],
        "color": f[3],
        "peso_total": f[4],
        "peso_restante": f[5],
        "marca": f[6],
        "cantidad": f[7],
        "ultima_actualizacion": f[8]
    } for f in filamentos])

# Ruta para agregar un nuevo filamento
@app.route("/filamentos", methods=["POST"])
def add_filamento():
    try:
        data = request.json
        query_db("""
            INSERT INTO filamentos (nombre, tipo, color, peso_total, peso_restante, marca, cantidad)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["nombre"], 
            data["tipo"], 
            data["color"], 
            data["peso_total"], 
            data["peso_restante"], 
            data.get("marca"), 
            data.get("cantidad", 0)
        ), commit=True)
        return jsonify({"message": "Filamento agregado"}), 201
    except KeyError as e:
        return jsonify({"error": f"Falta el campo: {str(e)}"}), 400

# Ruta para actualizar un filamento
@app.route("/filamentos/<int:id>", methods=["PUT"])
def update_filamento(id):
    try:
        data = request.json
        result = query_db("""
            UPDATE filamentos
            SET nombre = ?, tipo = ?, color = ?, peso_total = ?, peso_restante = ?, marca = ?, cantidad = ?, ultima_actualizacion = ?
            WHERE id = ?
        """, (
            data["nombre"], 
            data["tipo"], 
            data["color"], 
            data["peso_total"], 
            data["peso_restante"], 
            data.get("marca"), 
            data.get("cantidad"), 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            id
        ), commit=True)
        if result is None:
            return jsonify({"message": "Filamento no encontrado"}), 404
        return jsonify({"message": "Filamento actualizado"}), 200
    except KeyError as e:
        return jsonify({"error": f"Falta el campo: {str(e)}"}), 400

# Ruta para eliminar un filamento
@app.route("/filamentos/<int:id>", methods=["DELETE"])
def delete_filamento(id):
    query_db("DELETE FROM filamentos WHERE id = ?", (id,), commit=True)
    return jsonify({"message": "Filamento eliminado"}), 200

# Manejadores de errores globales
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
