from rest_framework import serializers
from ..models import User


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "name", "role", "numberPhone", "address"]

class CustomerWithQuantityTrips(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    role = serializers.CharField()
    numberPhone = serializers.CharField()
    address = serializers.CharField()
    quantityTrips = serializers.IntegerField()