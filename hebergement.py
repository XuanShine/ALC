

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

from utils import sure

@use_scope("main", clear=True)
def gestion(tri: str = None, cp: str = None, ville: str = None, nom: str = None, occupation: int = None):
    """Affiche une barre de recherche
    "Nom hôtel" / "CP" / "Ville" avec un tri possible, et liste des hotels"""
    with use_scope("config"):
        put_text("TRI:", inline=True)
        put_buttons(["Code Postal", "Ville", "Nom"], onclick=[None, None, None])
        
    query = Hotel.select()
    
    for hotel in query:
        # put_row(size="auto 10px minmax(50px, 5%) 10px minmax(100px, 14%)", content=[
        #     put_text(hotel.cp), None,
        #     put_text(hotel.ville)
        #     put_collapse(title=f"{hotel.cp} - {hotel.ville} - {hotel.nom} ({hotel.disponibilite()}/{hotel.totalChambres()} libres)", content=[
                
        #     ])
        # ])
        try:
            chambres = sorted(hotel.chambres, key=lambda chambre: int(chambre.numero))
        except ValueError:
            chambres = hotel.chambres
        
        put_collapse(title=f"{hotel.cp} - {hotel.ville} - {hotel.nom} ({hotel.disponibilite()}/{hotel.totalChambres()} libres)", content=[
                put_row([put_text(header) for header in ["Numéro", "Convention", "Capacité", "Libre ?", "Prix", "Action"]])
            ] + [
            put_row([
                put_text(room.numero), None,
                put_text(emojis.encode(":white_check_mark:") if room.convention else emojis.encode(":x:")), None,
                put_text(room.capacite), None,
                put_button(f'{"Libre" if room.disponible_pour_alc() else "Voir PEC"}', color=f'{"success" if room.disponible_pour_alc() else "danger"}', onclick=""), None,
                put_text(room.prix), None,
                put_text("")
                
            ])
        for room in chambres])
    action = input_group("Recherche", inputs=[
        input("Nom", name="nom"),
        input("Code Postal", name="cp"),
        input("ville")
    ])
    return