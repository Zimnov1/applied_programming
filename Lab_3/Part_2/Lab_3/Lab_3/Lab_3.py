import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

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

class Entity:
    def display_info(self):
        pass

class Client(Entity):
    discount_rate = 0.1

    def __init__(self, id, name, surname, phone_number, email, address):
        self.id = id
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.email = email
        self.address = address

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"

    def apply_discount(self, amount):
        return amount * (1 - Client.discount_rate)

    def display_info(self):
        print(f"Client: {self.full_name}, Phone: {self.phone_number}")

    @staticmethod
    def get_discount_info():
        return f"Current discount for clients: {Client.discount_rate * 100}%"

class CorporateClient(Client):
    def __init__(self, id, name, surname, phone_number, company_name):
        super().__init__(id, name, surname, phone_number, None, None) 
        self.company_name = company_name

    def display_info(self):
        print(f"Corporate Client: {self.company_name}, Name: {self.full_name}")

class Device(Entity):
    def __init__(self, serial_number, device_type, brand, model):
        self.serial_number = serial_number
        self.device_type = device_type
        self.brand = brand
        self.model = model

    @property
    def device_info(self):
        return f"{self.brand} {self.model}"

    def perform_diagnosis(self):
        print(f"Diagnosis of device {self.device_info} completed.")

    def display_info(self):
        print(f"Device: {self.device_info}, Serial Number: {self.serial_number}")

class Worker:
    def __init__(self, id, name, surname, middle_name=None, phone_number=None, city_of_residence=None, street=None, apartment=None, position=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.middle_name = middle_name
        self.phone_number = phone_number
        self.city_of_residence = city_of_residence
        self.street = street
        self.apartment = apartment
        self.position = position

class SmartDevice(Device):
    def __init__(self, serial_number, device_type, brand, model, os_version):
        super().__init__(serial_number, device_type, brand, model)
        self.os_version = os_version

    def upgrade_os(self, new_version):
        self.os_version = new_version
        print(f"Operating system upgraded to version {self.os_version}")

    def display_info(self):
        print(f"Smart Device: {self.device_info} with OS version {self.os_version}")

class Repository:
    def __init__(self, db):
        self.db = db

    def get_client_by_id(self, client_id):
        try:
            self.db.cursor.execute("SELECT id, name, surname, phone_number, email, address FROM client WHERE id = %s", (client_id,))
            row = self.db.cursor.fetchone()
            if row:
                return Client(**row)
            return None
        except mysql.connector.Error as err:
            print(f"Error fetching client: {err}")
            return None

    def update_client(self, client):
        try:
            self.db.cursor.execute(
                "UPDATE client SET name = %s, surname = %s, phone_number = %s, email = %s, address = %s WHERE id = %s",
                (client.name, client.surname, client.phone_number, client.email, client.address, client.id)
            )
            self.db.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error updating client: {err}")

    def delete_client(self, client_id):
        try:
            self.db.cursor.execute("DELETE FROM client WHERE id = %s", (client_id,))
            self.db.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error deleting client: {err}")

    def update_device(self, device):
        try:
            self.db.cursor.execute(
                "UPDATE device SET type = %s, brand = %s, model = %s WHERE serial_number = %s",
                (device.device_type, device.brand, device.model, device.serial_number)
            )
            self.db.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error updating device: {err}")

    def delete_device(self, serial_number):
        try:
            self.db.cursor.execute("DELETE FROM device WHERE serial_number = %s", (serial_number,))
            self.db.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error deleting device: {err}")

    def get_all_clients(self):
        self.db.cursor.execute("SELECT id, name, surname, phone_number, email, address FROM client")
        return [Client(**row) for row in self.db.cursor.fetchall()]

    def add_client(self, client):
        self.db.cursor.execute(
            "INSERT INTO client (name, surname, phone_number, email, address) VALUES (%s, %s, %s, %s, %s)",
            (client.name, client.surname, client.phone_number, client.email, client.address)
        )
        self.db.connection.commit()

    def get_all_devices(self):
        self.db.cursor.execute("SELECT serial_number, type AS device_type, brand, model FROM device")
        return [Device(**row) for row in self.db.cursor.fetchall()]

    def add_device(self, device):
        self.db.cursor.execute(
            "INSERT INTO device (serial_number, type, brand, model) VALUES (%s, %s, %s, %s)",
            (device.serial_number, device.device_type, device.brand, device.model)
        )
        self.db.connection.commit()

    def get_all_workers(self):
        self.db.cursor.execute("SELECT id, name, surname, middle_name, phone_number, city_of_residence, street, apartment, position FROM worker")
        return [Worker(**row) for row in self.db.cursor.fetchall()]

    def add_worker(self, worker):
        try:
            cursor = self.db.connection.cursor() 
            cursor.execute(
                "INSERT INTO worker (name, surname, middle_name, phone_number, city_of_residence, street, apartment, position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (worker.name, worker.surname, worker.middle_name, worker.phone_number, worker.city_of_residence, worker.street, worker.apartment, worker.position)
            )
            self.db.connection.commit()
            cursor.close() 
        except mysql.connector.Error as err:
            print(f"Error adding worker: {err}")

    def update_worker(self, worker):
        try:
            cursor = self.db.connection.cursor() 
            cursor.execute(
                "UPDATE worker SET name = %s, surname = %s, middle_name = %s, phone_number = %s, city_of_residence = %s, street = %s, apartment = %s, position = %s WHERE id = %s",
                (worker.name, worker.surname, worker.middle_name, worker.phone_number, worker.city_of_residence, worker.street, worker.apartment, worker.position, worker.id)
            )
            self.db.connection.commit()  
            cursor.close() 
        except mysql.connector.Error as err:
            print(f"Error updating worker: {err}")

    def delete_worker(self, worker_id):
        try:
            cursor = self.db.connection.cursor()  
            cursor.execute("DELETE FROM worker WHERE id = %s", (worker_id,))
            self.db.connection.commit() 
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error deleting worker: {err}")

    def get_worker_by_id(self, worker_id):
        try:
            cursor = self.db.connection.cursor()  
            cursor.execute("SELECT * FROM worker WHERE id = %s", (worker_id,))
            row = cursor.fetchone()
            cursor.close()
            return Worker(*row) if row else None
        except mysql.connector.Error as err:
            print(f"Error fetching worker: {err}")
            return None

    def get_repo():
        db = Database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
        return db, Repository(db)

    def get_device_by_serial_number(self, serial_number):
        try:
            self.db.cursor.execute("SELECT serial_number, type AS device_type, brand, model FROM device WHERE serial_number = %s", (serial_number,))
            row = self.db.cursor.fetchone()
            if row:
                return Device(**row)
            return None
        except mysql.connector.Error as err:
            print(f"Error fetching device: {err}")
            return None

if __name__ == "__main__":
    db = Database(host="localhost", user="root", password="psvyjd13579", database="Lab_3")
    repo = Repository(db)

    clients = repo.get_all_clients()
    print("Clients:")
    for client in clients:
        print(client.full_name)

    new_client = Client(None, 'Sergiy', 'Zimnov', '0631761091', 'zimnovs3@gmail.com', 'Shevchenka 15-A')
    repo.add_client(new_client)

    devices = repo.get_all_devices()
    print("\nDevices:")
    for device in devices:
        device.display_info()

    new_device = Device('SN167823871', 'Laptop', 'Lenovo', 'IdeaPad 330')
    repo.add_device(new_device)

    workers = repo.get_all_workers()
    print("\nWorkers:")
    for worker in workers:
        print(f"{worker.name} {worker.surname}")

    client = Client(1, "Ivan", "Petrenko", "0987654321", "ivanp4@gmail.com", "Mazepu 4")
    client.display_info()
    print(client.apply_discount(1000))
    print(Client.get_discount_info())

    corp_client = CorporateClient(2, "Petro", "Ivanenko", "0981234567", "TechCorp")
    corp_client.display_info()

    device = Device("SN1125521346", "Laptop", "Dell", "XPS 13")
    device.display_info()
    device.perform_diagnosis()

    smart_device = SmartDevice("SN234227854", "Smartphone", "Samsung", "Galaxy S21", "11.0")
    smart_device.display_info()
    smart_device.upgrade_os("12.0")
    
    db.close()
