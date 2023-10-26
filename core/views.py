from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from trips.models import Session, User, Truck
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from .serializers import UserPersonSerializer, UserTruckSerializer, AdminSerializer
import json


def login(id):
    try:
        user = User.objects.get(id=id)
    except:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)
    try:
        # si no hay token sale una exceptions
        token = Token.objects.get(user=user)
        session = Session.objects.get(user=user)
        if (session.sessions >= 3):
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)
        session.sessions = session.sessions + 1
        session.save()
    except:
        # si no hay sesion inicia con valor de 1 a nombre del usuario
        session = Session(user=user)
        session.save()

    makeToken = Token.objects.get_or_create(user=user)[0]
    return {
        "token": str(makeToken),
        "id": str(user.id),
        "user": str(user)
    }


class Login(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # al comprobar si el usuario existe validad
            user = User.objects.get(id=request.data["id"])
            return Response(login(user.id))
        except:
            return Response({"error": "credentials incorrect"}, status=status.HTTP_400_BAD_REQUEST)


class Register(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        print(data)
        if (data["role"] == "truck"):
            serializer = UserTruckSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                Truck.objects.create(placa=data["id"])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"message": "data is not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer = None
            if (data["role"] == "customer"):
                serializer = UserPersonSerializer(data=data)
            else:
                serializer = AdminSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"message": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
