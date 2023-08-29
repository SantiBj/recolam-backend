from django.contrib import admin
from django.urls import path,include
from .views import Register,Login 

urlpatterns = [
    path('api/login',Login.as_view()),
    path('api/register',Register.as_view()),
    path('api/',include("trips.urls")),
    path('admin/', admin.site.urls),
]
