from rest_framework import generics
from ..models import Trip
from ..serializers.truckSerializers import TruckSerializer
from ..service.trucks_service import consult
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from ..pagination import CustomPagination

# camiones con menos de 3 viajes en la fecha indicada


class truck_available_In_Date_ListAPIView(generics.ListAPIView):
    serializer_class = TruckSerializer
    pagination_class = CustomPagination

    def list(self, request,*args, **kwargs):
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
