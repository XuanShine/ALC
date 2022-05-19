from pywebio.input import *
from pywebio.output import *
from pywebio.session import local
from pywebio.pin import *
from functools import partial
import models as db
from typing import Union
from datetime import datetime, date
from peewee import fn
from pywebio.session import set_env

@use_scope("main")
def viewPec(famille=None, chambre=None):
    assert local.famille
    assert not famille or famille == local.famille
    
    put_text(f"## Famille: {local.famille}")
    
    