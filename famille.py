from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.pin import *
from functools import partial
import models as db
from typing import Union

class Famille:
    @staticmethod
    @use_scope("main", clear=True)
    def formAjoutFamille():
        def render_famille(famille):
            put_column([
                put_markdown(f"# {famille}"),
                put_column([put_text(f"{membre}") for membre in famille.membres])
            ])
        #####
        
        familleNouvelle = input_group("Nouvelle Famille", [
            input("Nom de la Famille", name="nomFamille", required=True),
            input("Téléphone", name="telephone")
        ])
        
        query = db.Famille.select().where(db.Famille.nom == familleNouvelle["nomFamille"])
        
        if query:  # Si la famille existe
            put_text("La famille semble exister")
            put_column([render_famille(famille) for famille in query])
            selectFamille = actions("Selectionner:", buttons=[
                {
                    "label": str(famille),
                    "value": famille.id
                } for famille in query] + 
                [{
                    "label": "Ajouter une nouvelle Famille",
                    "value": 0,
                    "color": "success"
                }])
            if selectFamille != 0:
                return Famille.editFamille(selectFamille)

        # La famille n’existe pas
        famille = db.Famille.create(nom=familleNouvelle["nomFamille"], telephone=familleNouvelle["telephone"])
        return Famille.editFamille(famille.id)
    
    @staticmethod
    @use_scope("main", clear=True)
    def editFamille(id_: int):
        famille = db.Famille.get(id=id_)
        
        
        