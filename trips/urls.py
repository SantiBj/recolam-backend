from django.urls import path
from .views.TripViews import TripUpdateAPIView,CustomerTripCreateAPIView,AdminTripCreateAPIView
from .views import TruckListAPIView

urlpatterns = [
    path("trucks",TruckListAPIView.as_view()),
    path("trip-create-cust",CustomerTripCreateAPIView.as_view()),
    path("trip-create",AdminTripCreateAPIView.as_view()),
    path("trip-update/<int:pk>",TripUpdateAPIView.as_view()),
]


