from rest_framework import generics
from ..models import Trip, Truck, TripAssignedTruckDisable
from ..service.tripsService import truckBusy
from ..serializers.tripSerializers import TripWithCustomerSerializer
from ..serializers.truckSerializers import TruckSerializer
from ..service.trucksService import consult
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db.models import Q
from ..pagination import CustomPagination
from ..service.decorator_swigger import custom_swagger_decorador

# camiones con menos de 3 viajes en la fecha indicada


@custom_swagger_decorador
class truck_available_In_Date_ListAPIView(generics.ListAPIView):

    """
    Lista de camiones activos disponibles para ser asignados en una fecha especifica.
    """

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


@custom_swagger_decorador
class DisableTruck(generics.UpdateAPIView):

    """
    Activar y desactivar un camion, al desactivar un camion con viajes asignados, los viajes quedaran 
    sin camion pero deberan indicar que pertenecian al camion desactivado, y al activar el camion 
    si el viaje no ha sido reasignado se asignara de nuevo al viaje.
    """

    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def update(self, request, *args, **kwargs):
        today = datetime.now().date()
        instance = Truck.objects.filter(placa=kwargs["placa"])
        if len(instance) > 0:
            instance = instance[0]

            # viajes asignados al camion sin iniciar
            if instance.isDisable == False:
                trips = Trip.objects.filter(
                    Q(scheduleDay__gte=today) & Q(initialDateCompany=None) & Q(truck=instance))

                for trip in trips:
                    newInstance = TripAssignedTruckDisable(
                        trip=trip, truck=instance)
                    newInstance.save()
                    trip.truck = None
                    trip.save()
            else:
                tripsBeforeAssigneds = TripAssignedTruckDisable.objects.filter(
                    truck=instance)
                for tripAssigned in tripsBeforeAssigneds:
                    if tripAssigned.trip.scheduleDay >= today and tripAssigned.trip.truck == None:
                        tripAssigned.trip.truck = instance
                        tripAssigned.trip.save()
                    tripsBeforeAssigneds.delete()

            instance.isDisable = not instance.isDisable
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "not found truck"}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class TruckListAPIView(generics.ListAPIView):

    """
    Listado de camiones.
    """

    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    pagination_class = CustomPagination


@custom_swagger_decorador
class TruckIsBusy(generics.RetrieveAPIView):

    """
    Devuelve si el camion asignado a un viaje se encuentra a un 
    disponible luego de cambiar la fecha del viaje.
    """

    def retrieve(self, request, *args, **kwargs):
        trip = Trip.objects.filter(id=kwargs["trip"])[0]
        if trip != None:
            serializer = TripWithCustomerSerializer(trip)
            truckIsBusy = truckBusy(serializer.data)
            return Response(bool(truckIsBusy), status=status.HTTP_200_OK)
        return Response({"message": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)


# validando si un camion esta disponible en cierta fecha
@custom_swagger_decorador
class TruckIsAvailable(generics.RetrieveAPIView):

    """
    Validando si un camion se encuentra disponible en cierta fecha.
    """

    def retrieve(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(kwargs["date"], "%Y-%m-%d").date()
            truck = Truck.objects.filter(placa=kwargs["truck"])
            if len(truck) > 0:
                truck = truck[0]
                truckAvailableInDate = consult(date)
                if len(truckAvailableInDate) > 0:
                    available = False
                    for truckAvailable in truckAvailableInDate:
                        if (truckAvailable["placa"] == truck.placa):
                            available = True
                            break
                    return Response(bool(available), status=status.HTTP_200_OK)
                return Response({"not found trucks in this date"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "truck not found"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@custom_swagger_decorador
class CreateTruck(generics.CreateAPIView):

    """
    Crear camion.
    """

    def create(self, request, *args, **kwargs):
        serializer = TruckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        keyOfError = list(serializer.errors.keys())[0]
        return Response({"message":f"{keyOfError} = {serializer.errors[keyOfError][0]}"},status=status.HTTP_400_BAD_REQUEST) 
