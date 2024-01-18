<<<<<<< HEAD
import traceback
=======
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..serializers.customerSerializers import CustomerSerializer, CustomerWithQuantityTrips
<<<<<<< HEAD
from ..service.tripsService import numberTripsCustomerInDate
from ..models import User
from django.db.models import Q
from ..pagination import CustomPagination
from ..service.customerService import customerAvailableForCreateTripInDate
=======
from ..service.trips_service import quantityTripsForCustomerInDate
from ..models import User
from django.db.models import Q
from ..pagination import CustomPagination
from ..service.customer import customerAvailableForCreateTripInDate
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from ..pagination import CustomPagination
from ..service.decorator_swigger import custom_swagger_decorador
<<<<<<< HEAD
=======
# listado de clientes disponibles para un viaje en una fecha
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1


@custom_swagger_decorador
class CustomerListAPIView(generics.ListAPIView):
    """
    Listado de clientes con disponibilidad para tener otro viaje en una fecha especifica
    """

<<<<<<< HEAD
=======
    serializer_class = CustomerWithQuantityTrips

>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
    def list(self, request, *args, **kwargs):
        try:
            date = datetime.strptime(kwargs["date"], "%Y-%m-%d").date()
            customers = customerAvailableForCreateTripInDate(date)
            if (customers != None):
                serializerCust = CustomerSerializer(customers, many=True)
                customersWithQuantityTrips = numberTripsCustomerInDate(
                    serializerCust.data, date)
                paginator = PageNumberPagination()
                paginator.page_size = CustomPagination.page_size
                results = paginator.paginate_queryset(
                    customersWithQuantityTrips, request
                )
<<<<<<< HEAD
                serializer = CustomerWithQuantityTrips(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            raise ValueError("not found users availables in this date")
=======
                serializer = self.get_serializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            return Response({"message": "All customer already have assign two trips in this date"},
                            status=status.HTTP_400_BAD_REQUEST)
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


<<<<<<< HEAD

@custom_swagger_decorador
class Customer(generics.RetrieveAPIView):
=======
def numberTripsCustomerInDate(customers, date):
    customersWithNewField = []
    for customer in customers:
        quantity = quantityTripsForCustomerInDate(customer["id"], date)
        customer["quantityTrips"] = quantity.data["QuantityTrips"]
        customersWithNewField.append(customer)
    return customersWithNewField


@custom_swagger_decorador
class CustomerAddress(generics.RetrieveAPIView):
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1

    """
    Informacion de un cliente segun su id
    """

    def retrieve(self, request, *args, **kwargs):
        try:
            customer = User.objects.get(
<<<<<<< HEAD
                Q(document=kwargs["document"]) & Q(isAdmin=False))
=======
                Q(id=kwargs["id"]) & Q(role="customer"))
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
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
