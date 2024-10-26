from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask import Flask, jsonify, request, render_template
import pymysql

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Coloca tu contraseña de MySQL si tienes
app.config['MYSQL_DB'] = 'reservas'

# Crear la conexión manualmente usando pymysql
def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

# Inicialización de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tourist_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ruta para obtener todas las reservas
# Obtener todas las reservas
@app.route('/reservas', methods=['GET'])
def get_reservas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM reservas')
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reservas)

# Crear una nueva reserva
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

    app.run(debug=True)
