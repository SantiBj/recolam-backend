from django.db import connection
from ..models import User
from ..serializers.customerSerializers import CustomerSerializer
import datetime
from django.db.models import Q

# listado clientes disponibles para tener otro viaje
def customerAvailableForCreateTripInDate(date:datetime):
    query = f'''
    SELECT 
        users.document,
        COUNT(trips.id)
    FROM 
        users
    LEFT JOIN 
        trips ON users.document = trips.user_id
    WHERE 
        users.isAdmin = 0 
        AND users.document NOT IN (
            SELECT 
                user_id 
            FROM 
                trips
            WHERE 
                scheduleDay = '{date}' 
                AND isDisable = 0
            GROUP BY 
                user_id
            HAVING 
                COUNT(id) > 1 AND user_id IS NOT NULL
        )
    GROUP BY 
        users.document;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    if len(results) > 0:
        customers:list[User] = []
        for cusDB in results:
            user = User.objects.get(document=cusDB[0])
            user.quantityTrips = cusDB[1]
            customers.append(user)
        return customers
    raise Exception("not found user available.")


#validando la disponibilidad de un cliente para tener otro viaje
def validationCustomerTrip(user:[str,User],date:datetime)->User:
    if (isinstance(user,str)):
        user = User.objects.get(Q(document=user) & Q(isAdmin=False))
    userSelectedIsAvailable= filter(lambda customerAvailable: 
                                    customerAvailable.document == user.document
                                    ,customerAvailableForCreateTripInDate(date))
    if not userSelectedIsAvailable:
        raise Exception("the user selected isn't available")
    return user
