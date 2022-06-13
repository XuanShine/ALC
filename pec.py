from pywebio.input import *
from pywebio.output import *
from pywebio.session import local, set_env
from pywebio.pin import *

from functools import partial
from typing import Union
from datetime import datetime, date

from peewee import fn

import famille
from models import *
from hebergement import gestion

@use_scope("famille", clear=True)
def newPec(famille):
    local.famille = famille
    put_info("Veuillez choisir une ou plusieurs chambres pour la famille")
    put_markdown(f"### Famille sélectionnée : {local.famille}").style("color:red;")
    chambresStr = 'aucun' if local.chambres is None else " - ".join(map(str, local.chambres))
    put_markdown(f"### Hotel sélectionné:")
    with use_scope("chambres"):
        put_text(chambresStr).style("color:red;")
    
    put_buttons([{"label": "Reset", "value": "removeFamily", "color": "warning"},
                 {"label": "Enlever Chambres", "value": "removeRoom"},
                 {"label": "Valider", "value": "valid", "color": "info"}],
                small=True,
                onclick=[resetPec, removeRoom, validate])
    #breakpoint()
    return gestion()
    
def resetPec():
    clear("famille")
    local.famille = None
    local.chambres = None

@use_scope("chambres", clear=True)
def removeRoom():
    put_text("aucun")
    local.chambres = None

@use_scope("main", clear=True)
def validate():
    """bien enlever tous le local à la fin"""
    assert local.famille is not None, "Aucune Famille n’a été sélectionnée"
    assert local.chambres is not None, "Aucune Chambre n’a été sélectionnée"
    familleID = local.famille.id
    data = input_group("Nouvelle PEC", cancelable=True, inputs=[
        input("Famille", readonly=True, value=str(local.famille), name="_")
    ] + [
        input(f"Chambre {i+1}", readonly=True, value=str(chambre), name=f"_{i}")
         for i, chambre in enumerate(local.chambres)
    ] + [
        input("Date Début", type="date", name="date_debut", required=True, value=datetime.now().date().strftime("%Y-%m-%d")),
        input("Date Fin", type="date", name="date_fin", required=True)
    ])
    if data is None:
        return gestion()
    pec = PEC.create(famille=local.famille, **data)
    pec.setChambres([chambre.id for chambre in local.chambres])
    toast("PEC ajouté avec succès !", color="success")
    local.famille = None
    local.chambres = None
    clear("famille")
    return famille.GestionFamille.viewFamille(familleID)
    
