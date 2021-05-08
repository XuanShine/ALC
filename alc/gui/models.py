import datetime

from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    

class Famille(models.Model):
    nom = models.CharField(max_length=200)

    class Meta:
        ordering = ["nom"]

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

class Membre(models.Model):
    AUTRE = 0
    MALE = 1
    FEMELE = 2
    SEXE = (
        (AUTRE, "Autre"),
        (MALE, "Masculin"),
        (FEMELE, "Féminin")
        
    )
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    sexe = models.IntegerField(default=AUTRE, choice=SEXE)
    naissance = models.DateField()
    titre = models.CharField(max_length=200)  # père, mère, enfant
    est_responsable = models.BooleanField(default=False)
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name="membres")

    def __str__(self):
        return self.nom + " " + self.prenom + " " + str(self.naissance.year)
    
    def age(self):
        return int((timezone.now().date() - self.naissance).days / 365.25)


class Hotel(models.Model):
    nom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    mail = models.EmailField()

    class Meta:
        ordering = ["nom"]

    def __str__(self):
        return self.nom + " - " + str(self.id)
    
    def disponibilite(self):
        return len(self.chambres.filter(disponible=True))
    


class Chambre(models.Model):
    numero = models.CharField(max_length=200)
    convention = models.BooleanField(default=False)
    capacite = models.IntegerField(default=2)
    disponible = models.BooleanField(default=False)
    prix = models.IntegerField(blank=True, null=True)

    hotel = ForeignKey(Hotel, on_delete=models.CASCADE, related_name="chambres")
    PEC = ForeignKey("PEC", on_delete=models.DO_NOTHING, blank=True, null=True, related_name="chambres")

    class Meta:
        ordering = ["numero"]

    def __str__(self):
        return self.numero


class PEC(models.Model):
    # Lors du renouvellement, la date de fin est modifié.
    # Une fin de prise en charge modifie la date de fin et facture la PEC
    # Sur action, facture la prise en charge et change la derniere_date_facturee
    # Un changement de prix de la chambre facture la prise en charge et change le prix de la chambre
    # Un changement de chambre facture. Change la date facturation, change la chambre.
    famille = ForeignKey(Famille, on_delete=models.PROTECT, related_name="PEC")
    date_debut = models.DateField()
    date_fin = models.DateField()
    derniere_date_facturee = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["date_fin"]
    
    def renouvellement(self, nouvelle_date_fin):
        self.date_fin = nouvelle_date_fin
    
    def proche_fin(self):
        return self.date_fin + dt.timedelta(days=7) < timezone.now().date()
    
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
