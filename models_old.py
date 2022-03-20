import datetime

from peewee import *

db = SqliteDatabase('alc.db')
from datetime import timezone



class BaseModel(Model):
    class Meta:
        database = db

class Famille(BaseModel):
    nom = CharField()

    def responsable(self):
        query = self.membres.filter(est_responsable=True)
        if not query:
            return "Aucun indiqué"
        else:
            return " | ".join(map(str, query))

    def __str__(self):
        return self.nom + " - " + str(self.id)

    def nombre(self):
        return len(self.membres.all())

class Membre(BaseModel):
    AUTRE = 0
    MALE = 1
    FEMELE = 2
    SEXE = (
        (AUTRE, "Autre"),
        (MALE, "Masculin"),
        (FEMELE, "Féminin")
        
    )
    nom = CharField()
    prenom = CharField()
    sexe = IntegerField(default=AUTRE, choices=SEXE)
    naissance = DateField()
    titre = CharField()  # père, mère, enfant
    est_responsable = BooleanField(default=False)
    famille = ForeignKeyField(Famille, backref="membres")

    def __str__(self):
        return self.nom + " " + self.prenom + " " + str(self.naissance.year)
    
    def age(self):
        return int((timezone.now().date() - self.naissance).days / 365.25)


class Hotel(BaseModel):
    nom = CharField()
    adresse = CharField()
    telephone = CharField()
    mail = CharField(max_length=100)

    def __str__(self):
        return self.nom + " - " + str(self.id)
    
    def disponibilite(self):
        return len(self.chambres.filter(disponible=True))


class Employe(BaseModel):
    nom = CharField()


class PEC(BaseModel):
    # Lors du renouvellement, la date de fin est modifié.
    # Une fin de prise en charge modifie la date de fin et facture la PEC
    # Sur action, facture la prise en charge et change la derniere_date_facturee
    # Un changement de prix de la chambre facture la prise en charge et change le prix de la chambre
    # Un changement de chambre facture. Change la date facturation, change la chambre.
    famille = ForeignKeyField(Famille, backref="pec")
    date_debut = DateField()
    date_fin = DateField()
    derniere_date_facturee = DateField(null=True)
    
    def renouvellement(self, nouvelle_date_fin):
        self.date_fin = nouvelle_date_fin
    
    def proche_fin(self):
        return self.date_fin + datetime.timedelta(days=7) < timezone.now().date()
    
    def facturation(self, date):
        pass

    def fin_PEC(self, nouveau_date_fin):
        pass

    def change_prix(self, chambre, nouveau_prix):
        self.facturation()

        query = self.chambres.filter(numero=chambre)
        assert len(query) == 1  # TODO gérer l’erreur
        query[0].prix = nouveau_prix

    def change_chambre(self, ancienne_chambre, nouvelle_chambre):
        pass


class Chambre(BaseModel):
    numero = CharField()
    convention = BooleanField(default=False)
    capacite = IntegerField(default=2)
    disponible = BooleanField(default=False)
    prix = IntegerField(null=True)
    
    hotel = ForeignKeyField(Hotel, backref="chambres")
    pec = ForeignKeyField(PEC, backref="chambres")

    def __str__(self):
        return self.numero

    def disponible_pour_alc(self):
        """Pour information"""
        if (not self.PEC) or (not self.disponible):
            return False
        return True