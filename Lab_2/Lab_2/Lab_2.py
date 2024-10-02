
class Client:
    def __init__(self, client_id, name, surname, phone_number):
        self.client_id = client_id
        self.name = name
        self.surname = surname
        self.phone_number = phone_number

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_phone_number(self):
        return self.phone_number

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    def display_client_info(self):
        print(f"Client: {self.name} {self.surname}, Phone: {self.phone_number}")

    def update_phone_number(self, new_phone):
        self.phone_number = new_phone
        print(f"Phone number updated to: {self.phone_number}")


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
