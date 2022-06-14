from click import pass_context
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.pin import *
from pywebio.session import set_env, local

from functools import partial
from typing import Union
from datetime import datetime

from peewee import fn
import emojis

from models import *
from utils import sure
from hebergement import showHotel

def connect():
    local
    showHotel(hotel)