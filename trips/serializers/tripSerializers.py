from rest_framework.serializers import ModelSerializer
from trips.models import Trip

class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"

class CreateCustTripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = ['user','scheduleDay','weightAvg','details']
