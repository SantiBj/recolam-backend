from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,DestroyAPIView,UpdateAPIView
from trips.serializers.tripSerializers import CreateCustTripSerializer,TripSerializer
from trips.models import Trip
from rest_framework.response import Response
from rest_framework import status 


class CustomerTripCreateAPIView(CreateAPIView):
    serializer_class = CreateCustTripSerializer

    def post(self, request):
        serializer = CreateCustTripSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"error":"Data Not Valid"},status=status.HTTP_400_BAD_REQUEST)
    
class AdminTripCreateAPIView(CreateAPIView):
    serializer_class = Trip

    def post(self,request):
        serializer = TripSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"error":"Data Not Valid"},status=status.HTTP_400_BAD_REQUEST)
    
class TripUpdateAPIView(UpdateAPIView):
    # solo se actualiza un atributo a la vez no todos 
    def patch(self,request,*args, **kwargs):
        instance = Trip.objects.get(pk=kwargs["pk"])
        dataReceived = request.data
        try:
            for key in dataReceived.keys():
                instance.key = dataReceived[key]
        except:
            return Response({"error":"Data Not Valid"},status=status.HTTP_400_BAD_REQUEST)
        instance.save()
        serializer = TripSerializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
     


        
