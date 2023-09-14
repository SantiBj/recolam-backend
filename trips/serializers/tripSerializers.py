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


class PartialSerializer(serializers.ModelSerializer):
    truck = serializers.CharField(required=False)
    user = serializers.CharField(required=False)
    scheduleDay = serializers.DateField(required=False)
    details = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = Trip
        fields = "__all__"
