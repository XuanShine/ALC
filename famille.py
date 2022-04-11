from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.pin import *
from functools import partial
import models as db
from typing import Union
from datetime import datetime, date
from peewee import fn

from utils import sure

class Famille:
    @staticmethod
    @use_scope("main", clear=True)
    def formAjoutFamille():
        def render_famille(famille):
            put_column([
                put_markdown(f"## {famille}"),
                put_text(f"Téléphone: {famille.telephone}"),
                put_text("Composition de la famille:"),
                put_column([put_text(f"{membre}") for membre in famille.membres])
            ])
        
        def check_form(data):
            if not data["nomFamille"] and not data["telephone"]:
                return ("nomFamille", "Renseigner au moins un des deux champs")
        #####
        
        familleNouvelle = input_group("Ajouter / Rechercher une Famille (renseigner au moins un des deux champs)", [
            input("Nom de la Famille", name="nomFamille"),
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
        action = actions("", buttons=[("Changer Telephone", "tel"),
                                      ("Ajouter Membre", "new")])
 
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
    