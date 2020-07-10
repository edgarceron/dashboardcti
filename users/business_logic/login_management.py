"""Function for password encoding"""
import datetime
import pytz
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from users.models import User, LoginSession

def password_encode(data):
    """Alters request data before saving a model"""
    password = data['password']
    hasher = PBKDF2PasswordHasher()
    data['password'] = hasher.encode(password, "Wake Up, Girls!")
    return data

def password_validation(submited, user):
    encoded = user.password
    hasher = PBKDF2PasswordHasher()
    login_valid = hasher.verify(submited, encoded)
    return login_valid

def generate_key(username):
    hasher = PBKDF2PasswordHasher()
    key = username + str(datetime.datetime.now())
    key = hasher.encode(key, 'key', 10)
    return key

def login(request):
    """Logs in the user if given credentials are valid"""
    username = request.data['username']
    password = request.data['password']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    if user is not None:
        encoded = user.password
        hasher = PBKDF2PasswordHasher()
        login_valid = hasher.verify(password, encoded)

        if login_valid:
            key = generate_key(username)
            life = datetime.datetime.now() + datetime.timedelta(hours=14)
            timezone = pytz.timezone("America/Bogota")
            life_aware = timezone.localize(life)
            loginsession = LoginSession(key=key, life=life_aware, user=user)
            loginsession.save()
            request.session['loginsession'] = key
            data = {
                'success': True,
                'key': key
            }
            return data

    data = {
        'success': False,
        'message':"Nombre de usuario o contraseña incorrectos"
    }
    return data

def logout(request):
    """Deletes the loginsession key to denout logout"""
    key = request.session.get('loginsession')
    login_session = LoginSession.objects.get(key=key)
    if login_session is not None:
        del request.session['loginsession']
    data = {
        'success': True
    }
    return data

def password_hide(data):
    """Removes the password from the user data"""
    del data['password']
    return data