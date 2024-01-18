# API APP-VIAJES-RECOLAM

La API permite realizar operaciones de consulta, creación, actualización y eliminación de viajes. Estos viajes están asociados a un cliente específico y se les asigna un camión. Además, se tiene en cuenta la disponibilidad de los camiones para asignarlos en la fecha programada para el viaje. Se implementa un control para evitar la creación de viajes en ciertos casos, como los domingos o cuando el tiempo límite para la creación del viaje ya ha pasado.

## Instalación

La API está construida con Python y Django Rest Framework (DRF). Asegúrate de tener instaladas las siguientes dependencias:

- Python 3.10
- asgiref 3.7.2
- Django 4.2.4
- django-cors-headers 4.2.0
- djangorestframework 3.14.0
- drf-yasg 1.21.7
- inflection 0.5.1
- packaging 23.2
- pytz 2023.3
- PyYAML 6.0.1
- sqlparse 0.4.4
- typing_extensions 4.7.1
- uritemplate 4.1.1

Para instalar el entorno virtual y las dependencias del proyecto, sigue estos pasos:

1. Clona el repositorio.
2. Crea un entorno virtual con el comando `virtualenv nameEnv` y luego actívalo. Ejecuta `pip install -r req.txt` para instalar las dependencias del proyecto.
3. Inicia la API ejecutando `python manage.py runserver` en Windows o `python3 manage.py runserver` en Linux.
4. Una vez que el servidor esté en funcionamiento, accede a la documentación de la API a través de los siguientes enlaces: [Swagger](http://127.0.0.1:8000/swagger/) o [Redoc](http://127.0.0.1:8000/redoc/).

Con estos pasos, podrás acceder a la API y a su documentación de manera sencilla.

## Uso

La API se puede utilizar para conectar aplicaciones móviles y web, así como para integrarse en proyectos más amplios.

## Documentación de la API

Puedes acceder a la documentación de la API y probar sus endpoints siguiendo los pasos anteriores. La documentación proporciona detalles sobre todos los endpoints disponibles, parámetros esperados y posibles respuestas.

## Ejemplos

Algunos endpoints disponibles en la API incluyen:

- Consultar viajes finalizados por cliente.
- Crear un nuevo viaje.
- Editar la información de un viaje existente.
- Asignar un camión a un viaje específico.

## Licencia

[Nombre de la licencia]

## Contacto

Luis Santiago Beltran
Email: lsantibz@gmail.com

