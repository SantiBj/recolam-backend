from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from ..serializers.tripSerializers import TripWithOldTruckAssignedSerializer, TripInfoTruckAndCustomerSerializer, TripWithCustomerSerializer, PartialSerializer, TripSerializer
from ..models import Trip, Truck, User
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from ..pagination import CustomPagination
from ..service.trips_service import validationDateAvailable, addFieldOldTruckAssigned, dateTripsWithoutInitCAndOptionalTruck, truckBusy, truckWithTripInProcess, dateOfTripsWithoutInitCompany, dateOfTripsWithoutTruck, validation_trip, quantityTripsForCustomerInDate
from rest_framework.pagination import PageNumberPagination


class DatesTripsWithoutTruck(ListAPIView):
    def list(self, request, *args, **kwargs):
        dates = dateOfTripsWithoutTruck()
        if dates != None:
            return Response({"dates": dates}, status=status.HTTP_200_OK)
        return Response({"message": "not found dates without truck"}, status=status.HTTP_400_BAD_REQUEST)

class DateForTrip(RetrieveAPIView):
    queryset = Trip.objects.all()
    lookup_field = "id"
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance :
            return Response({"date":str(instance.scheduleDay)},status=status.HTTP_200_OK)
        return Response({"message":"trip not found"},status=status.HTTP_400_BAD_REQUEST)

class DatesTripsWithoutInitialDateCompany(ListAPIView):
    def list(self, request, *args, **kwargs):
        dates = dateOfTripsWithoutInitCompany()
        if dates != None:
            return Response({"dates": dates}, status=status.HTTP_200_OK)
        return Response({"message": "not found dates without truck"}, status=status.HTTP_400_BAD_REQUEST)


class QuantityTripsForCustomerInDate(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        quantityOrError = quantityTripsForCustomerInDate(
            kwargs["id"], kwargs["date"])
        return quantityOrError


class TripsAvailableForDate(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(
                kwargs["date"], '%Y-%m-%d').date()
            response = validation_trip(date)
            return response
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TripCreateAPIView(CreateAPIView):
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


class TripUpdateAPIView(UpdateAPIView):
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


class TripDestroyAPIView(DestroyAPIView):
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


class TripRetrieveAPIView(RetrieveAPIView):
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


class AsignTimeInitialTripCompany(UpdateAPIView):
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


class AsignTimeEndTripCompany(UpdateAPIView):
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


class TripsForDateListAPIView(ListAPIView):
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


class AsignTimeArriveCustomer(UpdateAPIView):
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


class AsignTimeEndCustomer(UpdateAPIView):
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


class AddTruckToTrip(UpdateAPIView):
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


class EditTruckTrip(UpdateAPIView):
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


class TripsWithoutTruck(ListAPIView):
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


class TripsWithoutInitCustomers(ListAPIView):
    serializer_class = TripSerializer

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
                        serializer = self.get_serializer(
                            tripsWithoutArrivedComp, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response({"message": "not found trips with init for this customer"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "not found trips for this customer in date inserted"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "date must be greater than or equal to today"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# viajes activos seran del dia de hoy no anteriores


class TripsWithDateInitCompany(ListAPIView):
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


class EndTripsForCustomer(ListAPIView):
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


class TripsWithoutInit(ListAPIView):
    serializer_class = TripsWithoutInitCustomers

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


class ListDatesWithTripsWithoutStart(ListAPIView):
    def list(self, request, *args, **kwargs):
        dates = dateTripsWithoutInitCAndOptionalTruck()
        if dates != None:
            return Response(dates, status=status.HTTP_200_OK)
        return Response({"message": "not found trips without start"}, status=status.HTTP_400_BAD_REQUEST)

# viajes sin iniciar con camion asignado opcionalmente


class TripsWithoutInitForDate(ListAPIView):
    serializer_class = TripSerializer

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
                    serializerInstances = self.get_serializer(
                        tripsWithoutInitComp, many=True)
                    # añadiendo un campo para ver si el viaje puede iniciar
                    tripsNewField = truckWithTripInProcess(
                        serializerInstances.data)
                    paginator = PageNumberPagination()
                    paginator.page_size = 1
                    results = paginator.paginate_queryset(
                        tripsNewField, request)
                    serializer = TripInfoTruckAndCustomerSerializer(
                        results, many=True)

                    return paginator.get_paginated_response(serializer.data)
                return Response({"message": "not fount trip without init for this date"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "not found trips for this date"}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TripsActivesToday(ListAPIView):
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
