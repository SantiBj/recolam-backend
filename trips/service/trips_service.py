from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, time
from ..models import Trip, User, Truck,TripAssignedTruckDisable
from django.db.models import Q
from ..serializers.tripSerializers import TripWithCustomerSerializer
from ..serializers.customerSerializers import CustomerSerializer
from django.db import connection


def validation_trip(date):
    now = datetime.now()
    number_trips_for_day = Trip.objects.filter(
        Q(scheduleDay=date) & Q(isDisable=False)).count()
    isSatuday = date.weekday() == 5
    if (isSatuday):
        available = True if number_trips_for_day < 10 else False
    else:
        available = True if number_trips_for_day < 20 else False

    if (date >= now.date()):
        if not date.weekday() == 6:
            if (isSatuday):
                if date == now.date() and now.time() > time(10, 0, 0):
                    return Response({"message": "If you want to schedule a trip today you must do it before 10 in the morning"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if date == now.date() and now.time() > time(13, 0, 0):
                    return Response({"message": "If you want to schedule a trip today you must do it before 1 in the late"}, status=status.HTTP_400_BAD_REQUEST)
            if (available):
                return Response({"avaliable": bool(available)}, status=status.HTTP_200_OK)
            return Response({"message": "The selected date reached its maximum travel capacity"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "on the day Sunday we cannot attend you"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "date must be greater than or equal to today"}, status=status.HTTP_400_BAD_REQUEST)


def quantityTripsForCustomerInDate(customer, date):
    try:
        user = User.objects.filter(id=customer)
        if len(user) > 0:
            trips = Trip.objects.filter(Q(user=user[0]) & Q(
                scheduleDay=date) & Q(isDisable=False)).count()
            userSerializer = CustomerSerializer(user[0])
            return Response({"QuantityTrips": trips, "user": userSerializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "user not exists"}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def dateOfTripsWithoutTruck():
    today = datetime.now().date()

    query = f'''
    SELECT scheduleDay 
    FROM trips
    WHERE truck_id IS NULL AND scheduleDay >= '{today}' AND isDisable = 0
    GROUP BY scheduleDay
    ORDER BY scheduleDay ASC
    '''
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    if len(results) > 0:
        dates = [str(date[0]) for date in results]
        return dates
    return None


def dateOfTripsWithoutInitCompany():
    today = datetime.now().date()

    query = f'''
    SELECT scheduleDay
    FROM trips
    WHERE initialDateCompany IS NULL AND scheduleDay >= '{today}' AND isDisable = 0 AND truck_id IS NOT NULL
    GROUP BY scheduleDay
    ORDER BY scheduleDay ASC
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    if len(results) > 0:
        dates = [str(date[0]) for date in results]
        return dates
    return None


def dateTripsWithoutInitCAndOptionalTruck():
    today = datetime.now().date()
    query = f'''
    SELECT scheduleDay
    FROM trips
    WHERE initialDateCompany IS NULL AND scheduleDay >= '{today}' AND isDisable = 0
    GROUP BY scheduleDay
    ORDER BY scheduleDay ASC
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    if len(results) > 0:
        dates = [str(date[0]) for date in results]
        return dates
    return None


def truckWithTripInProcess(trips):
    tripsWithNewField = []

    for trip in trips:
        trip = dict(trip)

        truckIsBusy = truckBusy(trip)
        if truckIsBusy:
            trip["truckTraveling"] = True
            tripsWithNewField.append(trip)
        else:
            trip["truckTraveling"] = False
            tripsWithNewField.append(trip)

    return tripsWithNewField


def truckBusy(trip):
    truckBusy = None
    truck = Truck.objects.get(placa=trip["truck"])
    tripsTruckThisDay = Trip.objects.filter(Q(truck=truck) & Q(
        scheduleDay=trip['scheduleDay']) & Q(isDisable=False)).exclude(id=trip['id'])
    if len(tripsTruckThisDay) > 0:
        for tripTruck in tripsTruckThisDay:
            if tripTruck.initialDateCompany != None and tripTruck.endDateCompany == None:
                truckBusy = True
            else:
                if truckBusy is None:
                    truckBusy = False
    else:
        truckBusy = False
    return truckBusy


def addFieldOldTruckAssigned(trips):
    tripsWithNewField = []
    for trip in trips:
        tripsWithNewField.append(tripHadTruckAssigned(trip))
    return tripsWithNewField


def tripHadTruckAssigned(trip):
    tripSerializer = TripWithCustomerSerializer(trip)
    tripSerializer = dict(tripSerializer.data)
    truckAssigned = TripAssignedTruckDisable.objects.filter(trip=trip)
    if len(truckAssigned) > 0:
        truckAssigned = truckAssigned[0]
        tripSerializer["oldTruckAssigned"] = truckAssigned.truck.placa
    else:
        tripSerializer["oldTruckAssigned"] = None

    return tripSerializer
