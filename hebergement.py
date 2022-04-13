

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
import emojis
from pywebio.session import set_env

from utils import sure

@use_scope("main", clear=True)
def gestion(tri: str = None, cp: str = None, ville: str = None, nom: str = None, occupation: int = None):
    """Affiche une barre de recherche
    "Nom hôtel" / "CP" / "Ville" avec un tri possible, et liste des hotels
    <tri>: str:  "cp" / "ville" / "nom"
    """
    set_env(input_panel_fixed=False)
    
    with use_scope("config"):
        put_text("TRI:", inline=True)
        put_buttons(["Code Postal", "Ville", "Nom"], onclick=[partial(gestion, tri="cp"), partial(gestion, tri="ville"), partial(gestion, tri="nom")])
    
    if tri == "cp":
        sortKey = Hotel.cp
    elif tri == "ville":
        sortKey = Hotel.ville
    elif tri == "nom":
        sortKey = Hotel.nom
    else:
        sortKey = Hotel.cp
    query = Hotel.select().order_by(sortKey)
    
    for hotel in query:
        try:
            chambres = sorted(hotel.chambres, key=lambda chambre: int(chambre.numero))
        except ValueError:
            chambres = hotel.chambres
        
        put_collapse(title=f"{hotel.cp} - {hotel.ville} - {hotel.nom} ({hotel.disponibilite()}/{hotel.totalChambres()} libres)", content=[
            put_row([
                put_button("Modifier", onclick=partial(editHotel, hotel))
            ])] + [
            put_row([put_text(header) for header in ["Numéro", "Convention", "Capacité", "Libre ?", "Prix", "Action"]])
            ] + [
            put_row([
                put_text(room.numero), None,
                put_text(emojis.encode(":white_check_mark:") if room.convention else emojis.encode(":x:")), None,
                put_text(room.capacite), None,
                put_button(f'{"Libre" if room.disponible_pour_alc() else "Voir PEC"}', color=f'{"success" if room.disponible_pour_alc() else "danger"}', onclick=""), None,
                put_text(room.prix), None,
                put_button("Modifier")
                
            ])
        for room in chambres])
    
    # ElasticSearch
    # query = Hotel.select()
    # noms = set()
    # cps = set()
    # villes = set()
    # for hotel in query:
    #     noms.add(hotel.nom)
    #     cps.add(hotel.cp)
    #     villes.add(hotel.ville)
        
    actions(buttons=["Ajouter un hôtel"])
    return gestion(tri, cp, ville, nom, occupation)

def editHotel(hotel):
    return