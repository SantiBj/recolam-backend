from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from ..serializers.tripSerializers import TripWithOldTruckAssignedSerializer, TripTruck, TripWithCustomerSerializer, SerializerUpdateTrip, TripSerializer
from ..models import Trip, Truck
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from ..pagination import CustomPagination
from ..service.customerService import validationCustomerTrip
from ..service.trucksService import validationTruckTrip
from ..service.tripsService import ( addFieldOldTruckAssigned,
    dateTripsWithoutInitCAndOptionalTruck,truckBusy,
    truckWithTripInProcess, datesOfTheTrips,
    dateOfTripsWithoutTruck, validationDateTrip, quantityTripsForCustomerInDate)
from rest_framework.pagination import PageNumberPagination
from ..service.decorator_swigger import custom_swagger_decorador
from django.core.exceptions import ObjectDoesNotExist


@custom_swagger_decorador
class DatesTripsWithoutTruck(ListAPIView):
    """
    Fechas de los viajes sin camiones asignados
    """

    def list(self, request, *args, **kwargs):
        dates = dateOfTripsWithoutTruck()
        if dates != None:
            return Response({"dates": dates}, status=status.HTTP_200_OK)
        return Response({"message": "not found dates without truck"}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class DateForTrip(RetrieveAPIView):
    """
    Fecha de un viaje segun su id
    """
    queryset = Trip.objects.all()
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            return Response({"date": str(instance.scheduleDay)}, status=status.HTTP_200_OK)
        return Response({"message": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class DatesTrips(ListAPIView):
    """
    Fechas de los viajes agendados sin iniciar
    """
    permission_classes=[]

    def list(self, request, *args, **kwargs):
        return Response({"dates": datesOfTheTrips()}, status=status.HTTP_200_OK)
       


@custom_swagger_decorador
class QuantityTripsForCustomerInDate(RetrieveAPIView):
    """
    Numero de viajes que tiene un cliente asignados en una fecha especifica
    """

    def retrieve(self, request, *args, **kwargs):
        quantityOrError = quantityTripsForCustomerInDate(
            kwargs["id"], kwargs["date"])
        return quantityOrError


@custom_swagger_decorador
class TripsAvailableForDate(RetrieveAPIView):
    """
    Validacion de la disponiblidad de un viaje en una fecha especifica teniendo 
    en cuenta la cantidad de viajes que se pueden realizar en el dia, segun si es de lunes a viernes o un sabado, 
    tambien si el viaje se quiere realizar el mismo dia se podra agendar hasta cierta hora del dia
    """

    def retrieve(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(
                kwargs["date"], '%Y-%m-%d').date()
            validationDateTrip(date)
            return Response(status=status.HTTP_200_OK)
        except (Exception,ValueError) as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class TripCreateAPIView(CreateAPIView):
    """
    Creacion de un viaje validando la disponibilidad del dia , del camion y del cliente
    """
    serializer_class = TripSerializer
    
    def create(self, request):
        try:
            serializer = TripSerializer(data=request.data)
            if not serializer.is_valid():
                raise Exception(serializer.errors)
            date = datetime.strptime(
                request.data["scheduleDay"], '%Y-%m-%d').date()
            validationDateTrip(date)
            if "truck" in request.data:
                validationTruckTrip(request.data["truck"],date)
            userSelected = validationCustomerTrip(request.data["user"] if "user" in request.data else request.user,date)
        
            serializer.save(user=userSelected)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except (Exception,TypeError,ObjectDoesNotExist) as e:
            print(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class TripUpdateAPIView(UpdateAPIView):

    """
    Actualizacion de un viaje, se permite actualizar el viaje antes de iniciar,se 
    podra actualizar la fecha del viaje, direccion, telefono, camion y cliente.
    retorna la instancia actualizada.
    """

    #enviar todos los campos solo se usaran los que no son nulos 
    def update(self, request, *args, **kwargs):
        #usar expresiones regulares para validar la direccion y el telefono
        try:
            serializer = SerializerUpdateTrip(data=request.data)
            if not serializer.is_valid():
                raise Exception(serializer.errors)
            oldTrip = Trip.objects.get(serializer.data["id"])
            date = datetime.strptime(
                serializer.data["scheduleDay"], '%Y-%m-%d').date()
            address = str(serializer.data["address"])
            truck = serializer.data["truck"]
            user = serializer.data["user"]

            if date != None and date != oldTrip.scheduleDay:
                validationDateTrip(date)
                oldTrip.scheduleDay = date

            if (truck != None and truck != oldTrip.truck.placa):
                validationTruckTrip(truck,date)
                oldTrip.truck = truck
            
            if (user != None and user != oldTrip.user.document):
                validationCustomerTrip(user,date)
                oldTrip.user = user
            
            if (address != None and address.upper() != oldTrip.address.upper()):
                oldTrip.address = address
        
        except (Exception,ObjectDoesNotExist) as e:
            Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
        


@custom_swagger_decorador
class TripDestroyAPIView(DestroyAPIView):
    """
    Eliminacion del viaje, no se elimina directamente, si no se desactiva
    """

    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.isDisable = True
            instance.save()
            return Response({"message": "trip destroy with success"})
        except:
            return Response({"error": "Data Not Valid"}, status=status.HTTP_400_BAD_REQUEST)

# validar que el viaje no haya iniciado


@custom_swagger_decorador
class TripRetrieveAPIView(RetrieveAPIView):
    """
    Descripcion de un viaje segun el id proporcionado por el cliente
    """
    queryset = Trip.objects.all()
    serializer_class = TripWithCustomerSerializer
    lookup_url_kwarg = 'pk'
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.isDisable:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)



class ControllerStageOfTrip(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        try:
            userAdmin = request.user.isAdmin == True
            trip = Trip.objects.get(id=kwargs["id"])

            if (trip.deleteDate != None):
                raise Exception("The trip not found")
           
            if (trip.endDateCompany != None):
                raise Exception("The trip is over.")
            
            if(trip.truck == None):
                raise Exception("the trip does not have an assigned truck")
            
            if (userAdmin):
                if (trip.initialDateCompany == None):
                    truckBusy(trip)
                    trip.initialDateCompany = datetime.now()
                else:
                    trip.initialDateCustomer = trip.initialDateCustomer if trip.initialDateCustomer != None else datetime.now()
                    trip.endDateCustomer = trip.endDateCustomer if trip.endDateCustomer != None else datetime.now()
                    trip.endDateCompany = datetime.now()
            else:
                if (trip.user.document != request.user.document):
                    raise Exception("the trip does not belong to the user")
                if (trip.initialDateCustomer == None):
                    truckBusy(trip)
                    trip.initialDateCustomer = trip.initialDateCustomer if trip.initialDateCustomer != None else datetime.now()
                else:
                    trip.endDateCustomer = trip.endDateCustomer if trip.endDateCustomer != None else datetime.now()
            
            trip.save()
            return Response(status=status.HTTP_200_OK)            
        except (Exception,ValueError,ObjectDoesNotExist) as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)




@custom_swagger_decorador
class TripsForDateListAPIView(ListAPIView):
    """
    Listado de viajes en una fecha, 
    se veran todos los viajes activos, no se tendra en cuenta si ya inicio el  viaje o no
    """
    serializer_class = TripSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(kwargs["date"], '%Y-%m-%d')
            trips = Trip.objects.filter(
                Q(isDisable=False) & Q(scheduleDay=date)
            )
            page = self.paginate_queryset(trips)
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@custom_swagger_decorador
class AddTruckToTrip(UpdateAPIView):
    """
    Asignacion de un camion a un viaje, basado en la disponiblidad 
    del camion seleccionado para a la fecha del viaje
    """
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "pk"

    def update(self, request, *args, **kwargs):
        trip = self.get_object()
        if trip.initialDateCompany is None:
            today = datetime.now().date()
            if trip.scheduleDay >= today:
                if trip.truck is None:
                    truck = Truck.objects.filter(placa=kwargs["placa"])
                    if len(truck) > 0:
                        if truck[0].isDisable:
                            return Response({"message": "The truck can't assigned because this truck is disable"}, status=status.HTTP_400_BAD_REQUEST)
                        countTripsTruck = Trip.objects.filter(
                            Q(truck=truck[0]) & Q(scheduleDay=trip.scheduleDay) & Q(isDisable=False)).count()
                        if countTripsTruck >= 3:
                            return Response({"message": "the capacity of travels for truck is full in this day"}, status=status.HTTP_409_CONFLICT)
                        trip.truck = truck[0]
                        trip.save()
                        serializer = self.get_serializer(trip)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response({"message": "truck not found"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "Cannot assign a truck to a trip with truck already assign"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Cannot assign a truck to a past trip"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "truck cannot be assigned to a trip that has already started"}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class EditTruckTrip(UpdateAPIView):
    """
    Actualizacion del camion previamente seleccionado, teniendo en cuenta si el camion distinto
    al primero y si este nuevo camion esta disponible para la fecha del viaje
    """

    def update(self, request, *args, **kwargs):
        trip = Trip.objects.filter(id=kwargs["trip"])
        if len(trip) > 0:
            trip = trip[0]
            newTruck = Truck.objects.filter(placa=kwargs["truck"])
            if len(newTruck) > 0:
                newTruck = newTruck[0]
                if not newTruck.isDisable:
                    if newTruck.placa != trip.truck.placa:
                        countTripsTruck = Trip.objects.filter(
                            Q(truck=newTruck) & Q(scheduleDay=trip.scheduleDay) & Q(isDisable=False)).count()
                        if countTripsTruck >= 3:
                            return Response({"message": "the capacity of travels for truck is full in this day"}, status=status.HTTP_400_BAD_REQUEST)
                        trip.truck = newTruck
                        trip.save()
                        return Response({"message": "success update"}, status=status.HTTP_200_OK)
                    return Response({"message": "the same truck cannot be reassigned"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "The truck can't assigned because this truck is disable"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Truck not found"})
        return Response({"message": ""}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class TripsWithoutTruck(ListAPIView):
    """
    Lista de viajes sin camion asigando en una fecha
    """
    serializer_class = TripWithCustomerSerializer

    def list(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(kwargs["date"], '%Y-%m-%d').date()
            today = datetime.now().date()
            if date == today or date > today:
                trips = Trip.objects.filter(
                    Q(scheduleDay=date) & Q(isDisable=False))
                tripsWithoutTruck = []
                for trip in trips:
                    if trip.truck is None:
                        tripsWithoutTruck.append(trip)
                if len(tripsWithoutTruck) > 0:
                    ###
                    tripsWithNewField = addFieldOldTruckAssigned(
                        tripsWithoutTruck)
                    paginator = PageNumberPagination()
                    paginator.page_size = 1
                    results = paginator.paginate_queryset(
                        tripsWithNewField, request)
                    serializer = TripWithOldTruckAssignedSerializer(
                        results, many=True)
                    return paginator.get_paginated_response(serializer.data)
                    ###
                return Response({"message": "not exists trips assign for date inserted"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "date must be greater than or equal to today"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class TripsWithoutInitCustomers(ListAPIView):
    """
    Viajes sin iniciar por parte del cliente que esta realizando la consulta
    """

    def list(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(kwargs["date"], '%Y-%m-%d').date()
            today = datetime.now().date()
            if date == today or date > today:
                trips = Trip.objects.filter(Q(user=request.user) & Q(
                    isDisable=False) & Q(scheduleDay=date))
                if len(trips) > 0:
                    tripsWithoutArrivedComp = []
                    for trip in trips:
                        if trip.initialDateCompany is None:
                            tripsWithoutArrivedComp.append(trip)
                    if len(tripsWithoutArrivedComp) > 0:
                        serializer = TripSerializer(
                            tripsWithoutArrivedComp, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response({"message": "not found trips with init for this customer"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "not found trips for this customer in date inserted"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "date must be greater than or equal to today"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class TripsWithDateInitCompany(ListAPIView):
    """
    Listado de viajes marcados como iniciados por parte de la empresa y que pertenecen 
    al cliente que esta realizando la peticion
    """
    serializer_class = TripSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        try:
            date = datetime.now().date()
            # date = datetime.strptime(kwargs["date"], "%Y-%m-%d").date()
            today = datetime.now().date()
            if date >= today:
                trips = Trip.objects.filter(
                    Q(user=request.user) & Q(
                        isDisable=False) & Q(scheduleDay=date)
                )
                if len(trips) > 0:
                    tripsWithDateInitComp = []
                    for trip in trips:
                        if not trip.initialDateCompany is None and trip.endDateCompany is None:
                            tripsWithDateInitComp.append(trip)
                    if len(tripsWithDateInitComp) > 0:
                        page = self.paginate_queryset(tripsWithDateInitComp)
                        serializer = self.get_serializer(
                            page, many=True)
                        return self.get_paginated_response(serializer.data)
                    return Response({"message": "not found trips for this customer with trips init"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "not found trips for this customer in date inserted"})
            return Response({"message": "date must be greater than or equal to today"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class EndTripsForCustomer(ListAPIView):
    """
    Listado de viajes finalizados completamente que pertencen al usuario de la consulta
    """
    serializer_class = TripSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        trips = Trip.objects.filter(Q(user=request.user) & Q(
            isDisable=False) & Q(isComplete=True))
        if len(trips) > 0:
            page = self.paginate_queryset(trips)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response({"message": "customer not have trips finished"}, status=status.HTTP_400_BAD_REQUEST)

# viajes sin iniciar con camion asignado opcionalmente



@custom_swagger_decorador
class ListDatesWithTripsWithoutStart(ListAPIView):
    """
    Listado de fechas de viajes sin iniciar por parte de la empresa
    """

    def list(self, request, *args, **kwargs):
        dates = dateTripsWithoutInitCAndOptionalTruck()
        if dates != None:
            return Response(dates, status=status.HTTP_200_OK)
        return Response({"message": "not found trips without start"}, status=status.HTTP_400_BAD_REQUEST)

# viajes sin iniciar con camion asignado opcionalmente


@custom_swagger_decorador
class TripsWithoutInitForDate(ListAPIView):
    """
    Lista de viajes sin iniciar por parte de la empresa segun la fecha indicada
    """
    serializer_class = TripSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(kwargs["date"], "%Y-%m-%d").date()
            
            if(date < datetime.now().date()):
                raise Exception("the date must be greater than today")

            trips = Trip.objects.filter(
                Q(deleteDate=None) & Q(scheduleDay=date)
                & Q(initialDateCustomer = None))

            if len(trips) == 0: raise Exception("not found trips for this date")

            page = self.paginate_queryset(trips)
            serializerInstances = TripTruck(
                page, many=True)
            return self.get_paginated_response(serializerInstances.data)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class TripsActivesToday(ListAPIView):
    """
    Listado de viajes activos (son viajes que tienes fecha de inicio por parte de la empresa pero no tiene fecha fin)
    """
    serializer_class = TripSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        today = datetime.now().date()
        trips = Trip.objects.filter(Q(isDisable=False) & Q(scheduleDay=today))
        if len(trips) > 0:
            tripsActives = []
            for trip in trips:
                if not trip.initialDateCompany is None and trip.endDateCompany is None:
                    tripsActives.append(trip)
            if len(tripsActives) > 0:
                print(tripsActives)
                page = self.paginate_queryset(tripsActives)
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response({"message": "not found trips with init for this date"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "not found trips for this date"}, status=status.HTTP_400_BAD_REQUEST)



# TODO validar que suscedde si se pasa un id que no existe
@custom_swagger_decorador
class StateTrip(RetrieveAPIView):
    lookup_field = "id"
    queryset = Trip.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.initialDateCompany != None and instance.initialDateCustomer == None and instance.endDateCustomer == None and instance.endDateCompany == None:
            return Response({"status": "ICP"}, status=status.HTTP_200_OK)
        elif instance.initialDateCompany != None and instance.initialDateCustomer != None and instance.endDateCustomer == None and instance.endDateCompany == None:
            return Response({"status": "ICL"}, status=status.HTTP_200_OK)
        elif instance.initialDateCompany != None and instance.initialDateCustomer != None and instance.endDateCustomer != None and instance.endDateCompany == None:
            return Response({"status": "ECL"}, status=status.HTTP_200_OK)
        elif instance.initialDateCompany != None and instance.initialDateCustomer != None and instance.endDateCustomer != None and instance.endDateCompany != None:
            return Response({"status": "ECP"}, status=status.HTTP_200_OK)
