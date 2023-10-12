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
    TripsAvailableForDate,
    QuantityTripsForCustomerInDate,
    DatesTripsWithoutTruck,
    DatesTripsWithoutInitialDateCompany,
    ListDatesWithTripsWithoutStart,
    TripsWithoutInit,
    EditTruckTrip,
    DateForTrip
)
from .views.CustomerViews import CustomerAddress, CustomerListAPIView, CustomerForNameSearch
from .views.TruckViews import TruckIsAvailable, TruckIsBusy, DisableTruck, TruckListAPIView, truck_available_In_Date_ListAPIView

urlpatterns = [
    path("trip-create", TripCreateAPIView.as_view()),
    path("trip-update/<int:pk>", TripUpdateAPIView.as_view()),
    path("trip-delete/<int:pk>", TripDestroyAPIView.as_view()),
    path("trip/<int:pk>", TripRetrieveAPIView.as_view()),
    path("trip-init-company/<int:pk>", AsignTimeInitialTripCompany.as_view()),
    path("trip-end-company/<int:pk>", AsignTimeEndTripCompany.as_view()),
    path("trip-for-date/<str:date>", TripsForDateListAPIView.as_view()),
    path("trip-init-customer/<int:pk>", AsignTimeArriveCustomer.as_view()),
    path("trip-end-customer/<int:pk>", AsignTimeEndCustomer.as_view()),
    path("trucks-available-date/<str:date>",
         truck_available_In_Date_ListAPIView.as_view()),
    path("add-truck-trip/<int:pk>/<str:placa>", AddTruckToTrip.as_view()),
    path("trips-without-truck/<str:date>", TripsWithoutTruck.as_view()),
    path("trips-without-init/<str:date>", TripsWithoutInitCustomers.as_view()),
    path("trips-with-init/<str:date>", TripsWithDateInitCompany.as_view()),
    path("trips-finished-customer", EndTripsForCustomer.as_view()),
    path("trips-without-initCompany-today", TripsWithoutInitForDate.as_view()),
    path("trips-actives-today-all", TripsActivesToday.as_view()),
    path("customers/<str:date>", CustomerListAPIView.as_view()),
    path("customer-search/<str:search>", CustomerForNameSearch.as_view()),
    path("trip-available-date/<str:date>", TripsAvailableForDate.as_view()),
    path("customer/<str:id>", CustomerAddress.as_view()),
    path("quantity-trips-user-date/<str:id>/<str:date>",
         QuantityTripsForCustomerInDate.as_view()),
    path("dates-trip-without-truck", DatesTripsWithoutTruck.as_view()),
    path("dates-trips-without-initialCompany",
         DatesTripsWithoutInitialDateCompany.as_view()),
    path("trucks", TruckListAPIView.as_view()),
    path("disable-truck/<str:placa>", DisableTruck.as_view()),
    path("truck-is-busy/<str:trip>", TruckIsBusy.as_view()),
    path("date-trips-without-start", ListDatesWithTripsWithoutStart.as_view()),
    path("trips-without-start/<str:date>", TripsWithoutInit.as_view()),
    path("edit-truck-trip/<str:trip>/<str:truck>", EditTruckTrip.as_view()),
    path("truck-available/<str:date>/<str:truck>", TruckIsAvailable.as_view()),
    path("date-trip/<str:id>",DateForTrip.as_view()),
]
