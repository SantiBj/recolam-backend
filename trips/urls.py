from django.urls import path
from .views.TripViews import TripRetrieveAPIView,TripDestroyAPIView,TripUpdateAPIView,CustomerTripCreateAPIView,AdminTripCreateAPIView

urlpatterns = [
    path("trip-create-cust",CustomerTripCreateAPIView.as_view()),
    path("trip-create",AdminTripCreateAPIView.as_view()),
    path("trip-update/<int:pk>",TripUpdateAPIView.as_view()),
    path("trip-delete/<int:pk>",TripDestroyAPIView.as_view()),
    path("trip/<int:pk>",TripRetrieveAPIView.as_view())
]


