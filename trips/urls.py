from django.urls import path
from .views.TripViews import TripRetrieveAPIView,TripDestroyAPIView,TripUpdateAPIView,TripCreateAPIView

urlpatterns = [
    path("trip-create",TripCreateAPIView.as_view()),
    path("trip-update/<int:pk>",TripUpdateAPIView.as_view()),
    path("trip-delete/<int:pk>",TripDestroyAPIView.as_view()),
    path("trip/<int:pk>",TripRetrieveAPIView.as_view())
]


