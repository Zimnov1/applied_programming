from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = "client"

    def __str__(self):
        return f"{self.name} {self.surname}"

class Device(models.Model):
    serial_number = models.CharField(max_length=50, unique=True, primary_key=True)
    type = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    class Meta:
        db_table = "device"

    def __str__(self):
        return f"{self.type} - {self.brand} - {self.model}"

class Worker(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    city_of_residence = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    apartment = models.CharField(max_length=10, null=True, blank=True)
    position = models.CharField(max_length=50)

    class Meta:
        db_table = "worker"

    def __str__(self):
        return f"{self.name} {self.surname}"

class RepairApplication(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    description = models.TextField()
    planned_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    device_serial_number = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "repair_application"

class Repair(models.Model):
    application = models.OneToOneField(RepairApplication, on_delete=models.CASCADE, unique=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = "repair"

class WorkerInRepair(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE)

    class Meta:
        db_table = "worker_in_repair"
        unique_together = ['worker', 'repair']

class SparePart(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField()
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE)

    class Meta:
        db_table = "spare_part"

class EquipmentForSale(models.Model):
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    device_serial_number = models.CharField(max_length=255, default='default_value')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, to_field='serial_number', related_name='equipments')

    class Meta:
        db_table = "equipment_for_sale"

    def __str__(self):
        return f"{self.name} {self.model} ({self.status})"

class Meta:
    indexes = [
        models.Index(fields=['device_serial_number'], name='idx_device_serial_number'),
        models.Index(fields=['device_serial_number'], name='idx_device_serial_number_equipment')
    ]
