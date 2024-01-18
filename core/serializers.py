from rest_framework import serializers
from trips.models import User


<<<<<<< HEAD
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['document', 'name', 'isAdmin', 'address', 'numberPhone']
=======
class UserPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'role', 'address', 'numberPhone']


class UserTruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role']


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role', 'name']
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
