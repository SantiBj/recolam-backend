from rest_framework import serializers
from ..models import Trip

class TripSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    address= serializers.CharField(required=False)
    details = serializers.CharField(required=False)

    class Meta:
        model = Trip
        fields = "__all__"


class PartialSerializer(serializers.ModelSerializer):
    truck = serializers.CharField(required=False)
    user = serializers.CharField(required=False)
    scheduleDay = serializers.DateField(required=False)
    weightAvg = serializers.DecimalField(max_digits=6,decimal_places=3,required=False)
    details = serializers.CharField(required=False)
    address= serializers.CharField(required=False)

    class Meta:
        model = Trip
        fields = "__all__"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          