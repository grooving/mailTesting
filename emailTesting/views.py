from django.http import HttpResponse
from utils.notifications.tasks import Notifications
import time


def send_email_view(request):

    print("Start at: " + time.ctime())

    # Notification.send_email_welcome(1)

    Notifications.send_email_pending_to_contract_made.delay(9)

    print("End at: " + time.ctime())

    return HttpResponse("Correo enviado")


