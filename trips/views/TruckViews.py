'''
from rest_framework import generics
from ..models import Trip
from ..serializers.truckSerializers import TruckSerializer
from ..service.trucks_service import consult
from rest_framework.response import Response
from rest_framework import status

# camiones con menos de 3 viajes en la fecha indicada


class truck_available_In_Date_ListAPIView(generics.ListAPIView):
    serializer_class = TruckSerializer

    def list(self, request):
        dataForSearch = request.query_params["date"]
        trucks = consult(dataForSearch)
        if len(trucks) > 0:
            serializer = self.get_serializer(trucks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "there are no trucks available on the date entered"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
'''