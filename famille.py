from logging import warning
from functools import partial
from typing import Union
from datetime import datetime, date

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import local, set_env
from pywebio_battery import put_logbox
from pywebio.pin import *

from peewee import fn

from models import *
import pec
from utils import sure, selectCalendar

class GestionFamille:
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
        elasticQuery = Famille.select()
        noms = list(set(famille.nom for famille in elasticQuery))
        
        familleNouvelle = input_group("Ajouter / Rechercher une Famille (renseigner au moins un des trois champs)", [
            input("Nom de la Famille", name="nomFamille", datalist=noms),
            input("ID", name="id"),
            input("Téléphone", name="telephone", help_text="Pour être efficace, ne mettez pas les deux premiers chiffres: 04 ou 06")
        ], validate=check_form)
        
        # on compare si le nom de famille lower est dans la base lower
        # et on compare si le tel sans espace est dans la base.
        if not familleNouvelle["nomFamille"]:
            query = Famille.select().where(
                (Famille.telephone.contains(familleNouvelle["telephone"].replace(" ", "")))
            )
        elif not familleNouvelle["telephone"]:
            query = Famille.select().where(
                (fn.LOWER(Famille.nom).contains(familleNouvelle["nomFamille"].lower()))
            )
        else:
            query = Famille.select().where(
                (fn.LOWER(Famille.nom).contains(familleNouvelle["nomFamille"].lower())) |
                (Famille.telephone.contains(familleNouvelle["telephone"].replace(" ", "")))
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
                return GestionFamille.viewFamille(selectFamille)

        # La famille n’existe pas     
        action = actions("La famille n’existe pas. Voulez-vous la créer ?", buttons=[
            ("Oui Créer une nouvelle famille", True),
            ("Non, Retour à la recherche", False)
        ])
        
        if action:
            famille = Famille.create(nom=familleNouvelle["nomFamille"], telephone=familleNouvelle["telephone"])
            return GestionFamille.viewFamille(famille.id)
        else:
            return GestionFamille.formAjoutFamille()
    
    @staticmethod
    @use_scope("main", clear=True)
    def viewFamille(familleID: int):
        famille = Famille.get(id=familleID)
        put_markdown(f"## Famille: {famille}")
        put_text(f"Telephone: {famille.telephone}")
        put_scrollable(content=["Notes", famille.notes], height=150)
        # put_button("Ajouter Note", onclick=partial(Famille.addRemarque, famille))
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
                    put_button("Ajouter Note", onclick=partial(GestionFamille.addRemarque, membre)), None,
                    put_button("Changer Informations", onclick=partial(GestionFamille.editMembre, membre.id)), None,
                    put_button("Supprimer", onclick=partial(sure, ifYes=partial(GestionFamille.deleteMembre, membre), ifNo=close_popup)), None
                ])
            ] for membre in famille.membres
            ],
            header=["Prénom", "Nom", "Sexe", "Naissance", "Titre", "Responsable", "Notes", "Action"]
        )
        put_markdown(f"### Prise en Charge (PEC):")
        if not famille.pecs.count():
            put_text(f"Aucun")
        else:
            GestionFamille.viewPecs(famille)
            # for pec in famille.pecs:
            #     put_text(f"Début : {pec.date_debut}\nFin : {pec.date_fin}\nDernière date Facturée : {pec.derniere_date_facturee}")
            #     for chambre in pec.chambres:
            #         put_text(f"{chambre.hotel.nom} - {chambre.hotel.ville} : {chambre.numero}")
        action = actions("", buttons=[{"label": "Changer Telephone", "value": "tel"},
                                      {"label": "Ajouter Membre", "value": "new"},
                                      {"label": "Ajouter notes", "value": "addNotes"},
                                      {"label": "Créer une PEC", "value": "newPEC", "color": "warning"}
                                     ])
 
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
                Membre.create(**nouveauMembre, famille=famille)
        elif action == "addNotes":
            GestionFamille.addRemarque(famille)
        elif action == "newPEC":
            put_info("Veuillez choisir une ou plusieurs chambres pour la famille")
            return pec.newPec(famille)
        return GestionFamille.viewFamille(familleID)
    
    @staticmethod
    def editMembre(membreID):
        membre = Membre.get(id=membreID)
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
        return GestionFamille.viewFamille(membre.famille.id)

    @staticmethod
    def deleteMembre(membre: Membre):
        famille = membre.famille
        membre.delete_instance()
        return GestionFamille.viewFamille(famille.id)

    @staticmethod
    def addRemarque(cible: Union[Membre, Famille]):
        note = textarea("Ajouter une note:")
        username = local["username"]
        time = datetime.now().strftime("%d/%m/%Y - %H:%M")
        cible.notes = f"{time} : {username} :\n{note}\n{'-' * 10}\n{cible.notes}"
        cible.save()
        if isinstance(cible, Membre):
            famille = cible.famille
        elif isinstance(cible, Famille):
            famille = cible
        return GestionFamille.viewFamille(famille.id)
    
    @staticmethod
    def viewPecs(famille):
        #breakpoint()
        put_table([
            [
                pec.date_debut.strftime("%d/%m/%Y"),
                pec.derniere_date_facturee.strftime("%d/%m/%Y"),
                put_text(pec.date_fin.strftime("%d/%m/%Y")).style(pec.style()),
                "Fini" if pec.fin_pec else "En Cours",
                pec.hotel,
                pec.get_chambres(),
                put_row([
                    put_button("Fin Prise en Charge", onclick=partial(selectCalendar, pec.fin_PEC, GestionFamille.viewFamille, famille)), None,
                    put_button("Facturer", onclick=partial(selectCalendar, pec.facturation, GestionFamille.viewFamille, famille)), None,
                    put_button("Prolonger/Tronquer", onclick=partial(selectCalendar, pec.renouvellement, GestionFamille.viewFamille, famille)), None
                ])
            ] for pec in famille.pecs
            ],
            header=["Début", "Dernière Facture", "Fin Prévu", "État", "Hôtel", "Chambre", "Action"]
        )