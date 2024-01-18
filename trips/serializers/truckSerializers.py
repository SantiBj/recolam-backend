from rest_framework import serializers
from ..models import Truck


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
<<<<<<< HEAD
        fields = "__all__"
        isDisable = serializers.BooleanField(required=False)
=======
        fields = "__all__"
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
