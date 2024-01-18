from rest_framework import serializers
from ..models import User


class CustomerSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    class Meta:
        model = User
        fields = ["document", "name", "isAdmin", "numberPhone", "address"]

class CustomerWithQuantityTrips(serializers.Serializer):
    document = serializers.CharField()
    name = serializers.CharField()
    isAdmin = serializers.BooleanField()
=======

    class Meta:
        model = User
        fields = ["id", "name", "role", "numberPhone", "address"]

class CustomerWithQuantityTrips(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    role = serializers.CharField()
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
    numberPhone = serializers.CharField()
    address = serializers.CharField()
    quantityTrips = serializers.IntegerField()