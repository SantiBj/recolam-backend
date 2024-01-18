from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
<<<<<<< HEAD
from .views import Register, Login, Logout
=======
from .views import Register, Login
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
<<<<<<< HEAD
    path('api/login/<str:document>', Login.as_view()),
    path('api/register', Register.as_view()),
    path('api/logout',Logout.as_view()),
=======
    path('api/login', Login.as_view()),
    path('api/register', Register.as_view()),
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
    path('api/', include("trips.urls")),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
