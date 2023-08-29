from rest_framework import serializers
from ..models import Trip

class TripSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    class Meta:
        model = Trip
        fields = "__all__"


class PartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"
    
    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance
