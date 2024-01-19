import traceback
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..serializers.customerSerializers import CustomerSerializer, CustomerQtyTrips
from ..service.tripsService import numberTripsCustomerInDate
from ..models import User
from django.db.models import Q
from ..pagination import CustomPagination
from ..service.customerService import customerAvailableForCreateTripInDate
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from ..pagination import CustomPagination
from ..service.decorator_swigger import custom_swagger_decorador


@custom_swagger_decorador
class CustomerListAPIView(generics.ListAPIView):
    """
    Listado de clientes con disponibilidad para tener otro viaje en una fecha especifica
    """
    pagination_class = CustomPagination
    serializer_class = CustomerQtyTrips
    # numberTripsCustomerInDate ---> eliminarla 

    def list(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(kwargs["date"], "%Y-%m-%d").date()
            usersPage = self.paginate_queryset(customerAvailableForCreateTripInDate(date))
            serializer = self.serializer_class(usersPage,many=True) 
            return self.get_paginated_response(serializer.data)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@custom_swagger_decorador
class Customer(generics.RetrieveAPIView):

    """
    Informacion de un cliente segun su id
    """
    def retrieve(self, request, *args, **kwargs):
        try:
            customer = User.objects.get(
                Q(document=kwargs["document"]) & Q(isAdmin=False))
            serializer = CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_400_BAD_REQUEST)


@custom_swagger_decorador
class CustomerForNameSearch(generics.ListAPIView):

    """
    Clientes cuya informacion coincida con la busquedad (nombre o id)
    """

    serializer_class = CustomerSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        customers = User.objects.filter(Q(role='customer') & (
            Q(id__icontains=kwargs["search"]) | Q(name__icontains=kwargs["search"])))
        if len(customers) > 0:
            page = self.paginate_queryset(customers)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response({"message": "not found customers with the param of search inserted"}, status=status.HTTP_400_BAD_REQUEST)
