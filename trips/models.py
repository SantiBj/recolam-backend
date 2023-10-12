from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class Role(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    class Meta:
        db_table = "roles"
        verbose_name = "role"
        verbose_name_plural = "roles"

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, id, role, password=None, **extra_fields):
        if not id or not role:
            raise ValueError("data invalid")
        user = self.model(
            id=id,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, id, name, role, address, numberPhone, password, **extra_fields):
        return self._create_user(id, name, role, address, numberPhone, password, **extra_fields)

    def create_superuser(self, id, name, role, address, numberPhone, password, **extra_fields):
        return self._create_user(id, name, role, address, numberPhone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=13, unique=True,
                          primary_key=True, null=False)
    name = models.CharField(max_length=100, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    numberPhone = models.CharField(max_length=10)
    objects = CustomUserManager()

    REQUIRED_FIELDS = ['role']
    USERNAME_FIELD = 'id'

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.id


class Truck(models.Model):
    placa = models.CharField(max_length=6, unique=True, primary_key=True)
    isDisable = models.BooleanField(default=False)

    class Meta:
        db_table = "trucks"
        verbose_name = "truck"
        verbose_name_plural = "trucks"

    def __str__(self):
        return self.placa


class Trip(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduleDay = models.DateField()
    address = models.CharField(max_length=50)
    initialDateCompany = models.DateTimeField(null=True)
    endDateCompany = models.DateTimeField(null=True)
    initialDateCustomer = models.DateTimeField(null=True)
    endDateCustomer = models.DateTimeField(null=True)
    details = models.CharField(max_length=300)
    isComplete = models.BooleanField(default=False)
    isDisable = models.BooleanField(default=False)

    class Meta:
        db_table = "trips"
        verbose_name = "trip"
        verbose_name_plural = "trips"

    def __str__(self):
        return str(self.user.name)


class TripAssignedTruckDisable(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)

    class Meta:
        db_table = "trips_truck_disable"

    def __str__(self) -> str:
        return self.id + " / " + self.truck.placa


class Session(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sessions = models.IntegerField(default=1)

    class Meta:
        db_table = "sessions"
        verbose_name = "session"
        verbose_name_plural = "sessions"
