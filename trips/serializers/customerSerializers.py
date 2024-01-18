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


    class Meta:
        model = User
        fields = ["document", "name", "role", "numberPhone", "address"]

class CustomerWithQuantityTrips(serializers.Serializer):
    class Meta:
        model=User
        fields = ["document", "name", "isAdmin", 
                  "numberPhone", "address","quantityTrips"]
