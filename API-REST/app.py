import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

# Conexión a la base de datos
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',        # Cambia esto si tu servidor está en otro lugar
        user='tu_usuario',       # Tu nombre de usuario de MySQL
        password='tu_contraseña', # Tu contraseña de MySQL
        database='reservas_hotel' # El nombre de tu base de datos
    )
    return conn

# Crear la tabla si no existe
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(100) NOT NULL,
            fecha_reserva DATE NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Ruta para obtener todas las reservas
@app.route('/reservas', methods=['GET'])
def get_reservas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Para obtener resultados como diccionarios
    cursor.execute('SELECT * FROM reservas')
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reservas)

# Ruta para crear una nueva reserva
@app.route('/reservas', methods=['POST'])
def create_reserva():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reservas (nombre, correo, fecha_reserva) VALUES (%s, %s, %s)',
                   (data['nombre'], data['correo'], data['fecha_reserva']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'nombre': data['nombre'], 'correo': data['correo'], 'fecha_reserva': data['fecha_reserva']}), 201

# Ruta para actualizar una reserva existente
@app.route('/reservas/<int:id>', methods=['PUT'])
def update_reserva(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE reservas SET nombre = %s, correo = %s, fecha_reserva = %s WHERE id = %s',
                   (data['nombre'], data['correo'], data['fecha_reserva'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'id': id, 'nombre': data['nombre'], 'correo': data['correo'], 'fecha_reserva': data['fecha_reserva']})

# Ruta para eliminar una reserva
@app.route('/reservas/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reservas WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Reserva eliminada con éxito'})

if __name__ == '__main__':
    init_db()  # Inicializa la base de datos
    app.run(debug=True)
