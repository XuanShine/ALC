from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.session import local, hold
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
    actions(buttons=["Continue"])
    return view()

def displayPEC():
    with put_collapse("PEC"):
        today = date.today()
        query = PEC.select()
        affichage = {"texte": [], "button": []}
        for pec in query:
            message = f"{pec.famille} : {pec.hotel}, fin: {pec.date_fin} ({(pec.date_fin - today).days} jours)"
            if pec.retard_pec():
                style = "color: red;"
            elif pec.proche_fin():
                style = "color: orange;"
            else:
                continue
            affichage["texte"].append(put_text(message).style(style))
            affichage["button"].append(put_button("Voir PEC", onclick=partial(GestionFamille.viewFamille, pec.famille.id)))
        put_table([[boutton, texte] for boutton, texte in zip(affichage["button"], affichage["texte"])]) # , cell_widths="10% 99%")
    return

def displayFamille():
    with put_collapse("Famille"):
        pass
    return 

def displayHotel():
    with put_collapse("Hotel"):
        pass
    return 