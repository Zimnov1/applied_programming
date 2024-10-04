class Client:
    client_counter = 0  

    def __init__(self, client_id, name, surname, phone_number):
        self.client_id = client_id
        self.name = name
        self.surname = surname
        self.__phone_number = phone_number  
        Client.client_counter += 1  

    @staticmethod
    def client_count():
        return Client.client_counter  

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value

    def display_client_info(self):
        print(f"Client: {self.name} {self.surname}, Phone: {self.__phone_number}")

    def update_phone_number(self, new_phone):
        self.phone_number = new_phone
        print(f"Phone number updated to: {self.__phone_number}")


class Payment:
    def process_payment(self, amount):
        print(f"Processing payment of ${amount}")


class Device:
    def __init__(self, device_id, type, brand):
        self.device_id = device_id
        self.type = type
        self.brand = brand

    def display_device_info(self):
        print(f"Device: {self.brand} {self.type}")


class RepairApplication(Client, Device, Payment):
    def __init__(self, application_id, status, planned_price, client_id, name, surname, phone, device_id, type, brand):
        Client.__init__(self, client_id, name, surname, phone)
        Device.__init__(self, device_id, type, brand)
        self.application_id = application_id
        self.status = status
        self.planned_price = planned_price

    def display_application_info(self):
        self.display_client_info()
        self.display_device_info()
        print(f"Application ID: {self.application_id}, Status: {self.status}, Planned Price: ${self.planned_price}")

    def process_payment(self, amount):
        super().process_payment(amount)  
        print(f"Payment for repair application {self.application_id}: ${amount}")


class Worker(Client):
    def __init__(self, client_id, name, surname, phone, worker_id, position):
        super().__init__(client_id, name, surname, phone)
        self.worker_id = worker_id
        self.position = position

    def display_worker_info(self):
        self.display_client_info()
        print(f"Worker ID: {self.worker_id}, Position: {self.position}")

    def assign_repair(self, application_id):
        print(f"Worker assigned to repair application {application_id}")


class Technician(Payment):
    def __init__(self, tech_id, name, surname):
        self.tech_id = tech_id
        self.name = name
        self.surname = surname

    def display_technician_info(self):
        print(f"Technician: {self.name} {self.surname}, ID: {self.tech_id}")

    def process_payment(self, amount):
        super().process_payment(amount)
        print(f"Technician payment processed for ${amount}")


class RepairWorker(Worker, Technician):
    def __init__(self, client_id, name, surname, phone, worker_id, position, tech_id):
        Worker.__init__(self, client_id, name, surname, phone, worker_id, position)
        Technician.__init__(self, tech_id, name, surname)

    def display_repair_worker_info(self):
        self.display_worker_info()
        self.display_technician_info()


client1 = Client(1, "John", "Doe", "123-456-789")
client1.display_client_info()
client1.update_phone_number("987-654-321")

worker1 = Worker(2, "Michael", "Smith", "987-654-123", 101, "Technician")
worker1.display_worker_info()

app1 = RepairApplication(1001, "In Progress", 250.75, 1, "John", "Doe", "987-654-321", 2001, "Laptop", "Dell")
app1.display_application_info()

app2 = RepairApplication(1002, "Completed", 150.50, 3, "Alice", "Johnson", "555-123-456", 2002, "Phone", "Samsung")
app2.display_application_info()

app1.process_payment(250.75)
app2.process_payment(150.50)

worker1.assign_repair(1001)

tech_worker = RepairWorker(3, "Sarah", "Connor", "555-987-654", 102, "Senior Technician", 201)
tech_worker.display_repair_worker_info()
tech_worker.process_payment(300.00)

print(f"Total clients: {Client.client_count()}")  
