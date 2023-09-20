from django.db import connection
from ..models import Trip
from datetime import datetime
from django.db.models import Q


def consult(date):
    query = f'''
        SELECT *
        FROM trucks
        WHERE placa not in (
            SELECT truck_id
            FROM trips
            WHERE scheduleDay = '{date}' AND isDisable = 0
            GROUP BY truck_id 
            HAVING count(id) > 2  AND truck_id IS NOT NULL
        ) AND isDisable = 0
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

        return [
            {"placa": row[0]} for row in results
        ]


def TruckWithTripInProcess(placa):
    today = datetime.now().date()
    trip = Trip.objects.filter(Q(truck=placa) & Q(scheduleDay=today) & Q(
        endDateCompany=None)).exclude(initialDateCompany=None)[0]
    return trip
