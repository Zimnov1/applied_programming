import mysql.connector
import os
from flask import Flask, render_template, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = os.urandom(24)

class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def close(self):
        self.cursor.close()
        self.connection.close()

class Repository:
    def __init__(self, db):
        self.db = db

    def get_all_clients(self):
        try:
            self.db.cursor.execute("SELECT id, name, surname, phone_number, email, address FROM client")
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching clients: {e}")
            return []

    def get_client_by_id(self, client_id):
        self.db.cursor.execute("SELECT id, name, surname, phone_number, email, address FROM client WHERE id = %s", (client_id,))
        return self.db.cursor.fetchone()

    def add_client(self, client):
        self.db.cursor.execute(
            "INSERT INTO client (name, surname, phone_number, email, address) VALUES (%s, %s, %s, %s, %s)",
            (client['name'], client['surname'], client['phone_number'], client['email'], client['address'])
        )
        self.db.connection.commit()

    def update_client(self, client):
        try:
            query = """
            UPDATE client
            SET name = %s, surname = %s, phone_number = %s, email = %s, address = %s
            WHERE id = %s
            """
            self.db.cursor.execute(query, (client['name'], client['surname'], client['phone_number'], client['email'], client['address'], client['id']))
            self.db.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error updating client: {err}")

    def delete_client(self, client_id):
        try:
            self.db.cursor.execute("DELETE FROM client WHERE id = %s", (client_id,))
            self.db.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error deleting client: {err}")

    def get_all_devices(self):
        self.db.cursor.execute("SELECT type, serial_number, model, brand FROM device")
        return self.db.cursor.fetchall()

    def get_device_by_serial_number(self, serial_number):
        self.db.cursor.execute("SELECT type, serial_number, model, brand FROM device WHERE serial_number = %s", (serial_number,))
        return self.db.cursor.fetchone()

    def update_device(self, device):
        self.db.cursor.execute(
            "UPDATE device SET type = %s, serial_number = %s, model = %s, brand = %s WHERE serial_number = %s",
            (device['type'], device['serial_number'], device['model'], device['brand'], device['serial_number'])
        )
        self.db.connection.commit()

    def add_device(self, device):
        try:
            self.db.cursor.execute(
                "INSERT INTO device (type, serial_number, model, brand) VALUES (%s, %s, %s, %s)",
                (device['type'], device['serial_number'], device['model'], device['brand'])
            )
            self.db.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error adding device: {err}")
            raise


    def delete_device(self, serial_number):
        try:
            self.db.cursor.execute("DELETE FROM device WHERE serial_number = %s", (serial_number,))
            self.db.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error deleting device: {err}")
            raise

    def get_all_workers(self):
        self.db.cursor.execute("SELECT id, name, surname, phone_number, city_of_residence, street, position FROM worker")
        return self.db.cursor.fetchall()

    def add_worker(self, worker):
        self.db.cursor.execute(
            "INSERT INTO worker (name, surname, position, phone_number, city_of_residence, street) VALUES (%s, %s, %s, %s, %s, %s)",
            (worker['name'], worker['surname'], worker['position'], worker['phone_number'], worker['city_of_residence'], worker['street'])
        )
        self.db.connection.commit()

    def update_worker(self, worker):
        self.db.cursor.execute(
            "UPDATE worker SET name = %s, surname = %s, position = %s, phone_number = %s, city_of_residence = %s, street = %s WHERE id = %s",
            (worker['name'], worker['surname'], worker['position'], worker['phone_number'], worker['city_of_residence'], worker['street'], worker['id'])
        )
        self.db.connection.commit()

    def get_worker_by_id(self, worker_id):
        self.db.cursor.execute("SELECT id, name, surname, position, phone_number, city_of_residence, street FROM worker WHERE id = %s", (worker_id,))
        return self.db.cursor.fetchone()

    def delete_worker(self, worker_id):
        self.db.cursor.execute("DELETE FROM worker WHERE id = %s", (worker_id,))
        self.db.connection.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clients')
def clients():
    try:
        db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
        repo = Repository(db)
        clients = repo.get_all_clients()
        db.close()
        return render_template('client.html', clients=clients, current_tab='clients')
    except Exception as e:
        print(f"Error: {e}")
        return "Error"

@app.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        client = {
            'name': request.form['name'],
            'surname': request.form['surname'],
            'phone_number': request.form['phone_number'],
            'email': request.form['email'],
            'address': request.form['address']
        }
        db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
        repo = Repository(db)
        repo.add_client(client)
        db.close()
        flash('Client added successfully!')
        return redirect(url_for('clients')) 

@app.route('/delete_client/<int:client_id>')
def delete_client(client_id):
    db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
    repo = Repository(db)
    repo.delete_client(client_id)
    db.close()
    flash('Client deleted successfully!')
    return redirect(url_for('clients')) 

@app.route('/edit_client/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
    repo = Repository(db)

    if request.method == 'POST':
        client = {
            'id': client_id,
            'name': request.form['name'],
            'surname': request.form['surname'],
            'phone_number': request.form['phone_number'],
            'email': request.form['email'],
            'address': request.form['address']
        }
        repo.update_client(client)
        flash('Client updated successfully!')
        db.close()
        return redirect(url_for('clients')) 

    client_data = repo.get_client_by_id(client_id)
    db.close()

    if not client_data:
        flash('Client not found!')
        return redirect(url_for('clients'))

    return render_template('edit_client.html', client=client_data)

@app.route('/devices')
def devices():
    try:
        db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
        repo = Repository(db)
        devices = repo.get_all_devices()
        print("Devices fetched successfully")  
        db.close()
        return render_template('devices.html', devices=devices, current_tab='devices')
    except Exception as e:
        print(f"Error in devices route: {e}")
        return "Error fetching devices", 500

@app.route('/add_device', methods=['POST'])
def add_device():
    device = {
        'type': request.form['type'],
        'brand': request.form['brand'],
        'model': request.form['model'],
        'serial_number': request.form['serial_number']
    }
    db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
    repo = Repository(db)
    repo.add_device(device)
    db.close()
    flash('Device added successfully!')
    return redirect(url_for('devices'))

@app.route('/delete_device/<string:serial_number>')
def delete_device(serial_number):
    try:
        db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
        repo = Repository(db)
        repo.delete_device(serial_number)
        flash('Device deleted successfully!')
    except Exception as e:
        print(f"Error in delete_device route: {e}")
        flash('Error deleting device! Please try again.')
    finally:
        db.close()
    return redirect(url_for('devices'))

@app.route('/edit_device/<string:serial_number>', methods=['GET', 'POST'])
def edit_device(serial_number):
    db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
    repo = Repository(db)

    if request.method == 'POST':
        device = {
            'type': request.form['type'],
            'serial_number': serial_number,  
            'model': request.form['model'],
            'brand': request.form['brand']
        }
        repo.update_device(device)
        flash('Device updated successfully!')
        db.close()
        return redirect(url_for('devices'))

    device_data = repo.get_device_by_serial_number(serial_number)
    db.close()

    if not device_data:
        flash('Device not found!')
        return redirect(url_for('devices'))

    return render_template('edit_device.html', device=device_data)

@app.route('/workers')
def workers():
    db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
    repo = Repository(db)
    workers = repo.get_all_workers()
    db.close()
    return render_template('workers.html', workers=workers, current_tab='workers')

@app.route('/add_worker', methods=['POST'])
def add_worker():
    worker = {
        'name': request.form['name'],
        'surname': request.form['surname'],
        'position': request.form['position'],
        'phone_number': request.form['phone_number'],  
        'city_of_residence': request.form['city_of_residence'], 
        'street': request.form['street'] 
    }
    db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
    repo = Repository(db)
    repo.add_worker(worker)
    db.close()
    flash('Worker added successfully!')
    return redirect(url_for('workers'))

@app.route('/delete_worker/<int:worker_id>')
def delete_worker(worker_id):
    db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
    repo = Repository(db)
    repo.delete_worker(worker_id)
    db.close()
    flash('Worker deleted successfully!')
    return redirect(url_for('workers'))

@app.route('/edit_worker/<int:worker_id>', methods=['GET', 'POST'])
def edit_worker(worker_id):
    db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
    repo = Repository(db)

    if request.method == 'POST':
        worker = {
            'id': worker_id,
            'name': request.form['name'],
            'surname': request.form['surname'],
            'position': request.form['position'],
            'phone_number': request.form['phone_number'],  
            'city_of_residence': request.form['city_of_residence'],  
            'street': request.form['street'] 
        }
        repo.update_worker(worker)
        flash('Worker updated successfully!')
        db.close()
        return redirect(url_for('workers'))

    worker_data = repo.get_worker_by_id(worker_id)
    db.close()

    if not worker_data:
        flash('Worker not found!')
        return redirect(url_for('workers'))

    return render_template('edit_worker.html', worker=worker_data)

if __name__ == "__main__":
    app.run(debug=True)
