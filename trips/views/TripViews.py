from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from ..serializers.tripSerializers import TripWithOldTruckAssignedSerializer, TripInfoTruckAndCustomerSerializer, TripWithCustomerSerializer, PartialSerializer, TripSerializer
from ..models import Trip, Truck, User
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from ..pagination import CustomPagination
<<<<<<< HEAD
from ..service.customerService import validationCustomerTrip
from ..service.trucksService import validationTruckTrip
from ..service.tripsService import ( addFieldOldTruckAssigned,
    dateTripsWithoutInitCAndOptionalTruck,truckBusy,
    truckWithTripInProcess, dateOfTripsWithoutInitCompany,
    dateOfTripsWithoutTruck, validationDateTrip, quantityTripsForCustomerInDate)
from rest_framework.pagination import PageNumberPagination
from ..service.decorator_swigger import custom_swagger_decorador
from django.core.exceptions import ObjectDoesNotExist
=======
from ..service.trips_service import validationDateAvailable, addFieldOldTruckAssigned, dateTripsWithoutInitCAndOptionalTruck, truckBusy, truckWithTripInProcess, dateOfTripsWithoutInitCompany, dateOfTripsWithoutTruck, validation_trip, quantityTripsForCustomerInDate
from rest_framework.pagination import PageNumberPagination
from ..service.decorator_swigger import custom_swagger_decorador
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1


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
class DatesTripsWithoutInitialDateCompany(ListAPIView):
    """
    Fechas de los viajes agendados sin iniciar
    """

    def list(self, request, *args, **kwargs):
        dates = dateOfTripsWithoutInitCompany()
        if dates != None:
            return Response({"dates": dates}, status=status.HTTP_200_OK)
        return Response({"message": "not found dates without truck"}, status=status.HTTP_400_BAD_REQUEST)


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
<<<<<<< HEAD
            return Response(validationDateTrip(date),status=status.HTTP_200_OK)
        except (Exception,ValueError) as e:
=======
            response = validation_trip(date)
            return response
        except ValueError as e:
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class TripCreateAPIView(CreateAPIView):
    """
<<<<<<< HEAD
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
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
=======
    Creacion de un viaje validando la disponiblidad del dia , del camion y del cliente
    """
    serializer_class = TripSerializer

    def create(self, request):
        try:
            date = datetime.strptime(
                request.data["scheduleDay"], '%Y-%m-%d').date()
            validationsDate = validation_trip(date)
            if validationsDate.status_code == 200:
                number_trips_for_truck = None
                if "truck" in request.data:
                    truck = Truck.objects.filter(placa=request.data["truck"])
                    if len(truck) > 0:
                        truck = truck[0]
                        if (truck.isDisable):
                            return Response({"message": "the truck selected this disable"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"message": "the truck not found"}, status=status.HTTP_400_BAD_REQUEST)
                    number_trips_for_truck = Trip.objects.filter(
                        Q(scheduleDay=request.data["scheduleDay"]) & Q(truck=request.data["truck"]) & Q(isDisable=False)).count()
                if not number_trips_for_truck is None:
                    if int(number_trips_for_truck) >= 3:
                        return Response({"message": "the capacity of travels for truck is full in this day"}, status=status.HTTP_409_CONFLICT)

                # validar si un cliente puede mas viajes en un misma fecha

                serializer = TripSerializer(data=request.data)
                if serializer.is_valid():
                    if not "user" in request.data:
                        quantityOrError = quantityTripsForCustomerInDate(
                            request.user, request.data["scheduleDay"])
                        if quantityOrError.status_code != 200:
                            return quantityOrError
                        elif quantityOrError.data["QuantityTrips"] >= 2:
                            return Response({"message": "the ability to create trips on this date with this user is complete"}, status=status.HTTP_400_BAD_REQUEST)
                        serializer.save(user=request.user)
                    else:
                        quantityOrError = quantityTripsForCustomerInDate(
                            request.data["user"], request.data["scheduleDay"])

                        if quantityOrError.status_code != 200:
                            return quantityOrError
                        elif quantityOrError.data["QuantityTrips"] >= 2:
                            return Response({"message": "the ability to create trips on this date with this user is complete"}, status=status.HTTP_400_BAD_REQUEST)
                        user = User.objects.filter(id=request.data["user"])
                        serializer.save(user=user[0])
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return validationsDate
        except TypeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1


@custom_swagger_decorador
class TripUpdateAPIView(UpdateAPIView):
<<<<<<< HEAD

    """
    Actualizacion de un viaje, se permite actualizar el viaje antes de iniciar,se 
    podra actualizar la fecha del viaje, direccion, telefono, camion y cliente.
    retorna la instancia actualizada.
    """

    #enviar todos los campos solo se usaran los que no son nulos 
    def update(self, request, *args, **kwargs):

        try:
            serializer = PartialSerializer(data=request.data)
            if not serializer.is_valid():
                raise Exception(serializer.errors)
            oldTrip = Trip.objects.get(serializer.data["id"])
            date = datetime.strptime(
                serializer.data["scheduleDay"], '%Y-%m-%d').date()
        

            if date != None and date != oldTrip.scheduleDay:
                validationDateTrip(date)
                oldTrip.scheduleDay = date

            if serializer.data["truck"] != None and serializer.data["truck"] != oldTrip.truck.placa:
                print("")
            
            
        
        except (Exception,ObjectDoesNotExist) as e:
            Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
=======
    """
    Actualizacion de un viaje, si se cambia la fecha se validara la disponibilidad, 
    retorna la instancia actualizada
    """
    queryset = Trip.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "pk"
    serializer_class = PartialSerializer

    def update(self, request, *args, **kwargs):
        serializer = PartialSerializer(data=request.data)

        if serializer.is_valid():
            instance = self.get_object()
            if not instance.isDisable:
                date = datetime.strptime(
                    serializer.data["scheduleDay"], '%Y-%m-%d').date()

                if serializer.data["scheduleDay"] != instance.scheduleDay:
                    dateIsAvailable = validationDateAvailable(date)
                    if (dateIsAvailable.status_code != 200):
                        return dateIsAvailable

                for key in list(serializer.data.keys()):
                    if not serializer.data[key] is None:
                        setattr(instance, key, serializer.data[key])
                instance.save()
                instance_serializer = self.get_serializer(instance)
                return Response(instance_serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "trip disable"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1


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
<<<<<<< HEAD
=======
            print(serializer.data)
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class AsignTimeInitialTripCompany(UpdateAPIView):
    """
    Inicio de un viaje por parte de la empresa segun el id del viaje, 
    el viaje iniciara si no se tiene previamente un inicio y si el resto
    de campos que controlan el ciclo de vida del viaje se encuentran vacios  
    """
    queryset = Trip.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.isDisable:
            if not instance.truck is None:
                if instance.initialDateCompany is None:
                    serializerTrip = TripSerializer(instance)
                    truckIsBusy = truckBusy(serializerTrip.data)

                    if not truckIsBusy:
                        instance.initialDateCompany = datetime.now()
                        self.perform_update(instance)
                        return Response({"message": "update success"}, status=status.HTTP_200_OK)
                    return Response({"message": "the truck have in process other trip"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "the trip already init"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "cannot init trip without a truck assign"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class AsignTimeEndTripCompany(UpdateAPIView):
    """
    Finalizacion de un viaje segun el id de este, 
    se tiene en cuenta que finalizara si ya existe previamente la finalizacion de este por parte del cliente
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    lookup_field = "id"
    lookup_url_kwarg = "pk"

    def update(self, request, **kwargs):
        instance = self.get_object()
        if not instance.isDisable and instance.endDateCustomer is None:
            return Response({"message": "the customer's departure date is required first"}, status=status.HTTP_400_BAD_REQUEST)
        if not instance.isDisable:
            if not instance.endDateCustomer is None:
                instance.endDateCompany = datetime.now()
                instance.isComplete = True
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "customer trip finish date is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)


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
class AsignTimeArriveCustomer(UpdateAPIView):
    """
    Asignacion del inicio del viaje por parte del cliente
    """

    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    lookup_field = "id"
    lookup_url_kwarg = "pk"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.isDisable:
            if not instance.initialDateCompany is None:
                instance.initialDateCustomer = datetime.now()
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "company trip departure date is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class AsignTimeEndCustomer(UpdateAPIView):
    """
    Finalizacion del viaje por parte del cliente
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    lookup_field = "id"
    lookup_url_kwarg = "pk"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.isDisable:
            if not instance.initialDateCustomer is None:
                instance.endDateCustomer = datetime.now()
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "customer trip departure date is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)


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
<<<<<<< HEAD
                    paginator.page_size = 1
=======
                    paginator.page_size = CustomPagination.page_size
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
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
<<<<<<< HEAD
    al cliente que esta realizando la peticion
=======
    al cliente que esta realziando la peticion
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
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
class TripsWithoutInit(ListAPIView):
    """
    Listado de viajes sin iniciar por parte de la empresa segun la fecha inidicada en los params
    """

    def list(self, request, *args, **kwargs):
        try:
            today = datetime.now().date()
            date = datetime.strptime(kwargs["date"], "%Y-%m-%d").date()
            if date < today:
                return Response({"message": "the date must be greater than or equal to today"}, status=status.HTTP_400_BAD_REQUEST)

            trips = Trip.objects.filter(
                Q(initialDateCompany=None) & Q(scheduleDay=date) & Q(isDisable=False))
            if len(trips) > 0:
                tripsWithNewField = addFieldOldTruckAssigned(trips)
                paginator = PageNumberPagination()
                paginator.page_size = CustomPagination.page_size
                results = paginator.paginate_queryset(
                    tripsWithNewField, request)
                serializer = TripWithOldTruckAssignedSerializer(
                    results, many=True)
                return paginator.get_paginated_response(serializer.data)
            return Response({"message": "not found trips"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
<<<<<<< HEAD
    serializer_class = TripSerializer
=======
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1

    def list(self, request, *args, **kwargs):
        try:
            today = datetime.now().date()
            trips = Trip.objects.filter(
                Q(isDisable=False) & Q(scheduleDay=today)).exclude(truck__isnull=True)

            if len(trips) > 0:
                tripsWithoutInitComp = []
                for trip in trips:
                    if trip.initialDateCompany is None:
                        tripsWithoutInitComp.append(trip)
                if len(tripsWithoutInitComp) > 0:
<<<<<<< HEAD
                    serializerInstances = TripSerializer(
                        tripsWithoutInitComp, many=True)
                    # añadiendo un campo para ver si el viaje puede iniciar
                    tripsNewField = truckWithTripInProcess(
                        serializerInstances.data)
                    paginator = PageNumberPagination()
                    paginator.page_size = 1
=======
                    # añadiendo un campo para ver si el viaje puede iniciar
                    tripsNewField = truckWithTripInProcess(
                        tripsWithoutInitComp)
                    paginator = PageNumberPagination()
                    paginator.page_size = CustomPagination.page_size
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
                    results = paginator.paginate_queryset(
                        tripsNewField, request)
                    serializer = TripInfoTruckAndCustomerSerializer(
                        results, many=True)

                    return paginator.get_paginated_response(serializer.data)
                return Response({"message": "not fount trip without init for this date"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "not found trips for this date"}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class TripsActivesToday(ListAPIView):
    """
    Listado de viajes activos (son viajes que tienes fecha de inicio por parte de la empresa pero no tiene fecha fin)
    """
<<<<<<< HEAD
    serializer_class = TripSerializer
=======
    serializer_class = TripWithCustomerSerializer
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
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
<<<<<<< HEAD
=======

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
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
