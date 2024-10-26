from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tourist_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

# Modelo para la tabla reservas
class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(255), nullable=False)
    fecha_reserva = db.Column(db.Date, nullable=False)

# Ruta para obtener todas las reservas
@app.route('/reservas', methods=['GET'])
def get_reservas():
    reservas = Reserva.query.all()
    return jsonify([{
        'id': r.id,
        'nombre': r.nombre,
        'correo': r.correo,
        'fecha_reserva': r.fecha_reserva.isoformat()
    } for r in reservas])

# Crear una nueva reserva
@app.route('/reservas', methods=['POST'])
def create_reserva():
    data = request.get_json()
    if not all(k in data for k in ('nombre', 'correo', 'fecha_reserva')):
        return jsonify({'error': 'Faltan datos necesarios'}), 400
    
    nueva_reserva = Reserva(
        nombre=data['nombre'],
        correo=data['correo'],
        fecha_reserva=data['fecha_reserva']
    )
    
    db.session.add(nueva_reserva)
    db.session.commit()
    return jsonify({'id': nueva_reserva.id, 'nombre': nueva_reserva.nombre, 'correo': nueva_reserva.correo, 'fecha_reserva': nueva_reserva.fecha_reserva}), 201

# Ruta para actualizar una reserva existente
@app.route('/reservas/<int:id>', methods=['PUT'])
def update_reserva(id):
    data = request.get_json()
    reserva = Reserva.query.get_or_404(id)
    reserva.nombre = data.get('nombre', reserva.nombre)
    reserva.correo = data.get('correo', reserva.correo)
    reserva.fecha_reserva = data.get('fecha_reserva', reserva.fecha_reserva)
    
    db.session.commit()
    return jsonify({'id': reserva.id, 'nombre': reserva.nombre, 'correo': reserva.correo, 'fecha_reserva': reserva.fecha_reserva})

# Ruta para eliminar una reserva
@app.route('/reservas/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    db.session.delete(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva eliminada con éxito'})

if __name__ == '__main__':
    app.run(debug=True)
