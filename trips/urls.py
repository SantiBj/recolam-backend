from django.urls import path
from .views.TripViews import (
    TripRetrieveAPIView,
    TripDestroyAPIView,
    TripCancelAPIView,
    TripUpdateAPIView,
    TripCreateAPIView,
    ControllerStageOfTrip,
    TripsForDateListAPIView,
    AddTruckToTrip,
    TripsWithoutTruck,
    TripsWithDateInitCompany,
    EndTripsForCustomer,
    TripsWithoutInitForDate,
    TripsActivesToday,
    TripsAvailableForDate,
    QuantityTripsForCustomerInDate,
    DatesTripsWithoutTruck,
    DatesTrips
)
from .views.CustomerViews import Customer, CustomerListAPIView, CustomerForNameSearch
from .views.TruckViews import TruckIsAvailable, TruckIsBusy, DisableTruck, TruckListAPIView, truck_available_In_Date_ListAPIView,CreateTruck

urlpatterns = [
    path("trip-create", TripCreateAPIView.as_view()),
    path("trip-update/<int:pk>", TripUpdateAPIView.as_view()),
    path("trip/<int:pk>", TripRetrieveAPIView.as_view()),
    path("trip/set-stage-trip/<int:id>",ControllerStageOfTrip.as_view()),
    path("trips-without-date/<str:date>", TripsWithoutInitForDate.as_view()),
    path("dates-trips",DatesTrips.as_view()),
    path("trip-delete/<int:pk>", TripDestroyAPIView.as_view()),
    path("trip-cancel/<int:pk>", TripCancelAPIView.as_view()),


    path("trips-for-date/<str:date>", TripsForDateListAPIView.as_view()),
    path("trucks-available-date/<str:date>",
         truck_available_In_Date_ListAPIView.as_view()),
    path("add-truck-trip/<int:pk>/<str:placa>", AddTruckToTrip.as_view()),
    path("trips-without-truck/<str:date>", TripsWithoutTruck.as_view()),
    #path("trips-without-init/<str:date>", TripsWithoutInitCustomers.as_view()),
    path("trips-with-init/<str:date>", TripsWithDateInitCompany.as_view()),
    path("trips-finished-customer", EndTripsForCustomer.as_view()),
    path("trips-actives-today-all", TripsActivesToday.as_view()),
    path("customers/<str:date>", CustomerListAPIView.as_view()),
    path("customer-search/<str:search>", CustomerForNameSearch.as_view()),
    path("trip-available-date/<str:date>", TripsAvailableForDate.as_view()),
    path("customer/<str:document>", Customer.as_view()),
    path("quantity-trips-user-date/<str:id>/<str:date>",
         QuantityTripsForCustomerInDate.as_view()),
    path("dates-trip-without-truck", DatesTripsWithoutTruck.as_view()),
    path("trucks", TruckListAPIView.as_view()),
    path("disable-truck/<str:placa>", DisableTruck.as_view()),
    path("truck-is-busy/<str:trip>", TruckIsBusy.as_view())
]
