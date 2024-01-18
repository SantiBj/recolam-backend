from rest_framework import serializers
from ..models import Trip
from .customerSerializers import CustomerSerializer

class TripSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    details = serializers.CharField(required=False)

    class Meta:
        model = Trip
        fields = "__all__"

class TripWithCustomerSerializer(serializers.ModelSerializer):
    user = CustomerSerializer()
    class Meta:
        model = Trip
        fields = "__all__"

class TripInfoTruckAndCustomerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    truck = serializers.CharField()
    user = serializers.CharField()
    scheduleDay = serializers.DateField()
    address= serializers.CharField()
    initialDateCompany = serializers.DateTimeField()
    endDateCompany = serializers.DateTimeField()
    initialDateCustomer = serializers.DateTimeField()
    endDateCustomer = serializers.DateTimeField()
    details = serializers.CharField()
    isComplete = serializers.BooleanField()
    isDisable = serializers.BooleanField()
    truckTraveling = serializers.BooleanField()

class TripWithOldTruckAssignedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    truck = serializers.CharField()
    user = CustomerSerializer()
    scheduleDay = serializers.DateField()
    address= serializers.CharField()
    initialDateCompany = serializers.DateTimeField()
    endDateCompany = serializers.DateTimeField()
    initialDateCustomer = serializers.DateTimeField()
    endDateCustomer = serializers.DateTimeField()
    details = serializers.CharField()
    isComplete = serializers.BooleanField()
    isDisable = serializers.BooleanField()
    oldTruckAssigned = serializers.CharField()


class PartialSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    truck = serializers.CharField(required=False)
    user = serializers.CharField(required=False)
    scheduleDay = serializers.DateField(required=False)
    details = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = Trip
        fields = "__all__"
