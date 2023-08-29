from rest_framework import generics
from ..models import Trip
from ..serializers.truckSerializers import TruckSerializer

#camiones con menos de 3 viajes en la fecha indicada
class truckDisponibleInDateListAPIView(generics.ListAPIView):
    serializer_class = TruckSerializer

    def list(self,request):
        trucks = 
        
        return
