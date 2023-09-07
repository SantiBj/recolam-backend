from rest_framework.response import Response
from rest_framework import status
from datetime import datetime,time
from ..models import Trip
from django.db.models import Q

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