import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

# Conexión a la base de datos MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',  # Cambia esto si tu servidor está en otro lugar
        user='tu_usuario',
        password='tu_contraseña',
        database='nombre_de_tu_base_de_datos'
    )
    return conn


# Crear la tabla si no existe
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            fecha_reserva TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ruta para obtener todas las reservas
@app.route('/reservas', methods=['GET'])
def get_reservas():
    conn = get_db_connection()
    reservas = conn.execute('SELECT * FROM reservas').fetchall()
    conn.close()
    return jsonify([dict(reserva) for reserva in reservas])

# Ruta para crear una nueva reserva
@app.route('/reservas', methods=['POST'])
def create_reserva():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO reservas (nombre, correo, fecha_reserva) VALUES (?, ?, ?)',
                 (data['nombre'], data['correo'], data['fecha_reserva']))
    conn.commit()
    conn.close()
    return jsonify({'nombre': data['nombre'], 'correo': data['correo'], 'fecha_reserva': data['fecha_reserva']}), 201

# Ruta para actualizar una reserva existente
@app.route('/reservas/<int:id>', methods=['PUT'])
def update_reserva(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE reservas SET nombre = ?, correo = ?, fecha_reserva = ? WHERE id = ?',
                 (data['nombre'], data['correo'], data['fecha_reserva'], id))
    conn.commit()
    conn.close()
    return jsonify({'id': id, 'nombre': data['nombre'], 'correo': data['correo'], 'fecha_reserva': data['fecha_reserva']})

# Ruta para eliminar una reserva
@app.route('/reservas/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM reservas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Reserva eliminada con éxito'})

if __name__ == '__main__':
    init_db()  # Inicializa la base de datos
    app.run(debug=True)
