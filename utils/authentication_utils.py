from emailTesting.models import Artist, Customer, User

from rest_framework.authtoken.models import Token


def get_logged_user(request):
    try:
        token = request._auth.key
        if token is not None:
            token_object = Token.objects.all().filter(pk=token).first()
            if token_object is not None:
                user_id = token_object.user_id
                artist = Artist.objects.filter(user_id=user_id).first()
                if artist is not None:
                    return artist
                else:
                    customer = Customer.objects.filter(user_id=user_id).first()
                    if customer is not None:
                        return customer

                    else:
                        return None
        else:
            return None
    except:
        return None


def is_user_authenticated(user, request):
    return get_logged_user(request) == user


def get_artist(request):
    try:
        token = request._auth.key
        if token is not None:
            token_object = Token.objects.all().filter(pk=token).first()
            if token_object is not None:
                user_id = token_object.user_id
                artist = Artist.objects.filter(user_id=user_id).first()
                if artist is not None:
                    return artist
                else:
                    return None
        else:
            return None
    except:
        return None


def get_customer(request):
    try:
        token = request._auth.key
        if token is not None:
            token_object = Token.objects.all().filter(pk=token).first()
            if token_object is not None:
                user_id = token_object.user_id
                customer = Customer.objects.filter(user_id=user_id).first()
                if customer is not None:
                    return customer
                else:
                    return None
        else:
            return None
    except:
        return None


def get_admin(request):
    try:
        token = request._auth.key
        if token is not None:
            token_object = Token.objects.all().filter(pk=token).first()
            if token_object is not None:

                admin = User.objects.filter(id=token_object.user_id).first()

                if admin is not None and admin.is_staff:
                    return admin
                else:
                    return None
        else:
            return None
    except:
        return None

# Deprecated functions


def get_user_type(artist_or_customer):

    if artist_or_customer:
        artist = Artist.objects.filter(user_id=artist_or_customer.user_id).first()
        if artist is not None:
            return "Artist"
        else:
            customer = Customer.objects.filter(user_id=artist_or_customer.user_id).first()
            if customer is not None:
                return "Customer"
    else:
        return None

def get_language(user):

    if user:
        artist = Artist.objects.filter(user_id=user.id).first()
        if artist is not None:
            return artist.language
        else:
            customer = Customer.objects.filter(user_id=user.id).first()
            if customer is not None:
                return customer.language
    else:
        return None


def get_artist_or_customer_by_user(user):

    if user:
        artist = Artist.objects.filter(user_id=user.id).first()

        if artist is not None:
            return artist
        else:
            customer = Customer.objects.filter(user_id=user.id).first()

            if customer is not None:
                return customer

    return None
