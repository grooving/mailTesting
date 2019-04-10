from __future__ import absolute_import      # Activamos los import absolutos para evitar conflictos entre packages
import os
from django.conf import settings
from celery import Celery

# Establecer las opciones de django para la aplicación de celery. (No es necesario, pero así evitamos tener que
# pasarle siempre al programa nuestro módulo 'settings.py')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail.settings')

# Creamos la aplicación de Celery
app = Celery(broker=settings.CELERY_BROKER_URL)

# Especificamos que las variables de configuración de Celery se encuentran en el fichero 'settings.py' de Django.
# El fichero namespace es para decir que las variables de configuración de Celery en el fichero settings empiezan
# con el fichero "CELERY".
app.config_from_object('django.conf:settings')

# Este método auto-registra las tareas para el broker. Busca las tareas dentro de todos los archivos 'tasks.py' que
# haya en las apps y las envía a Redis automáticamente. De esta forma, no tenemos que añadirlo de forma manual a la
# variable CELERY_IMPORTS en 'settings.py'
# app.autodiscover_tasks(settings.INSTALLED_APPS)
app.autodiscover_tasks(settings.INSTALLED_APPS)

if __name__ == '__main__':
    app.start()
