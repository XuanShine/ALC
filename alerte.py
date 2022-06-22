from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.session import local
from pywebio.session import set_env
from pywebio.platform.flask import webio_view
import pywebio

from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from functools import partial

from models import *
from famille import GestionFamille

@use_scope("main", clear=True)
def view():
    displayPEC()
    displayFamille()
    displayHotel()
    input("")

def displayPEC():
    with put_collapse("PEC"):
        today = date.today()
        query = PEC.select()
        for pec in query:
            message = f"{pec.famille} : {pec.hotel}, fin: {pec.date_fin} ({(pec.date_fin - today).days} jours)"
            with put_row():
                if pec.retard_pec():
                    put_text(message).style("color: red;")
                elif pec.proche_fin():
                    put_text(message).style("color: orange;")
                else:
                    continue
                put_button("Voir PEC", onclick=partial(GestionFamille.viewFamille, pec.famille.id))
    return

def displayFamille():
    with put_collapse("Famille"):
        pass
    return 

def displayHotel():
    with put_collapse("Hotel"):
        pass
    return 