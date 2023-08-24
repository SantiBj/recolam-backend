from django.urls import path
from .views import TruckListAPIView

urlpatterns = [
    path("trucks",TruckListAPIView.as_view())
]
