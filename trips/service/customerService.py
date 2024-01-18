from django.db import connection
from ..models import User
from ..serializers.customerSerializers import CustomerSerializer
import datetime
from django.db.models import Q

# listado clientes disponibles para tener otro viaje
def customerAvailableForCreateTripInDate(date:datetime):
    query = f'''
        SELECT * 
        FROM users
        WHERE isAdmin = 0 AND document NOT IN (
        SELECT user_id 
        FROM trips
        WHERE scheduleDay='{date}' AND isDisable = 0
        GROUP BY user_id
        HAVING count(id) > 1 AND user_id IS NOT NULL
        )
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    print(f"clientes con habiles {results}")

    if len(results) > 0:
        customers = []
        for cusDB in results:
            customers.append(User.objects.get(document=cusDB[6]))
        return customers
    return None


#validando la disponibilidad de un cliente para tener otro viaje
def validationCustomerTrip(user:[str,User],date:datetime)->User:
    if (isinstance(user,str)):
        user = User.objects.get(Q(document=user) & Q(isAdmin=False))
    if user.isDisable:
        raise Exception("the user selected is disable.") 
    userSelectedIsAvailable= filter(lambda customerAvailable: 
                                    customerAvailable.document == user.document
                                    ,customerAvailableForCreateTripInDate(date))
    if not userSelectedIsAvailable:
        raise Exception("the user selected isn't available")
    return user
