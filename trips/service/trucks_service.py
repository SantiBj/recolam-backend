from django.db import connection

def consult(date):
    print(date)
    query = f'''
        SELECT *
        FROM trucks
        WHERE placa not in (
            SELECT truck_id
            FROM trips
            WHERE scheduleDay = '{date}' AND isDisable = 0
            GROUP BY truck_id 
            HAVING count(id) > 2  AND truck_id IS NOT NULL
        )
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

        return [
            {"placa":row[0]} for row in results
        ]
