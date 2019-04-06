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
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import cm


def report_template(pdf_title, content):

    # Create the PDF object, using the BytesIO object as its "file."

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Header

    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawImage('emailTesting/Banner.png', x=15, y=700, width=350, height=100)
    c.setFont('Helvetica-Bold', 20)
    c.drawString(35, 690, pdf_title)

    c.setFont('Helvetica-Bold', 12)
    c.drawString(480, 750, "06/06/2019")
    c.line(460, 747, 560, 747)

    # Pdf size

    width, height = A4
    content[0].wrapOn(c, width, height)
    content[0].drawOn(c, 30, content[1])

    # Footer (TODO)

    c.showPage()              # Save page from pdf
    c.save()                  # Save pdf

    pdf = buffer.getvalue()   # Get the value of BytesIO
    buffer.close()            # Close the buffer

    return pdf


def send_mail_payment_made():

    # Table header

    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    numero = Paragraph('''#''', styleBH)
    alumno = Paragraph('''Alumno''', styleBH)
    b1 = Paragraph('''BIM1''', styleBH)
    b2 = Paragraph('''BIM2''', styleBH)
    b3 = Paragraph('''BIM3''', styleBH)
    total = Paragraph('''Total''', styleBH)

    data = []

    data.append([numero, alumno, b1, b2, b3, total])

    # Table

    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    high = 650                              # ¿Donde vamos a escribir la tabla dependiendo de la cantidad de columnas?

    # Student data table

    students = [{'#': '1', 'name': 'Miguel Nieva',     'b1': '3.4', 'b2': '2.2', 'b3': '4.5', 'total': '3.36'},
                {'#': '2', 'name': 'Sacha Lifszyc',    'b1': '4.3', 'b2': '2.6', 'b3': '4.6', 'total': '3.83'},
                {'#': '3', 'name': 'Carlos Jimenez',   'b1': '2.1', 'b2': '4.3', 'b3': '4.9', 'total': '3.76'},
                {'#': '4', 'name': 'Raquel Hernández', 'b1': '5.0', 'b2': '4.7', 'b3': '4.4', 'total': '4.7'},
                {'#': '5', 'name': 'Elizabeth Rangel', 'b1': '3.3', 'b2': '4.9', 'b3': '4.9', 'total': '4.36'}]

    for student in students:
        this_student = [student['#'], student['name'], student['b1'], student['b2'], student['b3'], student['total']]
        data.append(this_student)
        high = high - 18                    #

    # Table size

    table = Table(data, colWidths=[1.9 * cm, 9.5 * cm, 1.9 * cm, 1.9 * cm, 1.9 * cm, 1.9 * cm])
    table.setStyle(TableStyle([          # estilos de la tabla
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

    pdf = report_template('Payment information', [table, high])

    return pdf


def send_email_for_grooving(request):

    # Form 2 (Final): calling each variable & adding a PDF file

    pdf = send_mail_payment_made()

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