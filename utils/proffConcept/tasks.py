from celery import Celery
import time

# Creamos la aplicación de Celery.
# El primer parámetro es el nombre de nuestro módulo
# El parámetro broker es la url del broker.
# En nuestro caso, la url es: redis://localhost:6379/0
app = Celery('tasks', broker='redis://localhost:6379/0')

# Creamos una tarea llamada sum_num usando el decorador @app.task
@app.task
def sum_num(x, y):
    time.sleep(5)
    return x + y

# Creamos una tarea llamada hello
@app.task
def hello(name):
    time.sleep(5)
    return 'Hello %s' % name
