from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "/data/filament_inventory.db"

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/filamentos", methods=["GET"])
def get_filamentos():
    filamentos = query_db("SELECT * FROM filamentos")
    return jsonify([{"id": f[0], "nombre": f[1], "tipo": f[2], "color": f[3], "peso_total": f[4], "peso_restante": f[5], "marca": f[6], "ultima_actualizacion": f[7]} for f in filamentos])

@app.route("/filamentos", methods=["POST"])
def add_filamento():
    data = request.json
    query_db("INSERT INTO filamentos (nombre, tipo, color, peso_total, peso_restante, marca) VALUES (?, ?, ?, ?, ?, ?)", 
             (data["nombre"], data["tipo"], data["color"], data["peso_total"], data["peso_restante"], data.get("marca")))
    return jsonify({"message": "Filamento agregado"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
