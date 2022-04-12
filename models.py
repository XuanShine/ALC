from peewee import *
from datetime import date, datetime

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
        return self.nom + " - " + str(self.id)

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


class Hotel(BaseModel):
    nom = CharField()
    hotelname = CharField(unique=True)
    adresse = CharField()
    ville = CharField()
    cp = CharField(max_length=5)
    telephone = CharField()
    mail = CharField(max_length=100)
    # chambres*

    def __str__(self):
        """return ex: (id=34) Hotel Panorama - Grasse"""
        return f"{self.id=} {self.nom} - {self.ville}"
    
    def disponibilite(self):
        return len(self.chambres.where(Chambre.disponible == True))
    
    def totalChambres(self):
        return len(self.chambres)


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
    # - chambres*
    # - historiques*

    def setChambres(self, idChambres):
        for id_ in idChambres:
            chambre = Chambre.get(id=id_)
            chambre.pec = self
            chambre.save()
    
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
    
    def hotel(self):
        raise NotImplemented()
    

class Chambre(BaseModel):
    numero = CharField()
    numeroTemporaire = CharField(null=True)
    convention = BooleanField(default=False)
    capacite = SmallIntegerField(default=2)
    disponible = BooleanField(default=False)
    prix = IntegerField()
    
    hotel = ForeignKeyField(Hotel, backref="chambres")
    pec = ForeignKeyField(PEC, backref="chambres", null=True)
    
    def famille(self):
        raise NotImplemented()

    def __str__(self):
        return self.numero

    def disponible_pour_alc(self):
        """Pour information"""
        if (not self.PEC) or (not self.disponible):
            return False
        return True