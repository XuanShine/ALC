from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import local
from pywebio_battery import put_logbox
from pywebio.pin import *
from functools import partial
import models as db
from typing import Union
from datetime import datetime, date
from peewee import fn
from pywebio.session import set_env

import pec

from utils import sure, clearFamille

class Famille:
    @staticmethod
    @use_scope("main", clear=True)
    def formAjoutFamille():
        set_env(input_panel_fixed=True, input_panel_init_height=175)
        
        def render_famille(famille):
            put_column([
                put_markdown(f"## {famille}"),
                put_text(f"Téléphone: {famille.telephone}"),
                put_text("Composition de la famille:"),
                put_column([put_text(f"{membre}") for membre in famille.membres])
            ])
        
        def check_form(data):
            if not data["nomFamille"] and not data["telephone"] and not data["id"]:
                return ("nomFamille", "Renseigner au moins un des trois champs")
        #####
        
        # ElasticSearch
        elasticQuery = db.Famille.select()
        noms = list(set(famille.nom for famille in elasticQuery))
        
        familleNouvelle = input_group("Ajouter / Rechercher une Famille (renseigner au moins un des trois champs)", [
            input("Nom de la Famille", name="nomFamille", datalist=noms),
            input("ID", name="id"),
            input("Téléphone", name="telephone", help_text="Pour être efficace, ne mettez pas les deux premiers chiffres: 04 ou 06")
        ], validate=check_form)
        
        # on compare si le nom de famille lower est dans la base lower
        # et on compare si le tel sans espace est dans la base.
        if not familleNouvelle["nomFamille"]:
            query = db.Famille.select().where(
                (db.Famille.telephone.contains(familleNouvelle["telephone"].replace(" ", "")))
            )
        elif not familleNouvelle["telephone"]:
            query = db.Famille.select().where(
                (fn.LOWER(db.Famille.nom).contains(familleNouvelle["nomFamille"].lower()))
            )
        else:
            query = db.Famille.select().where(
                (fn.LOWER(db.Famille.nom).contains(familleNouvelle["nomFamille"].lower())) |
                (db.Famille.telephone.contains(familleNouvelle["telephone"].replace(" ", "")))
            )
        
        if query:  # Si la famille existe
            put_markdown("## La famille semble exister")
            put_column([render_famille(famille) for famille in query])
            selectFamille = actions("Selectionner la famille désirée:", buttons=[
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
                return Famille.viewFamille(selectFamille)

        # La famille n’existe pas     
        action = actions("La famille n’existe pas. Voulez-vous la créer ?", buttons=[
            ("Oui Créer une nouvelle famille", True),
            ("Non, Retour à la recherche", False)
        ])
        
        if action:
            famille = db.Famille.create(nom=familleNouvelle["nomFamille"], telephone=familleNouvelle["telephone"])
            return Famille.viewFamille(famille.id)
        else:
            return Famille.formAjoutFamille()
    
    @staticmethod
    @use_scope("main", clear=True)
    def viewFamille(familleID: int):
        famille = db.Famille.get(id=familleID)
        put_markdown(f"## Famille: {famille.nom}")
        put_text(f"Telephone: {famille.telephone}")
        put_scrollable(content=["Notes", famille.notes], keep_bottom=True, height=150)
        put_button("Ajouter Note", onclick=partial(Famille.addRemarque, famille))
        put_markdown(f"### Membres ({len(famille.membres)})")
        put_table([
            [
                membre.prenom,
                membre.nomFamille(),
                str(membre.sexe),
                f'{membre.naissance.strftime("%d/%m/%Y")} ({int((date.today()-membre.naissance).days/365)} ans)',
                membre.titre,
                "oui" if membre.estResponsable else "non",
                put_collapse("Notes", content=membre.notes),
                put_row([
                    put_button("Ajouter Note", onclick=partial(Famille.addRemarque, membre)), None,
                    put_button("Changer Informations", onclick=partial(Famille.editMembre, membre.id)), None,
                    put_button("Supprimer", onclick=partial(sure, ifYes=partial(Famille.deleteMembre, membre), ifNo=close_popup)), None
                ])
            ] for membre in famille.membres
            ],
            header=["Prénom", "Nom", "Sexe", "Naissance", "Titre", "Responsable", "Notes", "Action"]
        )
        put_markdown(f"### Prise en Charge (PEC):")
        if not famille.pec.count():
            put_text(f"Aucun")
        else:
            for pec in famille.pecs:
                put_text(f"Début : {pec.date_debut}\nFin : {pec.date_fin}\nDernière date Facturée : {pec.derniere_date_facturee}")
                for chambre in pec.chambres:
                    put_text(f"{chambre.hotel.nom} - {chambre.hotel.ville} : {chambre.numero}")
        action = actions("", buttons=[{"label": "Changer Telephone", "value": "tel"},
                                      {"label": "Ajouter Membre", "value": "new"},
                                      {"label": "Créer une PEC", "value": "createPec",
                                       "disabled": famille.pec.count() != 0,
                                       "color": "danger"},
                                      {"label": "Voir la PEC", "value": "viewPec",
                                       "disabled": famille.pec.count() == 0,
                                       "color": "danger"}])
 
        if action == "tel":
            telephone = input("Telephone")
            if telephone:
                famille.telephone = telephone.replace(" ", "")
                famille.save()
        elif action == "new":
            nouveauMembre = input_group("Nouveau Membre", cancelable=True, inputs=[
                input("Prénom", name="prenom", required=True),
                input("Nom", name="nom", value=famille.nom),
                radio("Sexe", name="sexe", required=True, inline=True,
                      options=[("Male", "M"), ("Femelle", "F"), ("Autre", "A")]),
                input("Date de Naissance", name="naissance", type="date", required=True),
                input("Titre (père, mère, enfant, ...)", name="titre", required=True,
                      datalist=["père", "mère", "enfant"]),
                radio("Est Responsable", name="estResponsable", required=True,
                      options=[("Oui", True), ("Non", False, True)], inline=True),
                textarea("Remarques", name="notes")
            ])
            if nouveauMembre:
                db.Membre.create(**nouveauMembre, famille=famille)
        elif action == "createPec" or action == "viewPec":
            local.famille = famille
            with use_scope("famille", clear=True):
                put_markdown(f"##Famille sélectionnée: {local.famille}")
                put_button("Enlever famille", onclick=clearFamille, color="danger")
            return pec.viewPec(famille=famille)
        return Famille.viewFamille(familleID)
    
    @staticmethod
    def editMembre(membreID):
        membre = db.Membre.get(id=membreID)
        editMembre = input_group(f"{membre.prenom} {membre.nomFamille()}", cancelable=True, inputs=[
            input("Prénom", name="prenom", required=True, value=membre.prenom),
            input("Nom", name="nom", value=membre.nomFamille()),
            radio("Sexe", name="sexe", required=True, inline=True, value=membre.sexe,
                    options=[("Male", "M"), ("Femelle", "F"), ("Autre", "A")]),
            input("Titre (père, mère, enfant, ...)", name="titre", required=True, value=membre.titre,
                    datalist=["père", "mère", "enfant"]),
            radio("Est Responsable", name="estResponsable", required=True, value=membre.estResponsable,
                    options=[("Oui", True), ("Non", False, True)], inline=True),
            textarea("Remarques", name="notes", value=membre.notes, readonly=True)
        ])
        membre.prenom = editMembre["prenom"]
        membre.nom = editMembre["nom"]
        membre.sexe = editMembre["sexe"]
        membre.titre = editMembre["titre"]
        membre.estResponsable = editMembre["estResponsable"]
        membre.save()
        return Famille.viewFamille(membre.famille.id)

    @staticmethod
    def deleteMembre(membre: db.Membre):
        famille = membre.famille
        membre.delete_instance()
        return Famille.viewFamille(famille.id)

    @staticmethod
    def addRemarque(cible: Union[db.Membre, db.Famille]):
        note = textarea("Ajouter une note:")
        # TODO: ajouter le nom de la personne qui a écrit la note
        time = datetime.now().strftime("%d/%m/%Y - %H:%M")
        cible.notes = f"{cible.notes}\n{'-' * 10}\n{time} :\n{note}"
        cible.save()
        if isinstance(cible, db.Membre):
            famille = cible.famille
        elif isinstance(cible, db.Famille):
            famille = cible
        return Famille.viewFamille(famille.id)
    