from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import HttpResponse
from emailTesting.models import Offer, SystemConfiguration
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


def generate_pdf_payment_made():

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
                {'#': '4', 'name': 'Raquel Hernández', 'b1': '5.0', 'b2': '4.7', 'b3': '4.4', 'total': '4.7'} ,
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


def generate_pdf_pending_to_contract_made(offerId):

    offer = Offer.objects.get(pk=offerId)

    # pdf = report_template('Contract', [table, high])
    pdf = generate_pdf_payment_made()

    return pdf


def send_email_pending_to_reject(offerId):

    offer = Offer.objects.get(pk=offerId)

    email = EmailMessage()
    email.subject = 'Offer rejected'
    email.from_email = 'Grooving <no-reply@grupogrooving.com>'

    email.to = [offer.paymentPackage.portfolio.artist.user.email]
    email.body = 'You have rejected the offer received by ' + offer.eventLocation.customer.user.get_full_name()
    email.send()

    email.to = [offer.eventLocation.customer.user.email]
    email.body = 'The offer sent to ' + offer.paymentPackage.portfolio.artist.user.get_full_name() + ' has been rejected'
    email.send()


def send_email_pending_to_withdrawn(offerId):

    offer = Offer.objects.get(pk=offerId)

    email = EmailMessage()
    email.subject = 'Offer withdrawn'
    email.from_email = 'Grooving <no-reply@grupogrooving.com>'

    email.to = [offer.paymentPackage.portfolio.artist.user.email]
    email.body = 'The customer ' + offer.eventLocation.customer.user.get_full_name() + ' has withdrawn the offer'
    email.send()

    email.to = [offer.eventLocation.customer.user.email]
    email.body = 'You have withdrawn the offer sent to ' + offer.paymentPackage.portfolio.artisticName
    email.send()


def send_email_pending_to_contract_made(offerId):

    offer = Offer.objects.get(pk=offerId)
    system_configuration = SystemConfiguration.objects.filter(pk=1).first()
    pdf = generate_pdf_pending_to_contract_made(offerId)

    email = EmailMessage()
    email.subject = 'Offer accepted'
    email.from_email = 'Grooving <no-reply@grupogrooving.com>'
    email.attach('bill.pdf', pdf, 'application/pdf')
    email.content_subtype = 'html'

    # Artist mail

    email.to = [offer.paymentPackage.portfolio.artist.user.email]
    body = '<h1 style="color: #FFFFF; font-family: Helvetica"> Congratulations! ' \
           'You have been hired by ' + offer.eventLocation.customer.user.get_full_name() + '</h1>' \
           '</br> ' \
           '<h2 style="color: #FFFFF; font-family: Helvetica">Event information: </h2>'\
           '<table>'

    if offer.eventLocation.name is not None:
        body += '<tr><td><b>Name event</b>:</td><td>' + offer.eventLocation.name + '</td>'
    if offer.eventLocation.address is not None:
        body += '<tr><td><b>Address</b>:</td><td>' + offer.eventLocation.address + '</td>'
    if offer.eventLocation.description is not None:
        body += '<tr><td><b>Description</b>:</td><td>' + offer.eventLocation.description + '</td>'

    if offer.paymentPackage.performance is not None:
        body += '<tr><td><b>Package selected</b>:</td><td>Performance</td>'
        body += '<tr><td><b>Information</b>:</td><td>' + offer.paymentPackage.performance.info + '</td>'
    elif offer.paymentPackage.performance is not None:
        body += '<tr><td><b>Package selected</b>:</td><td>Fare</td>'
    else:
        body += '<tr><td><b>Package selected</b>:</td><td>Custom</td>'

    body += '<tr><td><b>Date</b>:</td><td>' + offer.date.strftime('%Y-%m-%d') + '</td>'
    body += '<tr><td><b>Duration</b>:</td><td>' + str(offer.hours) + ' hour/s</td>'
    body += '<tr><td><b>Price</b>:</td><td>' + str(offer.price) + ' ' + str(offer.currency) + '</td>'

    if offer.eventLocation.equipment is not None:
        body += '<tr><td><b>Equipment</b>:</td><td>' + offer.eventLocation.equipment
    else:
        body += '<tr><td><b>Equipment</b>:</td><td> It is not necessary</td>'

    body += '</table>'

    body += '<h2 style="color: #FFFFF; font-family: Helvetica">Terms & conditions: </h2>'
    body += '<p>' + system_configuration.termsText + '</p>'

    email.body = body
    email.send()            # Sending email

    # Customer mail

    email.to = [offer.eventLocation.customer.user.email]
    body = '<h1 style="text-align: center; color: #FFFFF; font-family: Helvetica"> Done! You have hired ' + \
           offer.paymentPackage.portfolio.artisticName + '!</h1>'
    body += '<h2 style="color: #FFFFF; font-family: Helvetica">Terms & conditions: </h2>'
    body += '<p>' + system_configuration.termsText + '</p>'
    email.body = body

    email.send()            # Sending email


def send_email_view(request):

    # Form 2 (Final): calling each variable & adding a PDF file

    send_email_pending_to_contract_made(1)

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