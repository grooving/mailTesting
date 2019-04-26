from django.http import HttpResponse
from utils.notifications.notifications import Notifications
import time


def send_email_view(request):
    print("Start at: " + time.ctime())

    # Notifications.send_email_welcome(2)
    # Notifications.send_email_create_an_offer(9)
    # Notifications.send_email_pending_to_rejected(9)
    # Notifications.send_email_pending_to_withdrawn(9)
    Notifications.send_email_pending_to_contract_made(9)
    # Notifications.send_email_contract_made_to_payment_made(9)
    # Notifications.send_email_contract_made_to_cancelled_artist(1)
    # Notifications.send_email_contract_made_to_cancelled_customer(2)
    # Notifications.send_notification_for_breach_security("Hola", "Que tal")
    # Notifications.send_email_right_to_be_forgotten("utri1990@gmail.com", "en")
    # Notifications.send_email_ban_unban_users(4)
    # Notifications.send_email_download_all_personal_data(2)

    print("End at: " + time.ctime())

    return HttpResponse("Correo enviado")
