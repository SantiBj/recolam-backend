from rest_framework import serializers
from ..models import User


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["document", "name", "isAdmin", "numberPhone", "address"]

class CustomerQtyTrips(serializers.ModelSerializer):
    quantityTrips = serializers.IntegerField
    class Meta:
        model = User
        fields = ["document", "name", "numberPhone",
                "address","quantityTrips"]