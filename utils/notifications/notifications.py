from django.core.mail import EmailMessage

from emailTesting.models import Offer, SystemConfiguration, User, Actor
from weasyprint import HTML
from django.template.loader import render_to_string
from datetime import datetime
import threading
from utils.authentication_utils import get_language
from utils.notifications.internacionalization import translate, translate_render


class EmailMessageThread(threading.Thread):

    def __init__(self, from_email, to, body, subject, body_content_type, list_attachments, fail_silently=False):
        self.from_email = from_email
        self.to = to
        self.body = body
        self.subject = subject
        self.body_content_type = body_content_type
        self.fail_silently = fail_silently
        self.list_attachments = list_attachments

        threading.Thread.__init__(self)

    def run(self):
        message = EmailMessage(from_email=self.from_email, to=self.to, body=self.body, subject=self.subject)
        message.content_subtype = self.body_content_type

        message.attachments = self.list_attachments

        '''
        How it works attachments on EmailMessage?
        
        - Traditional method:
        
        if self.list_attachments:
            for attachment in self.list_attachments:
                message.attach(attachment[0], attachment[1], attachment[2])  # filename, content, mimetype
        
        - Resume method:
                
        [message.attach(attachment[0], attachment[1], attachment[2]) for attachment in self.list_attachments
        if self.list_attachments]
        
        - Fast method:
        
        message.attachments = self.list_attachment
        '''
        message.send(fail_silently=self.fail_silently)

    @staticmethod
    def send_mail(from_email, to, body, subject, body_content_type, fail_silently):
        EmailMessageThread(from_email, to, body, subject, body_content_type, None, fail_silently).start()

    @staticmethod
    def send_mail_with_attachments(from_email, to, body, subject, body_content_type, list_attachments, fail_silently):
        EmailMessageThread(from_email, to, body, subject, body_content_type, list_attachments, fail_silently).start()


class Notifications:

    @staticmethod
    def footer(languages):
        return translate(languages, 'FOOTER')

    @staticmethod
    def send_email_welcome(user_id):

        # Entity database objects

        user = User.objects.filter(pk=user_id).first()
        languages = get_language(user)

        # Email content

        from_email = "Grooving <no-reply@grupogrooving.com>"
        body_content_type = "html"
        to = [user.email]
        subject = translate(languages, "WELCOME_SUBJECT")
        body = ""

        if languages == "en":
            body = "<p>Hi there,</p>" \
                   "<p>Congratulations! You've signing with Grooving and are now part of a community that connects " \
                   "artists and improve their visibility in an easy, simple, simple and reliable way. " \
                   "From now, you'll get regular updates on the offers status made and all the information related" \
                   " to them. </p>" \
                   "<p>Your username is: <b>" + user.username + "</b></p>" \
                                                                "<p>Cheers,</p>" \
                                                                "<p>Grooving team</p>"
        elif languages == "es":
            body = "<p>¡Felicidades!,</p>" \
                   "<p>Acabas de registrarte en Grooving y ahora eres parte de una comunidad que conecta " \
                   "artistas y mejorar su visibilidad de una forma facíl, simple y confiable." \
                   "Desde este momento, recibirás actualizaciones regulares sobre las ofertas que recibas con " \
                   "información detallada.</p>" \
                   "<p>Your username is: <b>" + user.username + "</b></p>" \
                                                                "<p>Cheers,</p>" \
                                                                "<p>Grooving team</p>"
        body += Notifications.footer(languages)

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

    @staticmethod
    def send_email_create_an_offer(offer_id):

        # Entity database objects

        offer = Offer.objects.filter(pk=offer_id).first()
        language_artist = get_language(offer.paymentPackage.portfolio.artist.user)
        language_customer = get_language(offer.eventLocation.customer.user)

        # Common email content

        from_email = "Grooving <no-reply@grupogrooving.com>"
        body_content_type = "html"

        # Artist email

        to = [offer.paymentPackage.portfolio.artist.user.email]
        subject = ""
        body = ""

        if language_artist == 'en':
            subject = "You received a new offer to " + offer.eventLocation.customer.user.get_full_name()
            body = "<h1>" + offer.eventLocation.customer.user.get_full_name() + \
                   " has contacted you. </h1><p>Come on! See the details on the webpage.<p>" + \
                   Notifications.footer(language_artist)
        elif language_artist == 'es':
            subject = "Has recibido una nueva oferta de " + offer.eventLocation.customer.user.get_full_name()
            body = "<h1>" + offer.eventLocation.customer.user.get_full_name() + \
                   " ha contactado contigo. </h1><p>Puedes mirar los detalles en la página web.<p>" + \
                   Notifications.footer(language_artist)

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Customer email

        to = [offer.eventLocation.customer.user.email]
        subject = ""
        body = ""

        if language_customer == 'en':
            subject = "You has sent a offer!"
            body = "<h1>Your offer has been send to " + offer.paymentPackage.portfolio.artisticName + "</h1>" + \
                   "<p>You will receive more information soon. </p>" + Notifications.footer(language_customer)
        elif language_customer == 'es':
            subject = "¡Has enviado una oferta!"
            body = "<h1>Tu oferta ha sido enviada a " + offer.paymentPackage.portfolio.artisticName + "</h1>" + \
                   "<p>Pronto recibiras más información.</p>" + Notifications.footer(language_customer)

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

    @staticmethod
    def send_email_pending_to_rejected(offer_id):

        # Entity database objects

        offer = Offer.objects.filter(pk=offer_id).first()
        language_artist = get_language(offer.paymentPackage.portfolio.artist.user)
        language_customer = get_language(offer.eventLocation.customer.user)

        # Common email content

        from_email = "Grooving <no-reply@grupogrooving.com>"
        body_content_type = "html"

        # Artist email

        to = [offer.paymentPackage.portfolio.artist.user.email]
        subject = ""
        body = ""

        if language_artist == "en":
            subject = "The offer has been rejected successfully"
            body = "You have rejected the offer received from " + offer.eventLocation.customer.user.get_full_name() \
                   + Notifications.footer(language_artist)
        elif language_artist == "es":
            subject = "La oferta ha sido rechazada satisfactoriamente"
            body = "Has rechazado la oferta recibida por " + offer.eventLocation.customer.user.get_full_name() \
                   + Notifications.footer(language_artist)

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Customer email

        to = [offer.eventLocation.customer.user.email]
        subject = ""
        body = ""

        if language_customer == "en":
            subject = "Your offer has been rejected"
            body = "We are sorry. The offer sent to " + offer.paymentPackage.portfolio.artisticName + \
                   " has been rejected." + Notifications.footer(language_customer)
        elif language_customer == "es":
            subject = "Tu oferta ha sido rechazada"
            body = "Lo sentimos. La oferta enviada por " + offer.paymentPackage.portfolio.artisticName + \
                   " ha sido rechazada." + Notifications.footer(language_customer)

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

    @staticmethod
    def send_email_pending_to_withdrawn(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.filter(pk=offer_id).first()
        language_artist = get_language(offer.paymentPackage.portfolio.artist.user)
        language_customer = get_language(offer.eventLocation.customer.user)

        # Common email content

        from_email = "Grooving <no-reply@grupogrooving.com>"
        body_content_type = "html"

        # Artist email

        to = [offer.paymentPackage.portfolio.artist.user.email]
        subject = ""
        body = ""

        if language_artist == "en":
            subject = 'The offer has been withdrawn'
            body = '<p>We are sorry. ' + offer.eventLocation.customer.user.get_full_name() + \
                   ' has withdrawn the offer.</p>' + Notifications.footer(language_artist)
        elif language_artist == "es":
            subject = 'La oferta ha sido retirada'
            body = '<p>Lo sentimos. ' + offer.eventLocation.customer.user.get_full_name() + \
                   ' ha retirado la oferta.</p>' + Notifications.footer(language_artist)

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Customer email

        to = [offer.eventLocation.customer.user.email]
        subject = ""
        body = ""

        if language_customer == "en":
            subject = 'The offer has been withdrawn successfully.'
            body = '<p>You have withdrawn the offer sent to ' + offer.paymentPackage.portfolio.artisticName + \
                   ".</p>" + Notifications.footer(language_customer)
        elif language_customer == "es":
            subject = 'La oferta ha sido retirada satisfactoriamente.'
            body = '<p>Has retirado la oferta enviada por ' + offer.paymentPackage.portfolio.artisticName + \
                   ".</p>" + Notifications.footer(language_customer)

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

    @staticmethod
    def send_email_pending_to_contract_made(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.filter(pk=offer_id).first()
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()
        language_artist = get_language(offer.paymentPackage.portfolio.artist.user)
        language_customer = get_language(offer.eventLocation.customer.user)

        # Data to generate email body & pdf

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
            'system_configuration_profit': system_configuration.profit,
        }

        # Check package type (necessary for generate pdf & body information)

        if offer.paymentPackage.performance is not None:
            context_pdf['event_payment_package'] = 'Performance'  # Informaremos el precio total y la duración
            context_body['event_payment_package'] = 'Performance'
        elif offer.paymentPackage.fare is not None:
            context_pdf['event_payment_package'] = 'Fare'  # Informaremos del precio multiplicado por la hora
            context_pdf['event_payment_package_price_per_hour'] = offer.paymentPackage.fare.priceHour
            context_body['event_payment_package'] = 'Fare'
        else:
            context_pdf['event_payment_package'] = 'Custom'  # Informaremos del precio total y la duración
            context_body['event_payment_package'] = 'Custom'

        # Email - PDF generator

        if language_artist == 'es':
            context_pdf['system_configuration_terms_and_conditions'] = system_configuration.termsText_es
        elif language_artist == 'en':
            context_pdf['system_configuration_terms_and_conditions'] = system_configuration.termsText_en

        pdf_html_artist = translate_render(language_artist, "PDF_PENDING_TO_CONTRACT_MADE", context_pdf)

        if language_customer == 'es':
            context_pdf['system_configuration_terms_and_conditions'] = system_configuration.termsText_es
        elif language_customer == 'en':
            context_pdf['system_configuration_terms_and_conditions'] = system_configuration.termsText_en

        pdf_html_customer = translate_render(language_customer, "PDF_PENDING_TO_CONTRACT_MADE", context_pdf)

        # Email - Body generator for artist

        if language_artist == "en":
            context_body['system_configuration_terms_and_conditions'] = system_configuration.termsText_en
            context_body['title'] = 'Congratulations! You have been hired by ' + \
                                    offer.eventLocation.customer.user.get_full_name()
        elif language_artist == "es":
            context_body['system_configuration_terms_and_conditions'] = system_configuration.termsText_es
            context_body['title'] = '¡Felicidades! Has sido contratado por ' + \
                                    offer.eventLocation.customer.user.get_full_name()

        body_artist_html = translate_render(language_artist, "BODY_PENDING_TO_CONTRACT_MADE", context_body) + \
                           Notifications.footer(language_artist)

        # Email - Body generator for customer

        if language_customer == "en":
            context_body['title'] = 'Done! You have hired ' + offer.paymentPackage.portfolio.artisticName
        elif language_customer == "es":
            context_body['title'] = '¡Hecho! Has contratado a ' + offer.paymentPackage.portfolio.artisticName
        context_body['event_payment_code'] = offer.paymentCode

        if language_customer == 'es':
            context_body['system_configuration_terms_and_conditions'] = system_configuration.termsText_es
        elif language_customer == 'en':
            context_body['system_configuration_terms_and_conditions'] = system_configuration.termsText_en

        body_customer_html = translate_render(language_customer, "BODY_PENDING_TO_CONTRACT_MADE", context_body) + \
                             Notifications.footer(language_customer)

        # Common email content

        from_email = "Grooving <no-reply@grupogrooving.com>"
        body_content_type = "html"

        # Artist mail

        to = [offer.paymentPackage.portfolio.artist.user.email]
        subject = ""

        if language_artist == 'en':
            subject = "Offer accepted"
        elif language_artist == 'es':
            subject = "Oferta aceptada"

        pdf_file_artist = HTML(string=pdf_html_artist).write_pdf()  # Generating PDF
        list_attachments = [('contract.pdf', pdf_file_artist, 'application/pdf')]

        EmailMessageThread.send_mail_with_attachments(from_email, to, body_artist_html, subject, body_content_type,
                                                      list_attachments, True)

        # Customer mail

        subject = ""

        if language_customer == 'en':
            subject = "Offer accepted"
        elif language_customer == 'es':
            subject = "Oferta aceptada"

        to = [offer.eventLocation.customer.user.email]
        pdf_file_customer = HTML(string=pdf_html_customer).write_pdf()  # Generating PDF
        list_attachments = [('contract.pdf', pdf_file_customer, 'application/pdf')]
        EmailMessageThread.send_mail_with_attachments(from_email, to, body_customer_html, subject, body_content_type,
                                                      list_attachments, True)

    @staticmethod  # Todo
    def send_email_contract_made_to_payment_made(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.filter(pk=offer_id).first()
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Data to generate email body & pdf

        artist_benefit = round(offer.price - offer.price * (system_configuration.profit / 100), 2)

        context_pdf = {
            'customer_name': offer.eventLocation.customer.user.get_full_name(),
            'artist_artisticName': offer.paymentPackage.portfolio.artisticName,
            'artist_name': offer.paymentPackage.portfolio.artist.user.get_full_name(),
            'event_name': offer.eventLocation.name,
            'event_address': offer.eventLocation.address,
            'event_corporate_email': system_configuration.corporateEmail,
            'event_date_now': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'event_duration': offer.hours,
            'event_total': offer.price,
            'event_currency': offer.currency,
            'system_configuration_terms_and_conditions': system_configuration.termsText,
            'system_configuration_profit': system_configuration.profit.normalize(),
            'invoice_grooving_benefit': round(offer.price * (system_configuration.profit / 100), 2),
            'invoice_artist_benefit': artist_benefit,
        }

        # Common email content

        from_email = "Grooving <no-reply@grupogrooving.com>"
        body_content_type = "html"

        # Customer mail

        subject = offer.paymentPackage.portfolio.artisticName + " performance is over"
        to = [offer.eventLocation.customer.user.email]
        body = '<p>We hope you enjoyed to ' + offer.paymentPackage.portfolio.artisticName + ' performance.<p>' \
               + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Artist mail

        subject = 'The payment has been realized'
        to = [offer.paymentPackage.portfolio.artist.user.email]
        body = '<h1>You have received the payment in your account </h1>' \
               '<p>You can see the details on pdf attachment.<p>' + Notifications.footer()

        # Email - PDF generator to artist

        pdf_html = render_to_string("pdf_contract_made_to_payment_made_en.html", context_pdf)
        pdf_file = HTML(string=pdf_html).write_pdf()

        list_attachments = [('contract.pdf', pdf_file, 'application/pdf')]

        EmailMessageThread.send_mail_with_attachments(from_email, to, body, subject, body_content_type,
                                                      list_attachments, True)

    @staticmethod  # Todo
    def send_email_contract_made_to_cancelled_artist(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.filter(pk=offer_id).first()
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Data to generate pdf

        artist_benefit = round(offer.price - offer.price * (system_configuration.profit / 100), 2)

        context_pdf = {
            'customer_name': offer.eventLocation.customer.user.get_full_name(),
            'artist_artisticName': offer.paymentPackage.portfolio.artisticName,
            'artist_name': offer.paymentPackage.portfolio.artist.user.get_full_name(),
            'event_name': offer.eventLocation.name,
            'event_address': offer.eventLocation.address,
            'event_corporate_email': system_configuration.corporateEmail,
            'event_date_now': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'event_duration': offer.hours,
            'event_total': offer.price,
            'event_currency': offer.currency,
            'system_configuration_terms_and_conditions': system_configuration.termsText,
            'system_configuration_profit': system_configuration.profit.normalize(),
            'invoice_grooving_benefit': round(offer.price * (system_configuration.profit / 100), 2),
            'invoice_customer_benefit': artist_benefit,
        }

        pdf_html = render_to_string("pdf_contract_made_to_cancelled_artist_en.html", context_pdf)

        # Email

        from_email = 'Grooving <no-reply@grupogrooving.com>'
        body_content_type = 'html'

        # Artist mail

        subject = 'The performance has been cancelled by you'
        to = [offer.paymentPackage.portfolio.artist.user.email]
        body = '<p>We are sorry that this decision.</p><p>See you soon!<p>' + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Customer mail

        subject = offer.paymentPackage.portfolio.artisticName + 'has cancelled the performance'
        to = [offer.eventLocation.customer.user.email]
        pdf_file = HTML(string=pdf_html).write_pdf()
        body = '<p>We are sorry that the performance has been cancelled. We proceed to return the money to your' \
               ' account.</p>' + Notifications.footer()

        list_attachments = [('invoice.pdf', pdf_file, 'application/pdf')]

        EmailMessageThread.send_mail_with_attachments(from_email, to, body, subject, body_content_type,
                                                      list_attachments, True)

    @staticmethod # Todo
    def send_email_contract_made_to_cancelled_customer(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.filter(pk=offer_id).first()
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Data to generate pdf

        artist_benefit = round(offer.price - offer.price * (system_configuration.profit / 100), 2)

        context_pdf = {
            'customer_name': offer.eventLocation.customer.user.get_full_name(),
            'artist_artisticName': offer.paymentPackage.portfolio.artisticName,
            'artist_name': offer.paymentPackage.portfolio.artist.user.get_full_name(),
            'event_name': offer.eventLocation.name,
            'event_address': offer.eventLocation.address,
            'event_corporate_email': system_configuration.corporateEmail,
            'event_date_now': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'event_duration': offer.hours,
            'event_total': offer.price,
            'event_currency': offer.currency,
            'system_configuration_terms_and_conditions': system_configuration.termsText,
            'system_configuration_profit': system_configuration.profit.normalize(),
            'invoice_grooving_benefit': round(offer.price * (system_configuration.profit / 100), 2),
            'invoice_customer_benefit': artist_benefit,
        }

        pdf_html = render_to_string('pdf_contract_made_to_cancelled_customer_en.html', context_pdf)

        # Email

        from_email = 'Grooving <no-reply@grupogrooving.com>'
        body_content_type = 'html'

        # Artist mail

        subject = 'The performance has been cancelled by ' + offer.eventLocation.customer.user.get_full_name()
        to = [offer.paymentPackage.portfolio.artist.user.email]
        body = '<p>We are sorry that the performance has been cancelled.</p>' \
               '<p>See you soon!</p>' + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Customer mail

        subject = 'You cancelled the performance'
        to = [offer.eventLocation.customer.user.email]
        pdf_file = HTML(string=pdf_html).write_pdf()
        body = '<p>We are sorry that this decision. We proceed to return the money to your account.</p>' + \
               Notifications.footer()
        list_attachments = [('invoice.pdf', pdf_file, 'application/pdf')]

        EmailMessageThread.send_mail_with_attachments(from_email, to, body, subject, body_content_type,
                                                      list_attachments, True)

    @staticmethod # Todo
    def send_notification_for_breach_security(breach_explanation, body):

        # Get all system emails
        email_system_configuration_list = ['', SystemConfiguration.corporateEmail, SystemConfiguration.reportEmail]
        emails_users = User.objects.exclude(email__in=email_system_configuration_list) \
            .values_list('email', flat=True).distinct()

        for email in emails_users:
            from_email = "Grooving <no-reply@grupogrooving.com>"
            to = [email]
            body_content_type = "html"
            custom_body = '<p>We are writing to inform you about a data security issue that many involve ' \
                          'your Grooving account information. We have taken steps to secure your account ' \
                          'and are working closely with law enforcement.</p>' \
                          '<p>' + body + '</p>' + Notifications.footer()

            EmailMessageThread.send_mail(from_email, to, custom_body, breach_explanation, body_content_type, True)

    @staticmethod
    def send_email_ban_unban_users(user_id):

        # Entity database objects (necessary from template & email)

        user = User.objects.filter(pk=user_id).first()
        language = get_language(user)

        # Email

        from_email = "Grooving <no-reply@grupogrooving.com>"
        to = [user.email]
        body_content_type = "html"
        subject = ""
        body = ""

        if user.is_active:
            subject = translate(language, "BAN_UNBAN_USERS_ACTIVE_SUBJECT")
            body = translate(language, "BAN_UNBAN_USERS_ACTIVE_BODY") + Notifications.footer(language)
        else:
            subject = translate(language, "BAN_UNBAN_USERS_INACTIVE_SUBJECT")
            body = translate(language, "BAN_UNBAN_USERS_INACTIVE_BODY") + Notifications.footer(language)

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)
