from django.db import connection
from ..models import Trip
from datetime import datetime
from django.db.models import Q
from ..models import Truck

#camiones disponibles en un fecha especifica
#toca cambiarle el nombre a un nombre mas diciente
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

# validando si el camion esta disponible para agendarle un viaje
def validationTruckTrip(placa:str,date:datetime):
    truckSelected = Truck.objects.get(placa=placa)
    if (truckSelected.isDisable):
        raise Exception("the truck selected is disable.")
    truckSelectedIsAvailable = filter(lambda truckAvailable: truckAvailable["placa"] == placa,consult(date))
    if (not truckSelectedIsAvailable):
        raise Exception(f"the truck selected isn't available in this date {str(date)}")

def TruckWithTripInProcess(placa):
    today = datetime.now().date()
    trip = Trip.objects.filter(Q(truck=placa) & Q(scheduleDay=today) & Q(
        endDateCompany=None)).exclude(initialDateCompany=None)[0]
    return trip
