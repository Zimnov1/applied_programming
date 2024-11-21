from rest_framework import serializers

class RepairsCountSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    repairs_count = serializers.IntegerField()

class InProgressRepairsSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    device_serial_number = serializers.CharField()
    description = serializers.CharField()
    planned_price = serializers.DecimalField(max_digits=10, decimal_places=2)

class SparePartsCountSerializer(serializers.Serializer):
    model = serializers.CharField()
    count = serializers.IntegerField()

class ClientsWithMultipleRepairsSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()

class SparePartsSortedByPriceSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class DevicesInRepairSerializer(serializers.Serializer):
    device_serial_number = serializers.CharField()
    status = serializers.CharField()
    planned_price = serializers.DecimalField(max_digits=10, decimal_places=2)
