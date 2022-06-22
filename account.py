from functools import wraps

from pywebio.output import *
from pywebio.input import *
from pywebio.session import *
from pywebio.pin import *
from pywebio_battery import *
from tornado.web import create_signed_value, decode_signed_value

from werkzeug.security import generate_password_hash, check_password_hash
from peewee import DoesNotExist

from models import User

def checkConnection(username, password):
    query = User.select().where(User.username == username)
    if len(query) == 0:
        return False
    if check_password_hash(query[0].password, password):
        return True
    return False

def login(*, basic_auth=None, custom_auth=None, salt=None, expire_days=7):
    """Persistence auth

    You need to provide a function to implement your auth logic and pass it to ``basic_auth`` or ``custom_auth``
    parameter.

    :param callable basic_auth: ``(username, password) -> is_succeed:bool``
    :param callable custom_auth: ``() -> username:str``
    :param str salt: HMAC secret for the signature. It should be a long, random str.
    :param int expire_days: how many days the auth state can keep valid.
       After this time, logged-in users need to log in again.
    :return str: username of the currently logged-in user
    """
    assert bool(basic_auth) != bool(custom_auth), "You can only assign to one of `basic_auth` or `custom_auth`"

    token = get_localstorage('webio-token')  # get token from user's web browser
    # try to decrypt the username from the token
    username = decode_signed_value(salt, 'token', token, max_age_days=expire_days)
    if not token or not username:  # no token or token validation failed
        while True:
            if basic_auth:
                user = input_group('Login', [
                    input("Username", name='username'),
                    input("Password", type=PASSWORD, name='password'),
                ])
                username = user['username']
                ok = basic_auth(username, user['password'])
            else:
                username = ok = custom_auth()

            if ok:
                signed = create_signed_value(salt, 'token', username).decode("utf-8")  # encrypt username to token
                set_localstorage('webio-token', signed)  # set token to user's web browser
                break
    
    if type(username) == bytes:
        username = username.decode("utf8")
    local["username"] = username
    return username

def logout():
    set_localstorage('webio-token', None)
    del local["username"]


def needLogin(role):
    """role: <directeur>, <assistant>, <hotel>"""
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            username = login(basic_auth=checkConnection, salt="auie", expire_days=7)
            try:
                user = User.select().where(User.username == username).get()
            except DoesNotExist:
                logout()
                return
            if role == "all" or user.role == role:
                kwargs["username"] = username
                kwargs["role"] = user.role
                return func(*args, **kwargs)
            else:
                # TODO : logging invalid access
                with popup("Accès invalid"):
                    put_text("Nous n’avez pas les permissions d’accéder à cet espace")
        return wrapper
    return decorate
    