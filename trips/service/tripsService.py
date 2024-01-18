from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, time
from ..models import Trip, User, Truck, TripAssignedTruckDisable
from django.db.models import Q
from ..serializers.tripSerializers import TripWithCustomerSerializer
from ..serializers.customerSerializers import CustomerSerializer
from django.db import connection


def validationDateTrip(date:datetime):
    now = datetime.now()
    numberTripsDayNewTrip = Trip.objects.filter(
        Q(scheduleDay=date) & Q(isDisable=False)).count()
    
    
    if(date < now.date()):
        raise Exception("date must be greater than or equal to today")

    if (date.weekday() == 6):
        raise Exception("on the day Sunday we cannot attend you")

    dayIsSaturday = date.weekday() == 5
    dateIsAvailable = numberTripsDayNewTrip < 10  if dayIsSaturday else numberTripsDayNewTrip < 20
    
    if (not dateIsAvailable):
        raise Exception("There is no ability to assign trips on this date.") 
    
    if dayIsSaturday:
        if date == now.date() and now.time() > time(10, 0, 0):
            raise Exception("If you want to schedule a trip today you must do it before 10 in the morning")
    else:
        if date == now.date() and now.time() > time(13, 0, 0):
            raise Exception("If you want to schedule a trip today you must do it before 1 in the late")
    

def numberTripsCustomerInDate(customers:list[dict], date:datetime):
    customersWithNewField:list[dict] = []
    for customer in customers:
        quantity = quantityTripsForCustomerInDate(customer["document"], date)
        customer["quantityTrips"] = quantity["quantityTrips"]
        customersWithNewField.append(customer)
    return customersWithNewField


#tengo la sospecha de que se esta usando en otro lado
def quantityTripsForCustomerInDate(customer:str, date:datetime):
    user = User.objects.filter(document=customer)
    if len(user) > 0:
        numberTrips = Trip.objects.filter(Q(user=user[0]) & Q(
            scheduleDay=date) & Q(isDisable=False)).count()
        return {
                "quantityTrips": numberTrips, 
                "user": CustomerSerializer(user[0]).data
            }
    raise ValueError("user not exists")


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
    tripSerializer["user"] = trip.user
    truckAssigned = TripAssignedTruckDisable.objects.filter(trip=trip)
    if len(truckAssigned) > 0:
        truckAssigned = truckAssigned[0]
        tripSerializer["oldTruckAssigned"] = truckAssigned.truck.placa
    else:
        tripSerializer["oldTruckAssigned"] = None

    return tripSerializer
