from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from trips.models import Session, User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from .serializers import UserSerializer
from .permissions import isAdmin


def login(document):
    try:
        user = User.objects.get(document=document)
    except:
        return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        token = Token.objects.get(user=user)
        session = Session.objects.get(user=user)
        if (session.sessions >= 3):
            return Response({"message":"user already have all sessions opened"},status=status.HTTP_400_BAD_REQUEST)
        session.sessions = session.sessions + 1
        session.save()
    except:
        session = Session(user=user)
        session.save()

    makeToken = Token.objects.get_or_create(user=user)[0]
    return Response({
        "token": str(makeToken),
        "user": {
            "document":user.document,
            "name":user.name,
            "isAdmin":user.isAdmin,
            "address":user.address,
            "numberPhone":user.numberPhone
        }
    },status=status.HTTP_200_OK)

# Con la generacion de token se tiene en cada peticion el usuario al que pertenece el token
# Internamente busca el usuario que tiene asociado el token

class Login(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]
    def post(self, request,**kwargs):
        return login(kwargs["document"])
       


class Register(generics.CreateAPIView):
    permission_classes = [isAdmin]
    
    # poner si es un admin el numberPhone y address
    def post(self, request):
        data = request.data
        if (data["isAdmin"]):
            data["numberPhone"] = None
            data["address"] = None

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({"message": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

class Logout(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        sessionUser = Session.objects.get(user=request.user)

        if sessionUser.sessions == 1:
            sessionUser.delete()
            Token.objects.get(user=request.user).delete()
        else:
            sessionUser.sessions = sessionUser.sessions - 1
            sessionUser.save()
        return Response({"message":"session of user closed with success"},status=status.HTTP_200_OK)
