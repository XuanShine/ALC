from peewee import *
from typing import List, Text
from datetime import date, datetime, timedelta

from werkzeug.security import generate_password_hash, check_password_hash


db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db


class Famille(BaseModel):
    nom = CharField(max_length=50)
    telephone = CharField(max_length=20, default="")
    notes = TextField(default="")
    # TODO: notes
    # - historiques*
    # - pec+
    # - membres*

    def responsable(self):
        # query = Membre.select().where(Membre.estResponsable == True, Membre.famille == self)
        query = self.membres.where(Membre.estResponsable)
        if not query:
            return "Aucun indiqué"
        else:
            return " | ".join(map(str, query))

    def __str__(self):
        return f"{self.nom} - (id:{self.id})"

    def nombre(self):
        return len(self.membres)

class Membre(BaseModel):
    nom = CharField(max_length=50, null=True)
    prenom = CharField(max_length=50)
    sexe = CharField(max_length=1, choices=[("A", "Autre"), ("M", "Masculin"), ("F", "Feminin")])
    naissance = DateField()
    titre = CharField(max_length=50)
    estResponsable = BooleanField(default=False)
    famille = ForeignKeyField(Famille, backref="membres")
    notes = TextField(default="")
    # - historiques*
    
    def nomFamille(self):
        return self.nom if self.nom else self.famille.nom
    
    def age(self):
        return int((date.today() - self.naissance).days / 365.25)

    def __str__(self):
        return f"{self.prenom} {self.nomFamille()} ({self.sexe}) - {self.naissance}"

class User(BaseModel):
    username = CharField(unique=True)
    telephone = CharField()
    password = CharField()
    contactSiAbsent = ForeignKeyField("self", backref="remplace", default=None, null=True)
    role = CharField()
    # hotels*
    
    @property
    def hotel(self):
        return bool(self.hotels)

class Hotel(BaseModel):
    nom = CharField()
    hotelname = CharField(unique=True)
    owner = ForeignKeyField(User, backref="hotels")
    adresse = CharField()
    ville = CharField()
    cp = CharField(max_length=5)
    telephone = CharField()
    mail = CharField(max_length=100)
    notes = TextField(default="")
    # chambres*

    def __str__(self):
        """return ex: (id:34) Hotel Panorama - Grasse"""
        return f"(id:{self.id}) {self.nom} - {self.ville}"
    
    def disponibilite(self):
        return len([chambre for chambre in self.chambres if chambre.disponible_pour_alc()])
    
    def totalChambres(self):
        return len(self.chambres)


class PEC(BaseModel):
    # Lors du renouvellement, la date de fin est modifié.
    # Une fin de prise en charge modifie la date de fin et facture la PEC
    # Sur action, facture la prise en charge et change la derniere_date_facturee
    # Un changement de prix de la chambre facture la prise en charge et change le prix de la chambre
    # Un changement de chambre facture. Change la date facturation, change la chambre.
    famille = ForeignKeyField(Famille, backref="pecs")
    hotel = ForeignKeyField(Hotel, backref="pecs", null=True)
    date_debut = DateField()
    date_fin = DateField()
    _derniere_date_facturee = DateField(null=True)
    historique_chambres = CharField(default="")
    fin_pec = BooleanField(default=False)
    # - chambres*
    # - historiques*
    
    @property
    def derniere_date_facturee(self):
        if not self._derniere_date_facturee:
            self._derniere_date_facturee = self.date_debut
        return self._derniere_date_facturee

    @derniere_date_facturee.setter
    def derniere_date_facturee(self, date_facture):
        self._derniere_date_facturee = date_facture
        
    def setChambres(self, idChambres: List[int]):
        for id_ in idChambres:
            chambre = Chambre.get(id=id_)
            chambre.pec = self
            chambre.disponible = False
            chambre.save()
            self.historique_chambres += f"{chambre}, "
            # breakpoint()
            self.hotel = chambre.hotel
        self.save()
        # breakpoint()
    
    def renouvellement(self, nouvelle_date_fin):
        assert nouvelle_date_fin >= self.derniere_date_facturee
        self.date_fin = nouvelle_date_fin
        self.save()
    
    def proche_fin(self):
        return self.date_fin < timedelta(days=7) + datetime.now().date()
    
    def retard_pec(self):
        return (not self.fin_pec) and self.date_fin < datetime.now().date()
    
    def actuelle(self):
        return not self.fin_pec
    
    def facturation(self, date):
        """
        assert date_derniere_facture < date < date_fin
        Pour facturer:
        Quand on facture, on facture à la date où le client "part"
        1/ On calcul le nombre de jour entre la <date> et <date_derniere_fature>
        2/ Pour chaque chambre, on le multiplie par le prix
        3/ On édite une demande de facture.
        4/ On change la <date_derniere_facture>
        """
        assert self.derniere_date_facturee <= date <= self.date_fin
        days = (date - self.derniere_date_facturee).days
        res = sum(days * chambre.prix for chambre in self.chambres)
        self.derniere_date_facturee = date
        self.save()
        return res

    def fin_PEC(self, nouveau_date_fin):
        """Fin PEC:
        1/ On facture
        2/ On change .fin_pec = True
        3/ On change .chambres.pec = None
        4/ On change date_fin
        """
        self.date_fin = nouveau_date_fin
        res = self.facturation(nouveau_date_fin)
        self.fin_pec = True
        for chambre in self.chambres:
            chambre.pec = None
            chambre.disponible = True
            chambre.save()
        self.save()
        return res

    def get_chambres(self):
        return self.historique_chambres if self.fin_pec else " ".join(map(str, self.chambres))

    def change_chambre(self, ancienne_chambre, nouvelle_chambre):
        pass

    def style(self):
        "style for pywebio"
        if self.retard_pec():
            return "background-color: red;"
        if self.proche_fin():
            return "background-color: orange;"
        else:
            return ""
    

class Chambre(BaseModel):
    numero = CharField()
    numeroTemporaire = CharField(default="")
    convention = BooleanField(default=False)
    capacite = SmallIntegerField(default=2)
    _disponible = BooleanField(default=False)
    prix = IntegerField()
    
    hotel = ForeignKeyField(Hotel, backref="chambres")
    pec = ForeignKeyField(PEC, backref="chambres", null=True)
    
    def famille(self):
        raise NotImplemented()

    def __str__(self):
        add_str = f" ({self.numeroTemporaire})" if self.numeroTemporaire else ""
        return f"{self.numero}" + add_str

    @property
    def disponible(self):
        return self.disponible_pour_alc()

    @disponible.setter
    def disponible(self, value:bool):
        self._disponible = value
    
    def disponible_pour_alc(self):
        """Pour information"""
        if self.pec or (not self._disponible):
            return False
        return True



    