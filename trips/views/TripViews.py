from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,DestroyAPIView,UpdateAPIView
from ..serializers.tripSerializers import PartialSerializer,CreateCustTripSerializer,TripSerializer
from ..models import Trip
from rest_framework.response import Response
from rest_framework import status 


class CustomerTripCreateAPIView(CreateAPIView):
    serializer_class = CreateCustTripSerializer

    def post(self, request):
        serializer = CreateCustTripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"error":"Data Not Valid"},status=status.HTTP_400_BAD_REQUEST)
    
class AdminTripCreateAPIView(CreateAPIView):
    serializer_class = TripSerializer

    def post(self,request):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"error":"Data Not Valid"},status=status.HTTP_400_BAD_REQUEST)
    
class TripUpdateAPIView(UpdateAPIView):
    # solo se actualizan los atributos enviados, no deben ser todos 
    queryset = Trip.objects.all()
    serializer_class = PartialSerializer

class TripDestroyAPIView(DestroyAPIView):
    serializer_class = TripSerializer
    #lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = Trip.objects.get(pk=kwargs["pk"])
            instance.isDisable = True
            instance.save()
            return Response({"message":"trip destroy with success"})
        except:
            return Response({"error":"Data Not Valid"},status=status.HTTP_400_BAD_REQUEST)

class TripRetrieveAPIView(RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class=TripSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)



