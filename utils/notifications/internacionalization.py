from emailTesting.models import SystemConfiguration
from django.template.loader import render_to_string

# Necessary variables
system_configuration = SystemConfiguration.objects.filter(pk=1).first()

spanish = {
    "WELCOME_SUBJECT": "Bienvenido a Grooving",
    "BAN_UNBAN_USERS_ACTIVE_SUBJECT": "¡Tu cuenta de Grooving ha sido activada de nuevo!",
    "BAN_UNBAN_USERS_ACTIVE_BODY": "<p>Hola,</p>" +
                                   "<p>Gracias por contactar con el equipo de Grooving. Hemos activado su cuenta " +
                                   "de nuevo.</p>" +
                                   "<p>Disculpe las molestias por lo ocurrido.</p>",
    "BAN_UNBAN_USERS_INACTIVE_SUBJECT": "Tu cuenta de Grooving ha sido bloqueada",
    "BAN_UNBAN_USERS_INACTIVE_BODY": "<p>Hello,</p>" +
                                     "<p>Esta cuenta ha sido temporalmente desactivada por violación de los Terminos " +
                                     "y condiciones de Grooving. Por favor, contacte con el equipo de grooving en " +
                                     system_configuration.reportEmail + "</p>",
    "FOOTER": render_to_string('footer_mail_es.html'),
}

english = {
    "WELCOME_SUBJECT": "Welcome to Grooving family",
    "BAN_UNBAN_USERS_ACTIVE_SUBJECT": "Your Grooving account has been actived again",
    "BAN_UNBAN_USERS_ACTIVE_BODY": "<p>Hello,</p>" +
                                   "<p>Thanks for contacting Grooving Support. We have activated your account " +
                                   "again.</p> <p>We apologize for the inconvenience.</p>",
    "BAN_UNBAN_USERS_INACTIVE_SUBJECT": "Your Grooving account has been banned",
    "BAN_UNBAN_USERS_INACTIVE_BODY": "<p>Hello,</p>" +
                                     "<p>This account has been temporaly banned to a violation of ours Terms & " +
                                      "conditions. Please contact to Grooving support at " +
                                      system_configuration.reportEmail + "</p>",
    "FOOTER": render_to_string('footer_mail_en.html'),
}


def translate(key_language: str, key_to_translate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return translations[key_language][key_to_translate]


spanish_document = {
    "BODY_PENDING_TO_CONTRACT_MADE": "body_pending_to_contract_made_es.html",
    "PDF_PENDING_TO_CONTRACT_MADE": "pdf_pending_to_contract_made_es.html",
    "PDF_CONTRACT_MADE_TO_PAYMENT_MADE": "pdf_contract_made_to_payment_made_es.html",
    "PDF_CONTRACT_MADE_TO_CANCELLED_ARTIST": "pdf_contract_made_to_cancelled_artist_es.html",
    "PDF_CONTRACT_MADE_TO_CANCELLED_CUSTOMER": "pdf_contract_made_to_cancelled_customer_es.html",
}

english_document = {
    "BODY_PENDING_TO_CONTRACT_MADE": "body_pending_to_contract_made_en.html",
    "PDF_PENDING_TO_CONTRACT_MADE": "pdf_pending_to_contract_made_en.html",
    "PDF_CONTRACT_MADE_TO_PAYMENT_MADE": "pdf_contract_made_to_payment_made_en.html",
    "PDF_CONTRACT_MADE_TO_CANCELLED_ARTIST": "pdf_contract_made_to_cancelled_artist_en.html",
    "PDF_CONTRACT_MADE_TO_CANCELLED_CUSTOMER": "pdf_contract_made_to_cancelled_customer_en.html",
}


def translate_render(key_language: str, document_to_translate: str, context: dict):
    translations_document = {
        "es": spanish_document,
        "en": english_document
    }

    return render_to_string(translations_document[key_language][document_to_translate], context)
