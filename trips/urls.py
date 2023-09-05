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
    AsignTimeEndCustomer,
    AddTruckToTrip,
    TripsWithoutTruck,
    TripsWithoutInitCustomers,
    TripsWithDateInitCompany,
    EndTripsForCustomer,
    TripsWithoutInitForDate,
    TripsActivesToday,
    TripsAvailableForDate
)
from .views.CustomerViews import CustomerListAPIView,CustomerForNameSearch
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
    path("trucks-available-date",truck_available_In_Date_ListAPIView.as_view()),
    path("add-truck-trip/<int:pk>/<str:placa>",AddTruckToTrip.as_view()),
    path("trips-without-truck/<str:date>",TripsWithoutTruck.as_view()),
    path("trips-without-init/<str:date>",TripsWithoutInitCustomers.as_view()),
    path("trips-with-init/<str:date>",TripsWithDateInitCompany.as_view()),
    path("trips-finished-customer",EndTripsForCustomer.as_view()),
    path("trips-without-init-date-all/<str:date>",TripsWithoutInitForDate.as_view()),
    path("trips-actives-today-all",TripsActivesToday.as_view()),
    path("customers",CustomerListAPIView.as_view()),
    path("customer-search/<str:search>",CustomerForNameSearch.as_view()),
    path("trip-available-date/<str:date>",TripsAvailableForDate.as_view())
]


