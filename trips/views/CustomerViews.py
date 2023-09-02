from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..serializers.customerSerializers import CustomerSerializer
from ..models import User
from django.db.models import Q
from ..pagination import CustomPagination


class CustomerListAPIView(generics.ListAPIView):
    serializer_class = CustomerSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        customers = User.objects.filter(role='customer')
        if len(customers) > 0:
            page = self.paginate_queryset(customers)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response({"message": "customers not found"}, status=status.HTTP_400_BAD_REQUEST)


class CustomerForNameSearch(generics.ListAPIView):
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
