from django.core.mail import EmailMessage
from django.http import HttpResponse
from emailTesting.models import Offer, SystemConfiguration
from weasyprint import HTML
from django.template.loader import render_to_string


def send_email_create_an_offer(offerId):
    offer = Offer.objects.get(pk=offerId)

    email = EmailMessage()
    email.from_email = 'Grooving <no-reply@grupogrooving.com>'
    email.content_subtype = 'html'

    email.to = [offer.paymentPackage.portfolio.artist.user.email]
    email.subject = "You received a new offer to " + offer.paymentPackage.portfolio.artisticName
    email.body = '<h1>' + offer.eventLocation.customer.user.get_full_name() + ' has contacted you. </h1>' \
                 '<p>Come on! See the details on the webpage.<p>'
    email.send()

    email.to = [offer.eventLocation.customer.user.email]
    email.subject = 'You has sent a offer!'
    email.body = '<h1>Your offer has been send to ' + offer.paymentPackage.portfolio.artisticName + '</h1>' + \
                 '<p>You will receive more information soon. </p>'
    email.send()


def send_email_pending_to_rejected(offerId):

    offer = Offer.objects.get(pk=offerId)

    email = EmailMessage()
    email.from_email = 'Grooving <no-reply@grupogrooving.com>'

    email.to = [offer.paymentPackage.portfolio.artist.user.email]
    email.subject = 'The offer has been rejected successfully'
    email.body = 'You have rejected the offer received from ' + offer.eventLocation.customer.user.get_full_name()
    email.send()

    email.to = [offer.eventLocation.customer.user.email]
    email.subject = 'Your offer has been rejected'
    email.body = 'We are sorry. The offer sent to ' + offer.paymentPackage.portfolio.artisticName + ' has been rejected.'
    email.send()


def send_email_pending_to_withdrawn(offerId):

    offer = Offer.objects.get(pk=offerId)

    email = EmailMessage()
    email.from_email = 'Grooving <no-reply@grupogrooving.com>'

    email.to = [offer.paymentPackage.portfolio.artist.user.email]
    email.subject = 'The offer has been withdrawn'
    email.body = 'We are sorry. ' + offer.eventLocation.customer.user.get_full_name() + ' has withdrawn the offer.'
    email.send()

    email.to = [offer.eventLocation.customer.user.email]
    email.subject = 'The offer has been withdrawn successfully.'
    email.body = 'You have withdrawn the offer sent to ' + offer.paymentPackage.portfolio.artisticName
    email.send()


def send_email_pending_to_contract_made(offerId):

    # Entity database objects (necessary from template & email)

    offer = Offer.objects.get(pk=offerId)
    system_configuration = SystemConfiguration.objects.filter(pk=1).first()

    # Template

    context_body = {
        'customer_name': offer.eventLocation.customer.user.get_full_name(),
        'event_name': offer.eventLocation.name,
        'event_address': offer.eventLocation.address,
        'event_description': offer.eventLocation.description,
        'event_date': offer.date.strftime('%Y-%m-%d'),
        'event_duration': offer.hours,
        'event_hour': offer.date.strftime('%H:%M'),
        'event_price': offer.price,
        'event_currency': offer.currency,
        'event_equipment': offer.eventLocation.equipment,
        'system_configuration_terms_and_conditions': system_configuration.termsText,
    }

    context_pdf = {
        'customer_name': offer.eventLocation.customer.user.get_full_name(),
        'artist_artisticName': offer.paymentPackage.portfolio.artisticName,
        'artist_name': offer.paymentPackage.portfolio.artist.user.get_full_name(),
        'event_name': offer.eventLocation.name,
        'event_address': offer.eventLocation.address,
        'event_description': offer.eventLocation.description,
        'event_date': offer.date.strftime('%Y-%m-%d'),
        'event_duration': offer.hours,
        'event_hour': offer.date.strftime('%H:%M'),
        'event_price': offer.price,
        'event_currency': offer.currency,
        'event_equipment': offer.eventLocation.equipment,
        'system_configuration_terms_and_conditions': system_configuration.termsText,
        'system_configuration_profit': system_configuration.profit,
    }

    # Check package type (necessary for generate pdf & email information)

    if offer.paymentPackage.performance is not None:
        context_pdf['event_payment_package'] = 'Performance'    # Informaremos el precio total y la duración
        context_body['event_payment_package'] = 'Performance'
    elif offer.paymentPackage.fare is not None:
        context_pdf['event_payment_package'] = 'Fare'           # Informaremos del precio multiplicado por la hora
        context_pdf['event_payment_package_price_per_hour'] = offer.paymentPackage.fare.priceHour
        context_body['event_payment_package'] = 'Fare'
    else:
        context_pdf['event_payment_package'] = 'Custom'         # Informaremos del precio total y la duración
        context_body['event_payment_package'] = 'Custom'

    pdf_html = render_to_string("pdf_pending_to_contract_made.html", context_pdf)

    # Email

    email = EmailMessage()
    email.subject = 'Offer accepted'
    email.from_email = 'Grooving <no-reply@grupogrooving.com>'
    email.content_subtype = 'html'
    pdf_file = HTML(string=pdf_html).write_pdf()
    email.attach('contract.pdf', pdf_file, 'application/pdf')

    # Artist mail

    context_body['title'] = 'Congratulations! You have been hired by ' + \
                            offer.eventLocation.customer.user.get_full_name()

    email.to = [offer.paymentPackage.portfolio.artist.user.email]
    email.body = render_to_string("body_pending_to_contract_made.html", context_body)
    email.send()            # Sending email

    # Customer mail

    context_body['title'] = 'Done! You have hired ' + offer.paymentPackage.portfolio.artisticName

    email.to = [offer.eventLocation.customer.user.email]
    email.body = render_to_string("body_pending_to_contract_made.html", context_body)

    email.send()            # Sending email

def send_email_contract_made_to_payment_made(offerId):

    # Entity database objects (necessary from template & email)

    offer = Offer.objects.get(pk=offerId)
    system_configuration = SystemConfiguration.objects.filter(pk=1).first()

    # Template

    # Check package type (necessary for generate pdf & email information)

    # Email

    email = EmailMessage()
    email.subject = 'Offer accepted'
    email.from_email = 'Grooving <no-reply@grupogrooving.com>'
    email.content_subtype = 'html'
    pdf_file = HTML(string=pdf_html).write_pdf()
    email.attach('contract.pdf', pdf_file, 'application/pdf')

    # Artist mail

    context_body['title'] = 'The payment has been realized to your account'

    email.to = [offer.paymentPackage.portfolio.artist.user.email]
    email.body = render_to_string("body_pending_to_contract_made.html", context_body)
    email.send()  # Sending email

    # Customer mail

    context_body['title'] = 'Done! You have hired ' + offer.paymentPackage.portfolio.artisticName

    email.to = [offer.eventLocation.customer.user.email]
    email.body = render_to_string("body_pending_to_contract_made.html", context_body)

    email.send()  # Sending email



def send_email_view(request):

    # Form 2 (Final): calling each variable & adding a PDF file

    send_email_pending_to_withdrawn(1)

    return HttpResponse("Correo enviado")
