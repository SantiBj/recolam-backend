from django.urls import path
from .views.TripViews import (
    TripRetrieveAPIView,
    TripDestroyAPIView,
    TripUpdateAPIView,
    TripCreateAPIView,
    AsignTimeInitialTripCompany,
    AsignTimeEndTripCompany,
    TripsForDateListAPIView,
    AsignTimeArriveCustomer,
    AsignTimeEndCustomer
)
from .views.TruckViews import truck_available_In_Date_ListAPIView

urlpatterns = [
    path("trip-create",TripCreateAPIView.as_view()),
    path("trip-update/<int:pk>",TripUpdateAPIView.as_view()),
    path("trip-delete/<int:pk>",TripDestroyAPIView.as_view()),
    path("trip/<int:pk>",TripRetrieveAPIView.as_view()),
    path("trip-init-company/<int:pk>",AsignTimeInitialTripCompany.as_view()),
    path("trip-end-company/<int:pk>",AsignTimeEndTripCompany.as_view()),
    path("trip-for-date/<str:date>",TripsForDateListAPIView.as_view()),
    path("trip-init-customer/<int:pk>",AsignTimeArriveCustomer.as_view()),
    path("trip-end-customer/<int:pk>",AsignTimeEndCustomer.as_view()),
    path("trucks-available-date",truck_available_In_Date_ListAPIView.as_view())
]


