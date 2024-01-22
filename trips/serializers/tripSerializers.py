from rest_framework import serializers
from ..models import Trip
from .customerSerializers import CustomerSerializer
from ..service.tripsService import truckBusy

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

class TripTruck(serializers.ModelSerializer):
    truckBusy = serializers.SerializerMethodField()
    
    class Meta:
        model = Trip
        fields = "__all__"

    def get_truckBusy(self,instance)->bool:
        try:
            truckBusy(instance)
            return True
        except:
            return False

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


class SerializerUpdateTrip(serializers.ModelSerializer):
    id = serializers.IntegerField()
    truck = serializers.CharField()
    user = serializers.CharField()
    scheduleDay = serializers.DateField()
    details = serializers.CharField()
    address = serializers.CharField()

    class Meta:
        model = Trip
        fields = "__all__"
