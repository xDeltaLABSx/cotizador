# models/client_model.py
import sqlite3
import os

DB_PATH = os.path.join("data", "cotizaciones_delta.db")

def init_client_db():
    """
    Crea la tabla de clientes para recordar historiales sin duplicados.
    """
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_atencion TEXT NOT NULL,
            cargo_departamento TEXT,
            empresa TEXT NOT NULL,
            correo TEXT,
            telefono TEXT,
            ultimo_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def guardar_o_actualizar_cliente(nombre_atencion, cargo, empresa, correo="", telefono=""):
    """
    Guarda un nuevo cliente o actualiza su última fecha de interacción.
    """
    init_client_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id FROM clientes 
        WHERE empresa = ? AND nombre_atencion = ?
    ''', (empresa, nombre_atencion))
    resultado = cursor.fetchone()
    
    if resultado:
        cliente_id = resultado[0]
        cursor.execute('''
            UPDATE clientes 
            SET cargo_departamento = ?, correo = ?, telefono = ?, ultimo_registro = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (cargo, correo, telefono, cliente_id))
    else:
        cursor.execute('''
            INSERT INTO clientes (nombre_atencion, cargo_departamento, empresa, correo, telefono)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre_atencion, cargo, empresa, correo, telefono))
        cliente_id = cursor.lastrowid
        
    conn.commit()
    conn.close()
    return cliente_id

def buscar_clientes(termino=""):
    """
    Búsqueda inteligente para autocompletar formularios.
    Retorna tuplas que incluyen el ID para facilitar el borrado.
    """
    init_client_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"%{termino}%"
    cursor.execute('''
        SELECT id, nombre_atencion, cargo_departamento, empresa, correo, telefono 
        FROM clientes 
        WHERE empresa LIKE ? OR nombre_atencion LIKE ?
        ORDER BY ultimo_registro DESC
        LIMIT 10
    ''', (query, query))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_todos_los_clientes():
    """
    Retorna absolutamente todos los clientes registrados para la vista de administración.
    """
    init_client_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, nombre_atencion, cargo_departamento, empresa, correo, telefono, ultimo_registro 
        FROM clientes 
        ORDER BY ultimo_registro DESC
    ''')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def eliminar_cliente(cliente_id):
    """
    Elimina un cliente de la base de datos local por su ID.
    """
    init_client_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    conn.close()
