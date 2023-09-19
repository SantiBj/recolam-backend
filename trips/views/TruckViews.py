from rest_framework import generics
from ..models import Trip, Truck
from ..service.trips_service import truckBusy
from ..serializers.tripSerializers import TripWithCustomerSerializer
from ..serializers.truckSerializers import TruckSerializer
from ..service.trucks_service import consult
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from ..pagination import CustomPagination

# camiones con menos de 3 viajes en la fecha indicada


class truck_available_In_Date_ListAPIView(generics.ListAPIView):
    serializer_class = TruckSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(kwargs["date"], "%Y-%m-%d").date()
            trucks = consult(date)
            if len(trucks) > 0:
                page = self.paginate_queryset(trucks)
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                return Response({"message": "there are no trucks available on the date entered"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# indicar que el camion no puede ser desactivado porque tiene varios viajes pendientes
# si se desactiva se cancelar los viajes pendientes del camión
# si no se podra desactivar si tiene viajes en curso
# viaje en curso que tiene el camion


class DisableTruck(generics.UpdateAPIView):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def update(self, request, *args, **kwargs):
        instance = Truck.objects.filter(placa=kwargs["placa"])

        if len(instance) > 0:
            instance = instance[0]
            instance.isDisable = not instance.isDisable
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "not found truck"}, status=status.HTTP_400_BAD_REQUEST)


class TruckListAPIView(generics.ListAPIView):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    pagination_class = CustomPagination


class TruckIsBusy(generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        trip = Trip.objects.filter(id=kwargs["trip"])[0]
        if trip != None:
            serializer = TripWithCustomerSerializer(trip)
            truckIsBusy = truckBusy(serializer.data)
            return Response(bool(truckIsBusy), status=status.HTTP_200_OK)
        return Response({"message":"trip not found"},status=status.HTTP_400_BAD_REQUEST)