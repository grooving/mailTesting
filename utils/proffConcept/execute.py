# Importamos las tareas del archivo tasks.
from utils.proffConcept.tasks import hello, sum_num
import time

print("Start at: " + time.ctime())
# Para ejecutar una función en forma de tarea lo tenemos que hacer de esta forma:
hello.delay('world')
# El parámetro de la función `hello` se pasa a través de la función`delay`

# Ejecutamos la tarea `sum_num`
sum_num.delay(3, 2)


# NOTA:
# Aunque hemos convertido la función `hello` en una tarea.
# Todavía la podemos usar como una función normal de python.
# print(hello('world'))
print("End at: " + time.ctime())
