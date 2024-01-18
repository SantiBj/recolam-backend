from rest_framework import serializers
from trips.models import User


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
