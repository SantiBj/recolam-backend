from django.urls import path
from .views.TripViews import AsignTimeInitialTripCompany,TripRetrieveAPIView,TripDestroyAPIView,TripUpdateAPIView,TripCreateAPIView
#from .views.TruckViews import truck_available_In_Date_ListAPIView

urlpatterns = [
    path("trip-init-company/<int:pk>",AsignTimeInitialTripCompany.as_view()),
    path("trip-create",TripCreateAPIView.as_view()),
    path("trip-update/<int:pk>",TripUpdateAPIView.as_view()),
    path("trip-delete/<int:pk>",TripDestroyAPIView.as_view()),
    path("trip/<int:pk>",TripRetrieveAPIView.as_view()),
    #path("trucks-available-date",truck_available_In_Date_ListAPIView.as_view())
]


