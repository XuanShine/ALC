

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.pin import *
from functools import partial
from models import *
from typing import Union
from datetime import datetime
from peewee import fn

from utils import sure

@use_scope("main", clear=True)
def gestion():
    """Affiche une barre de recherche
    "Nom hôtel" / "CP" / "Ville" avec un tri possible, et liste des hotels"""
    query = Chambre.select()
    
    
    return