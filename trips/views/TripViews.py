from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from ..serializers.tripSerializers import PartialSerializer, TripSerializer
from ..models import Trip, Truck, User
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from ..pagination import CustomPagination


class TripsAvailableForDate(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(
                kwargs["date"], '%Y-%m-%d').date()
            number_trips_for_day = Trip.objects.filter(
                Q(scheduleDay=date) & Q(isDisable=False)).count()
            available = True if number_trips_for_day < 1 else False
            return Response({"avaliable": bool(available)}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TripCreateAPIView(CreateAPIView):
    serializer_class = TripSerializer

    def create(self, request):
        try:
            date = datetime.strptime(
                request.data["scheduleDay"], '%Y-%m-%d').date()
            today = datetime.now().date()
            if date == today or date > today:
                number_trips_for_day = Trip.objects.filter(
                    Q(scheduleDay=request.data["scheduleDay"]) & Q(isDisable=False)).count()
                if int(number_trips_for_day) >= 20:
                    return Response({"message": "full travel capacity for this day"}, status=status.HTTP_409_CONFLICT)

                number_trips_for_truck = None
                if "truck" in request.data:
                    number_trips_for_truck = Trip.objects.filter(
                        Q(scheduleDay=request.data["scheduleDay"]) & Q(truck=request.data["truck"]) & Q(isDisable=False)).count()
                if not number_trips_for_truck is None:
                    if int(number_trips_for_truck) == 3:
                        return Response({"message": "the capacity of travels for truck is full in this day"}, status=status.HTTP_409_CONFLICT)

                serializer = TripSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(
                        user=request.data["customer"] if "customer" in request.data else request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "date must be greater than or equal to today"}, status=status.HTTP_400_BAD_REQUEST)
        except TypeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# TODO
# actualizar los que tengan el disable en false


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


class TripRetrieveAPIView(RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
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
                instance.initialDateCompany = datetime.now()
                self.perform_update(instance)
                return Response({"message": "update success"}, status=status.HTTP_200_OK)
            return Response({"message": "cannot init trip without a truck assign"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)


class AsignTimeEndTripCompany(UpdateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    lookup_field = "id"
    lookup_url_kwarg = "pk"

    def update(self, request, **kwargs):
        instance = self.get_object()
        if not instance.isDisable and instance.endDateCustomer is None:
            return Response({"error": "the customer's departure date is required first"}, status=status.HTTP_400_BAD_REQUEST)
        if not instance.isDisable:
            if not instance.endDateCustomer is None:
                instance.endDateCompany = datetime.now()
                instance.isComplete = True
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "customer trip finish date is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)

# TODO revisar


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
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
                return Response({"error": "company trip departure date is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)


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
                return Response({"error": "customer trip departure date is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)


class AddTruckToTrip(UpdateAPIView):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "pk"

    def update(self, request, *args, **kwargs):
        trip = self.get_object()
        if trip.initialDateCompany is None:
            today = datetime.now().date()
            if trip.scheduleDay == today or trip.scheduleDay > today:
                if trip.truck is None:
                    truck = Truck.objects.filter(placa=kwargs["placa"])
                    if len(truck) > 0:
                        trip.truck = truck[0]
                        trip.save()
                        serializer = self.get_serializer(trip)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response({"message": "truck not found"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "Cannot assign a truck to a trip with truck already assign"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Cannot assign a truck to a past trip"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "truck cannot be assigned to a trip that has already started"}, status=status.HTTP_400_BAD_REQUEST)


class TripsWithoutTruck(ListAPIView):
    serializer_class = TripSerializer
    pagination_class = CustomPagination

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
                    page = self.paginate_queryset(tripsWithoutTruck)
                    serializer = self.get_serializer(
                        page, many=True)
                    return self.get_paginated_response(serializer.data)
                return Response({"message": "not exists trips assign for date inserted"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "date must be greater than or equal to today"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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


class TripsWithDateInitCompany(ListAPIView):
    serializer_class = TripSerializer

    def list(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(kwargs["date"], "%Y-%m-%d").date()
            today = datetime.now().date()
            if date == today or date > today:
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
                        serializer = self.get_serializer(
                            tripsWithDateInitComp, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
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


class TripsWithoutInitForDate(ListAPIView):
    serializer_class = TripSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(kwargs["date"], "%Y-%m-%d").date()
            today = datetime.now().date()
            print(today)
            if date == today or date > today:
                trips = Trip.objects.filter(
                    Q(isDisable=False) & Q(scheduleDay=date))
                if len(trips) > 0:
                    tripsWithoutInitComp = []
                    for trip in trips:
                        if trip.initialDateCompany is None:
                            tripsWithoutInitComp.append(trip)
                    if len(tripsWithoutInitComp) > 0:
                        page = self.paginate_queryset(tripsWithoutInitComp)
                        serializer = self.get_serializer(
                            page, many=True)
                        return self.get_paginated_response(serializer.data)
                    return Response({"error": "not fount trip without init for this date"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "not found trips for this date"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "date must be greater than or equal to today"}, status=status.HTTP_400_BAD_REQUEST)
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
                page = self.paginate_queryset(tripsActives)
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response({"message": "not found trips with init for this date"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "not found trips for this date"}, status=status.HTTP_400_BAD_REQUEST)
