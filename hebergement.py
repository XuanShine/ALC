

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.pin import *
from functools import partial
import models as db
from typing import Union
from datetime import datetime
from peewee import fn

from utils import sure

@use_scope("main", clear=True)
def gestion():
    actions("", buttons=[
        ()
    ])
    return