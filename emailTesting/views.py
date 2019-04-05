from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import HttpResponse

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'gmail.settings')


# Documentation based: https://docs.djangoproject.com/en/2.2/topics/email/

def send_email_for_grooving(request):

    # Forma 1

    send_mail(subject='Asunto', message='Mensaje', from_email='grupogrooving@gmail.com',
              recipient_list=['utri1990@gmail.com'], fail_silently=False,
              auth_user='grupogrooving@gmail.com', auth_password='94TDtF4zG2t4Cxy')

    return HttpResponse("Correo enviado")


'''
# Forma 2: el servidor de correo lo detecta como SPAM

message1 = ('Asunto 1', 'Mensaje de prueba', 'grupogrooving@gmail.com', ['utri1990@gmail.com'])
message2 = ('Hola Chema', '¿Como va todo?', 'grupogrooving@gmail.com', ['joseph.jmlc@hotmail.com'])
send_mass_mail((message1, message2), fail_silently=False, auth_user='grupogrooving@gmail.com', auth_password='isppgrooving')

datatuple = (
     ('Asunto 1', 'Mensaje de prueba', 'grupogrooving@gmail.com', ['utri1990@gmail.com']),
     ('Hola Chema', '¿Como va todo?', 'grupogrooving@gmail.com', ['joseph.jmlc@hotmail.com'])
)

send_mass_mail(datatuple)

'''