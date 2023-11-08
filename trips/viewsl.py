from rest_framework.generics import ListAPIView
from .serializers import TruckSerializer
from .models import Truck
from rest_framework import permissions
from core.permissions import isTruck

# Create your views here.

class TruckListAPIView(ListAPIView):
    permission_classes= [isTruck]
    serializer_class = TruckSerializer
    queryset = Truck.objects.all()

    