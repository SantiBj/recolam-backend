from django.db import connection
from ..models import User
from ..serializers.customerSerializers import CustomerSerializer


def customerAvailableForCreateTripInDate(date):
    query = f'''
        SELECT * 
        FROM users
        WHERE role_id = 'customer' AND id NOT IN (
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

    if len(results) > 0:
        customers = []
        for cusDB in results:
            customers.append(User.objects.get(id=cusDB[3]))
        return customers
    return None
