from rest_framework import serializers
from trips.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['document', 'name', 'isAdmin', 'address', 'numberPhone']
