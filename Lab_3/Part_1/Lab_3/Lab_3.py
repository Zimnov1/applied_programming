import mysql.connector

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
        self.db.cursor.execute(
            "INSERT INTO worker (name, surname, middle_name, phone_number, city_of_residence, street, apartment, position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (worker.name, worker.surname, worker.middle_name, worker.phone_number, worker.city_of_residence, worker.street, worker.apartment, worker.position)
        )
        self.db.connection.commit()

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

    new_device = Device('SN1678236874', 'Laptop', 'Lenovo', 'IdeaPad 330')
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

    smart_device = SmartDevice("SN234227854", "Smartphone", "Samsung", "Galaxy S21", "Android 10")
    smart_device.display_info()
    smart_device.upgrade_os("Android 11")

    new_worker = Worker(None, 'Vitaly', 'Took', phone_number='0994652784', city_of_residence='Lviv', street='Veluka', apartment='10', position='Technician')
    repo.add_worker(new_worker)

    db.close()
