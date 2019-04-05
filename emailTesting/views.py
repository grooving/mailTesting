from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import HttpResponse

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'gmail.settings')


# Documentation based: https://docs.djangoproject.com/en/2.2/topics/email/
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


# ======================= CLASE reportePDF =========================

def generate_report():

    # Create the HTTP Response headers with PDF

    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename =Nombre-fichero-report.pdf'

    # Create the PDF object, using the BytesIO object as its "file."

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Header

    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30, 750, 'Grooving')
    c.setFont('Helvetica', 12)
    c.drawString(30, 735, 'Report')

    c.setFont('Helvetica-Bold', 12)
    c.drawString(480, 750, "06/06/2019")
    c.line(460, 747, 560, 747)

    # Save pdf

    c.save()

    # Get the value of BytesIO buffer and write response

    pdf = buffer.getvalue()
    buffer.close()

    return pdf


# A este método deberá llegarle: idOffer,

def send_email_for_grooving(request):

    # Form 2 (Final): calling each variable & adding a PDF file

    pdf = generate_report()

    email = EmailMessage()
    email.subject = 'Payment made'
    email.body = 'This is the payment for your performance'                     # Aquí va el contenido HTML
    email.from_email = 'Grooving <no-reply@grupogrooving.com>'
    email.to = ['utri1990@gmail.com']
    # email.attach_file('emailTesting/invoice.pdf')
    email.attach('bill.pdf', pdf, 'application/pdf')
    email.send()

    return HttpResponse("Correo enviado")

'''
# Forma 1: funciona. Nota: para que funcione en producción, la contraseña debe ser segura.

send_mail(subject='Asunto', message='Mensaje', from_email='grupogrooving@gmail.com',
          recipient_list=['utri1990@gmail.com'], fail_silently=False,
          auth_user='grupogrooving@gmail.com', auth_password='94TDtF4zG2t4Cxy')

return HttpResponse("Correo enviado")
'''

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