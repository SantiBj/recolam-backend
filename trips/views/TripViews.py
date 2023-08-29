from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from ..serializers.tripSerializers import PartialSerializer, TripSerializer
from ..models import Trip
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


class TripCreateAPIView(CreateAPIView):
    serializer_class = TripSerializer

    def create(self, request):
        number_trips_for_day = Trip.objects.filter(
            scheduleDay=request.data["scheduleDay"]).count()
        if int(number_trips_for_day) >= 30:
            return Response({"message": "full travel capacity for this day"}, status=status.HTTP_409_CONFLICT)

        number_trips_for_truck = None
        if request.data["truck"]:
            number_trips_for_truck = Trip.objects.filter(
                Q(scheduleDay=request.data["scheduleDay"]) & Q(truck=request.data["truck"])).count()
        if not number_trips_for_truck is None:
            if int(number_trips_for_truck) == 3:
                return Response({"message":"the capacity of travels for truck is full in this day"}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripUpdateAPIView(UpdateAPIView):
    # solo se actualizan los atributos enviados, no deben ser todos
    queryset = Trip.objects.all()
    serializer_class = PartialSerializer


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
    lookup_field = 'pk'
