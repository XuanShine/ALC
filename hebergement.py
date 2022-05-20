

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
import famille


@use_scope("main", clear=True)
def gestion(tri: str = None, cp: str = None, ville: str = None, nom: str = None, occupation: int = None, openHotel=None):
    """Affiche une barre de recherche
    "Nom hôtel" / "CP" / "Ville" avec un tri possible, et liste des hotels
    <tri>: str:  "cp" / "ville" / "nom"
    <openHotel> : Hotel or List(Hotel)
    """
    set_env(input_panel_fixed=False)
    # TODO: mettre une barre de recherche.
    
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
    # breakpoint()
    query = Hotel.select().order_by(sortKey)
    
    openHotel = openHotel if isinstance(openHotel, list) else [openHotel]
    for hotel in query:
        showHotel(hotel, open=(hotel in openHotel))
        
    action = actions("", buttons=[("Ajouter un hôtel", "addHotel")])
    if action == "addHotel":
        addHotel()
    # actions()
    return gestion(tri, cp, ville, nom, occupation)


def showHotel(hotel, open: bool = False):
    # TODO: gérer les chambres temporaires
    try:
        chambres = sorted(hotel.chambres, key=lambda chambre: int(chambre.numero))
    except ValueError:
        chambres = hotel.chambres
    
    put_collapse(title=f"{hotel.cp} - {hotel.ville} - {hotel.nom} ({hotel.disponibilite()}/{hotel.totalChambres()} libres)",
                 open=open, content=[

        put_text(f"ID Hotel: {hotel.id}\n{hotel.hotelname}\n{hotel.adresse}\n{hotel.telephone}\n{hotel.mail}"),
        put_row([
            put_button("Modifier", onclick=partial(editHotel, hotel)),
            put_button("Ajouter Chambre", onclick=partial(addRoom, hotel))
        ]),
        put_row([put_text(header) for header in ["Numéro", "Convention", "Capacité", "Libre ?", "Prix", "Action"]])
        ] + [
        put_row([
            put_text(f"{room.numero} {'' if not room.numeroTemporaire else '-> ' + room.numeroTemporaire}"), None,
            put_text(emojis.encode(":white_check_mark:") if room.convention else emojis.encode(":x:")), None,
            put_text(room.capacite), None,
            put_button(f'{"Sélectionner" if room.disponible_pour_alc() else "Voir PEC"}', color=f'{"success" if room.disponible_pour_alc() else "danger"}', onclick=partial(actionRoom, room)), None,
            put_text(room.prix), None,
            put_button("Modifier", onclick=partial(editRoom, room))
        ]) for room in chambres])
    return

def actionRoom(room):
    """Action sur la chambre lors du click
    - Aucun local.famille -> message d’information
    - Présence d’un local.famille:
        -> la chambre n’est pas <disponible_pour_alc> -> message d’erreur
        -> la chambre est déjà dans le local.chambres
        -> la chambre est disponible -> on ajoute au scope("chambre"). On reload "chambre"
    """
    if local.famille is None and room.pec:
        return famille.GestionFamille.viewFamille(room.pec.famille.id)
    if local.famille is None:
        toast("Aucune famille n’est sélectionnée pour créer une nouvelle prise en charge", color="error")
    elif not room.disponible_pour_alc():
        toast("Chambre non disponible", color="error")
    else:
        if local.chambres is None:
            clear("chambres")
            local.chambres = [room]
        elif room in local.chambres:
            toast("Chambre déjà sélectionnée", color="error")
            return 
        else:
            local.chambres.append(room)
        toast("Chambre sélectionnée", color="success")
        put_markdown(f"**{room.hotel}: {room}**", scope="chambres")
        
def editHotel(hotel):
    set_env(input_panel_fixed=True)
    datas = input_group(f"Modification {hotel.nom}", inputs=[
        input("Telephone", name="telephone", value=hotel.telephone),
        input("Mail", name="mail", value=hotel.mail, help_text="Pour des modifications importantes, veuillez contacter l’administrateur.")
    ])
    hotel.mail = datas["mail"]
    hotel.telephone = datas["telephone"]
    # TODO historique
    hotel.save()
    return gestion(openHotel=hotel)


def editRoom(room):
    set_env(input_panel_fixed=True)
    datas = input_group(f"Modification {room.hotel.nom} chambre: {room.numero}", inputs=[
        input("numero", readonly=True, value=room.numero, name="numero"),
        input("Numero Temporaire", value=room.numeroTemporaire, name="numeroTemporaire", help_text="Peut être vide"),
        input("Convention", value=room.convention, readonly=True, name="convention"),
        input("Capacite", name="capacite", value=room.capacite, type="number"),
        radio("", options=[("Disponible", True), ("Indisponible", False)], name="disponible", value=room.disponible),
        input("Prix", type="number", value=room.prix, name="prix")
    ])

    # TODO historique
    room.numeroTemporaire = datas["numeroTemporaire"]
    room.capacite = datas["capacite"]
    room.disponible = datas["disponible"]
    room.prix = datas["prix"]
    room.save()
    return gestion(openHotel=room.hotel)
    
    
def addHotel():
    datas = input_group(f"Ajout hôtel", inputs=[
        input("Nom", name="nom"),
        input("Identifiant Hotel", name="hotelname"),
        input("Adresse", name="adresse"),
        input("Ville", name="ville"),
        input("CP", name="cp"),
        input("Telephone", name="telephone"),
        input("Mail", name="mail")
    ])
    Hotel.create(**datas)
    return


def addRoom(hotel):
    datas = input_group(f"Ajout Chambre", inputs=[
        input("Numéro", name="numero"),
        # input("Convention", name="convention"),
        radio("Convention", options=[("oui", True), ("non", False, True)], inline=True, name="convention"),
        input("Capacite", name="capacite", type="number"),
        input("Prix journalier", name="prix"),
        radio("Disponible", options=[("oui", True), ("non", False, True)], inline=True, name="disponible"),
    ])
    Chambre.create(hotel=hotel, **datas)
    return gestion(openHotel=hotel)