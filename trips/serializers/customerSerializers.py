from rest_framework import serializers
from ..models import User


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["document", "name", "isAdmin", "numberPhone", "address"]

class CustomerWithQuantityTrips(serializers.Serializer):
    document = serializers.CharField()
    name = serializers.CharField()
    isAdmin = serializers.BooleanField()
    numberPhone = serializers.CharField()
    address = serializers.CharField()
    quantityTrips = serializers.IntegerField()