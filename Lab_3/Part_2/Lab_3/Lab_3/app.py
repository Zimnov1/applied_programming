import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from Lab_3 import Database, Repository, Client, Device, Worker
from functools import wraps
from flask import request, jsonify

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'psvyjd13579')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'Lab_3')

mysql = MySQL(app)

def check_auth(username, password):
    return username == 'admin' and password == 'password'

def authenticate():
    return jsonify({'message': 'Authentication required'}), 401

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/clients', methods=['GET'])
@requires_auth
def get_clients():
    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)
    clients = repo.get_all_clients()
    db.close()
    return jsonify([{'id': client.id, 'full_name': client.full_name} for client in clients])

@app.route('/clients', methods=['POST'])
@requires_auth
def add_client():
    data = request.get_json()
    required_fields = ['name', 'surname', 'phone_number', 'email', 'address']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing field: {field}'}), 400
    
    new_client = Client(None, data['name'], data['surname'], data['phone_number'], data['email'], data['address'])
    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)
    repo.add_client(new_client)
    db.close()
    return jsonify({'message': 'Client added successfully.'}), 201

@app.route('/clients/<int:client_id>', methods=['PUT'])
@requires_auth
def update_client(client_id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    app.logger.info(f'Updating client {client_id} with data: {data}')

    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)

    client = repo.get_client_by_id(client_id)
    if not client:
        db.close()
        return jsonify({'message': 'Client not found'}), 404

    client.name = data.get('name', client.name)
    client.surname = data.get('surname', client.surname)
    client.phone_number = data.get('phone_number', client.phone_number)
    client.email = data.get('email', client.email)
    client.address = data.get('address', client.address)

    try:
        repo.update_client(client)
    except Exception as e:
        db.close()
        return jsonify({'message': f'Error updating client: {str(e)}'}), 500

    db.close()
    return jsonify({'message': 'Client updated successfully.'})

@app.route('/clients/<int:client_id>', methods=['DELETE'])
@requires_auth
def delete_client(client_id):
    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)

    client = repo.get_client_by_id(client_id)
    if not client:
        db.close()
        return jsonify({'message': 'Client not found'}), 404

    repo.delete_client(client_id)
    db.close()
    return jsonify({'message': 'Client deleted successfully.'})

@app.route('/devices', methods=['POST'])
@requires_auth
def add_device():
    data = request.get_json()
    required_fields = ['serial_number', 'device_type', 'brand', 'model']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing field: {field}'}), 400

    new_device = Device(data['serial_number'], data['device_type'], data['brand'], data['model'])
    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)

    try:
        repo.add_device(new_device)
        return jsonify({'message': 'Device added successfully.'}), 201
    except Exception as e:
        return jsonify({'message': f'Error adding device: {str(e)}'}), 500
    finally:
        db.close()

@app.route('/devices', methods=['GET'])
@requires_auth
def get_devices():
    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)
    devices = repo.get_all_devices()
    db.close()
    return jsonify([{'serial_number': device.serial_number, 'brand': device.brand, 'model': device.model} for device in devices])

@app.route('/devices/<serial_number>', methods=['PUT'])
@requires_auth
def update_device(serial_number):
    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)

    data = request.get_json()

    try:
        device = repo.get_device_by_serial_number(serial_number)
        if not device:
            return jsonify({'message': 'Device not found'}), 404

        device.device_type = data.get('device_type', device.device_type)
        device.brand = data.get('brand', device.brand)
        device.model = data.get('model', device.model)

        repo.update_device(device)
        return jsonify({'message': 'Device updated successfully.'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@app.route('/devices/<serial_number>', methods=['DELETE'])
@requires_auth
def delete_device(serial_number):
    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)

    try:
        device = repo.get_device_by_serial_number(serial_number)
        if not device:
            return jsonify({'message': 'Device not found'}), 404

        repo.delete_device(serial_number)
        return jsonify({'message': 'Device deleted successfully.'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@app.route('/worker', methods=['GET'])
@requires_auth
def get_workers():
    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)
    workers = repo.get_all_workers()
    db.close()
    return jsonify([{'id': worker.id, 'name': worker.name, 'surname': worker.surname} for worker in workers])

@app.route('/worker', methods=['POST'])
@requires_auth
def add_worker():
    data = request.get_json()
    required_fields = ['name', 'surname', 'phone_number', 'city_of_residence', 'street', 'position']  
    for field in required_fields:
        if field not in data:  
            return jsonify({'message': f'Missing or empty field: {field}'}), 400

    new_worker = Worker(
        None, 
        data['name'], 
        data['surname'], 
        None,  
        data['phone_number'], 
        data['city_of_residence'], 
        data['street'], 
        None, 
        data['position']
    ) 
    
    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)

    try:
        repo.add_worker(new_worker)
        return jsonify({'message': 'Worker added successfully.'}), 201
    except Exception as e:
        return jsonify({'message': f'Error adding worker: {str(e)}'}), 500
    finally:
        db.close()

@app.route('/worker/<int:worker_id>', methods=['PUT'])
@requires_auth
def update_worker(worker_id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)

    worker = repo.get_worker_by_id(worker_id)
    if not worker:
        db.close()
        return jsonify({'message': 'Worker not found'}), 404

    worker.name = data.get('name', worker.name)
    worker.surname = data.get('surname', worker.surname)

    if 'phone_number' not in data or not data['phone_number']:
        db.close()
        return jsonify({'message': 'phone_number cannot be null or empty'}), 400
    worker.phone_number = data['phone_number']  

    try:
        repo.update_worker(worker)
        return jsonify({'message': 'Worker updated successfully.'}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating worker: {str(e)}'}), 500
    finally:
        db.close()

@app.route('/worker/<int:worker_id>', methods=['DELETE'])
def delete_worker(worker_id):
    db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    repo = Repository(db)

    try:
        repo.delete_worker(worker_id)
        return jsonify({'message': 'Worker deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting worker: {str(e)}'}), 500
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
