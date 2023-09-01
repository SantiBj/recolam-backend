from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from ..serializers.tripSerializers import PartialSerializer, TripSerializer
from ..models import Trip
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.utils import timezone
from datetime import datetime


class TripCreateAPIView(CreateAPIView):
    serializer_class = TripSerializer

    def create(self, request):
        try:
            number_trips_for_day = Trip.objects.filter(
                Q(scheduleDay=request.data["scheduleDay"]) & Q(isDisable=False)).count()
            if int(number_trips_for_day) >= 30:
                return Response({"message": "full travel capacity for this day"}, status=status.HTTP_409_CONFLICT)

            number_trips_for_truck = None
            if request.data["truck"]:
                number_trips_for_truck = Trip.objects.filter(
                    Q(scheduleDay=request.data["scheduleDay"]) & Q(truck=request.data["truck"]) & Q(isDisable=False)).count()
            if not number_trips_for_truck is None:
                if int(number_trips_for_truck) == 3:
                    return Response({"message": "the capacity of travels for truck is full in this day"}, status=status.HTTP_409_CONFLICT)

            serializer = TripSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            instance.initialDateCompany = timezone.now()
            self.perform_update(instance)
            return Response({"message": "update success"}, status=status.HTTP_200_OK)
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
                instance.endDateCompany = timezone.now()
                instance.isComplete = True
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "customer trip finish date is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)


class TripsForDateListAPIView(ListAPIView):
    serializer_class = TripSerializer

    def list(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(kwargs["date"], '%Y-%m-%d')
            trips = Trip.objects.filter(
                Q(isDisable=False) & Q(scheduleDay=date)
            )
            serializer = self.serializer_class(trips, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
                instance.initialDateCustomer = timezone.now()
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
                instance.endDateCustomer = timezone.now()
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "customer trip departure date is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "trip not found"}, status=status.HTTP_400_BAD_REQUEST)
