CREATE TABLE IF NOT EXISTS filamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    color TEXT NOT NULL,
    peso_total INTEGER NOT NULL,
    peso_restante INTEGER NOT NULL,
    marca TEXT,
    cantidad INTEGER DEFAULT 0,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
