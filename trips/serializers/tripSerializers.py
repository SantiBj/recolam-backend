from rest_framework.serializers import ModelSerializer
from ..models import Trip

class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"

class CreateCustTripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = ['user','scheduleDay','weightAvg','details']

class PartialSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"
    
    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance
